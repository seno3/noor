document.addEventListener('DOMContentLoaded', () => {
    const checkbox = document.getElementById('enableFactCheck');
    const status = document.getElementById('status');
    const serverStatus = document.getElementById('serverStatus');
    const debugButton = document.getElementById('debugFactCheck');
    const debugStatus = document.getElementById('debugStatus');
    
    // Ensure debug button exists and is visible
    if (!debugButton) {
        console.error('Debug button element not found!');
        return;
    }
    
    if (!debugStatus) {
        console.error('Debug status element not found!');
        return;
    }
    
    // Make absolutely sure button is visible
    debugButton.style.display = 'block';
    debugButton.style.visibility = 'visible';
    debugButton.style.opacity = '1';
    
    // Check server status
    async function checkServerStatus() {
        try {
            const response = await fetch('http://localhost:8004/health', {
                method: 'GET',
                timeout: 2000
            });
            
            if (response.ok) {
                serverStatus.className = 'status-indicator status-online';
                serverStatus.title = 'Server is online';
            } else {
                serverStatus.className = 'status-indicator status-offline';
                serverStatus.title = 'Server error';
            }
        } catch (error) {
            serverStatus.className = 'status-indicator status-offline';
            serverStatus.title = 'Server is offline';
        }
    }
    
    // Check server status on load and every 10 seconds
    checkServerStatus();
    setInterval(checkServerStatus, 10000);
    
    // Load saved settings
    chrome.storage.sync.get(['enableFactCheck'], (data) => {
        checkbox.checked = data.enableFactCheck !== false;
    });
    
    // Save settings on change
    checkbox.addEventListener('change', () => {
        chrome.storage.sync.set({ enableFactCheck: checkbox.checked }, () => {
            // Show status message
            if (checkbox.checked) {
                status.textContent = '✓ Verification enabled';
                status.className = 'status-success';
            } else {
                status.textContent = 'Verification disabled';
                status.className = '';
                status.style.color = '#9ca3af';
            }
            setTimeout(() => {
                status.textContent = '';
                status.className = '';
            }, 2000);
            
            // Notify content script of the change
            chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
                if (tabs[0]) {
                    chrome.tabs.sendMessage(tabs[0].id, {
                        type: 'SETTING_CHANGED',
                        enableFactCheck: checkbox.checked
                    }).catch(() => {
                        // Ignore errors if tab doesn't have content script
                    });
                }
            });
        });
    });
    
    // Reset button: Reset stuck fact check
    const resetButton = document.getElementById('resetFactCheck');
    if (resetButton) {
        resetButton.addEventListener('click', async () => {
            resetButton.disabled = true;
            resetButton.textContent = '🔄 Resetting...';
            debugStatus.textContent = '';
            
            try {
                const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
                
                if (!tab || !tab.url || !tab.url.includes('youtube.com')) {
                    debugStatus.textContent = '⚠️ This only works on YouTube pages';
                    debugStatus.style.color = '#f59e0b';
                    resetButton.disabled = false;
                    resetButton.textContent = '🔄 Reset (if stuck)';
                    return;
                }
                
                // Try to inject script first if needed
                try {
                    await chrome.scripting.executeScript({
                        target: { tabId: tab.id },
                        files: ['contentScript.js']
                    });
                } catch (injectError) {
                    // Script might already be loaded, continue
                    console.log('Script injection note:', injectError.message);
                }
                
                // Small delay to ensure script is ready
                await new Promise(resolve => setTimeout(resolve, 200));
                
                // Send reset message with timeout
                const resetPromise = new Promise((resolve, reject) => {
                    const timeout = setTimeout(() => {
                        reject(new Error('Reset timeout - script may not be loaded'));
                    }, 2000);
                    
                    chrome.tabs.sendMessage(tab.id, { type: 'RESET_FACT_CHECK' }, (response) => {
                        clearTimeout(timeout);
                        if (chrome.runtime.lastError) {
                            reject(new Error(chrome.runtime.lastError.message));
                        } else {
                            resolve(response);
                        }
                    });
                });
                
                try {
                    const response = await resetPromise;
                    if (response && response.success) {
                        debugStatus.textContent = '✅ Fact check reset! You can try again now.';
                        debugStatus.style.color = '#10b981';
                    } else {
                        debugStatus.textContent = '⚠️ Reset sent, but no confirmation';
                        debugStatus.style.color = '#f59e0b';
                    }
                } catch (error) {
                    if (error.message.includes('timeout')) {
                        debugStatus.textContent = '⚠️ Script not responding. Try refreshing the page.';
                    } else {
                        debugStatus.textContent = `❌ Error: ${error.message}`;
                    }
                    debugStatus.style.color = '#ef4444';
                }
                
                resetButton.disabled = false;
                resetButton.textContent = '🔄 Reset (if stuck)';
                
                setTimeout(() => {
                    debugStatus.textContent = '';
                }, 3000);
            } catch (error) {
                debugStatus.textContent = `❌ Error: ${error.message}`;
                debugStatus.style.color = '#ef4444';
                resetButton.disabled = false;
                resetButton.textContent = '🔄 Reset (if stuck)';
            }
        });
    }
    
    // Debug button: Force fact check
    debugButton.addEventListener('click', async () => {
        debugButton.disabled = true;
        debugButton.textContent = '🔄 Checking...';
        debugStatus.textContent = '';
        debugStatus.style.color = '';
        
        try {
            // Get current active tab
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            
            if (!tab) {
                debugStatus.textContent = '❌ No active tab found';
                debugStatus.style.color = '#ef4444';
                debugButton.disabled = false;
                debugButton.textContent = '🔍 Debug: Force Fact Check';
                return;
            }
            
            // Check if it's a YouTube page
            if (!tab.url || !tab.url.includes('youtube.com')) {
                debugStatus.textContent = '⚠️ This only works on YouTube pages';
                debugStatus.style.color = '#f59e0b';
                debugButton.disabled = false;
                debugButton.textContent = '🔍 Debug: Force Fact Check';
                return;
            }
            
            debugStatus.textContent = '📤 Injecting content script...';
            debugStatus.style.color = '#3b82f6';
            
            // Step 1: Inject the script
            try {
                await chrome.scripting.executeScript({
                    target: { tabId: tab.id },
                    files: ['contentScript.js']
                });
                console.log('✅ Content script injected successfully');
                debugStatus.textContent = '⏳ Waiting for script to initialize...';
            } catch (injectError) {
                console.log('⚠️ Script injection note:', injectError.message);
                // Continue anyway - script might already be there
            }
            
            // Step 2: Wait and verify script is ready with ping
            debugStatus.textContent = '🔍 Verifying script is ready...';
            let scriptReady = false;
            let retryCount = 0;
            const maxRetries = 5;
            
            while (!scriptReady && retryCount < maxRetries) {
                await new Promise(resolve => setTimeout(resolve, 300));
                
                try {
                    const pingResponse = await new Promise((resolve, reject) => {
                        chrome.tabs.sendMessage(tab.id, { type: 'PING' }, (response) => {
                            if (chrome.runtime.lastError) {
                                reject(new Error(chrome.runtime.lastError.message));
                            } else {
                                resolve(response);
                            }
                        });
                    });
                    
                    if (pingResponse && pingResponse.ready) {
                        scriptReady = true;
                        console.log('✅ Script is ready and responding!');
                    }
                } catch (error) {
                    retryCount++;
                    console.log(`⏳ Ping attempt ${retryCount}/${maxRetries} failed, retrying...`);
                }
            }
            
            if (!scriptReady) {
                debugStatus.textContent = '❌ Script not responding. Try refreshing the page.';
                debugStatus.style.color = '#ef4444';
                debugButton.disabled = false;
                debugButton.textContent = '🔍 Debug: Force Fact Check';
                return;
            }
            
            // Step 3: Script is ready, trigger fact check
            debugStatus.textContent = '🚀 Triggering fact check...';
            debugStatus.style.color = '#3b82f6';
            
            const testText = 'The Prophet Muhammad said that love of one\'s country is part of faith. In Surah 2:255, Allah says that He knows what is in the heavens and the earth.';
            
            chrome.tabs.sendMessage(tab.id, {
                type: 'DEBUG_FACT_CHECK',
                testText: testText
            }, (response) => {
                if (chrome.runtime.lastError) {
                    debugStatus.textContent = `❌ Error: ${chrome.runtime.lastError.message}`;
                    debugStatus.style.color = '#ef4444';
                } else if (response && response.success) {
                    debugStatus.textContent = '✅ Fact check triggered! Check console (F12) and page for results.';
                    debugStatus.style.color = '#10b981';
                } else {
                    debugStatus.textContent = response?.message || '⚠️ Fact check triggered, but no response received';
                    debugStatus.style.color = '#f59e0b';
                }
                
                debugButton.disabled = false;
                debugButton.textContent = '🔍 Debug: Force Fact Check';
                
                // Clear status after 8 seconds
                setTimeout(() => {
                    debugStatus.textContent = '';
                }, 8000);
            });
        } catch (error) {
            debugStatus.textContent = `❌ Error: ${error.message}`;
            debugStatus.style.color = '#ef4444';
            debugButton.disabled = false;
            debugButton.textContent = '🔍 Debug: Force Fact Check';
        }
    });
    
    // Hover effect for debug button
    debugButton.addEventListener('mouseenter', () => {
        if (!debugButton.disabled) {
            debugButton.style.backgroundColor = '#f59e0b';
        }
    });
    debugButton.addEventListener('mouseleave', () => {
        if (!debugButton.disabled) {
            debugButton.style.backgroundColor = '#d97706';
        }
    });
});
