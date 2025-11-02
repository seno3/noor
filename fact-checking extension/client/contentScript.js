
if (window.__islamicTruthVerifierLoaded) {
    console.log('⚠️ Script already loaded, skipping re-execution');
    if (typeof chrome !== 'undefined' && chrome.runtime) {
        console.log('✅ Script already initialized');
    }
} else {
    window.__islamicTruthVerifierLoaded = true;
    
    console.log('🛡️ Islamic Truth Verifier extension loaded');

    function getCaptions() {
        const captions = document.querySelector('.caption-window');
        return captions ? captions.innerText.trim() : '';
    }

    let accumulatedCaptions = '';
    let pendingCaptions = '';
    let lastRequestTime = 0;
    let lastPopupTime = 0;
    let isFactCheckPending = false;
    const MIN_REQUEST_INTERVAL = 2000;
    const MIN_POPUP_INTERVAL = 30000;
    const MAX_WORD_COUNT = 30;
    const POPUP_DURATION = 60000;

    function countWords(text) {
        return text.split(/\s+/).filter(word => word.length > 0).length;
    }
    
    function hashText(text) {
        const normalized = text.toLowerCase().replace(/\s+/g, ' ').trim().substring(0, 100);
        let hash = 0;
        for (let i = 0; i < normalized.length; i++) {
            const char = normalized.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return hash.toString();
    }
    
    function hasIslamicKeywordsQuick(text) {
        const textLower = text.toLowerCase();
        const islamicKeywords = [
            'prophet', 'messenger', 'rasul', 'muhammad', 'pbuh',
            'hadith', 'sunna', 'sunnah', 'ahadith',
            'quran', 'qur\'an', 'surah', 'ayah', 'verse',
            'allah', 'god', 'subhanallah', 'inshallah', 'alhamdulillah',
            'companions', 'sahaba', 'sahabah',
            'islam', 'muslim', 'islamic',
            'halal', 'haram', 'wajib', 'mustahabb',
            'prayer', 'salah', 'namaz', 'dua',
            'fiqh', 'sharia', 'shariah', 'madhhab'
        ];
        return islamicKeywords.some(keyword => textLower.includes(keyword));
    }

    function trimToMaxWords(text) {
        const words = text.split(/\s+/).filter(word => word.length > 0);
        if (words.length <= MAX_WORD_COUNT) {
            return text;
        }
        return words.slice(-(MAX_WORD_COUNT)).join(' ');
    }

    let currentPopupElement = null;
    let currentTaskId = null;
    let lastCheckedText = '';
    let checkedTextHashes = new Set();
    const MAX_CHECKED_HASHES = 10;

    async function pollComprehensiveResult(taskId, maxAttempts = 60, interval = 2000) {
        console.log(`🔄 Starting to poll for comprehensive result (task_id: ${taskId})`);
        
        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            try {
                const response = await fetch(`http:
                
                if (!response.ok) {
                    console.error(`❌ Polling failed: HTTP ${response.status}`);
                    continue;
                }
                
                const data = await response.json();
                
                if (data.status === 'completed') {
                    console.log('✅ Comprehensive result received!');
                    if (currentPopupElement && currentPopupElement.parentElement) {
                        showFactCheckPopup(data.result, data.result.claim, false);
                        const oldPopup = document.querySelector('.islamic-fact-check-popup');
                        if (oldPopup && oldPopup !== currentPopupElement) {
                            oldPopup.remove();
                        }
                    }
                    return data.result;
                } else if (data.status === 'error') {
                    console.error('❌ Comprehensive analysis failed:', data.error);
                    if (currentPopupElement && currentPopupElement.parentElement) {
                        const errorDiv = currentPopupElement.querySelector('.comprehensive-status');
                        if (errorDiv) {
                            errorDiv.innerHTML = `<div style="color: #ef4444; margin-top: 10px;">❌ Comprehensive analysis failed: ${data.error}</div>`;
                        }
                    }
                    return null;
                } else {
                    console.log(`⏳ Attempt ${attempt + 1}/${maxAttempts}: Still processing...`);
                    if (currentPopupElement && currentPopupElement.parentElement) {
                        const statusDiv = currentPopupElement.querySelector('.comprehensive-status');
                        if (statusDiv) {
                            statusDiv.innerHTML = `<div style="margin-top: 10px; font-size: 12px; opacity: 0.8;">🔄 Comprehensive analysis in progress... (${attempt + 1}/${maxAttempts})</div>`;
                        }
                    }
                }
                
                await new Promise(resolve => setTimeout(resolve, interval));
            } catch (error) {
                console.error(`❌ Polling error (attempt ${attempt + 1}):`, error);
                await new Promise(resolve => setTimeout(resolve, interval));
            }
        }
        
        console.warn('⚠️ Polling timeout - comprehensive result not received');
        if (currentPopupElement && currentPopupElement.parentElement) {
            const statusDiv = currentPopupElement.querySelector('.comprehensive-status');
            if (statusDiv) {
                statusDiv.innerHTML = `<div style="margin-top: 10px; font-size: 12px; color: #f59e0b;">⏱️ Comprehensive analysis taking longer than expected...</div>`;
            }
        }
        return null;
    }

    async function performFactCheck(text) {
        console.log('🎯 performFactCheck called with text:', text?.substring(0, 50) + '...');
        console.log('📍 document.body:', !!document.body);
        console.log('📍 isFactCheckPending:', isFactCheckPending);
        
        if (isFactCheckPending) {
            console.log('⏳ Fact check already pending, skipping...');
            showErrorPopup('A fact check is already in progress. Click the extension icon and use "Reset" button if stuck.', '⏳ Please Wait');
            return;
        }

        isFactCheckPending = true;
        const quickURL = 'http:
        const TIMEOUT_MS = 30000;
        
        console.log('\n🔄 ============================================================');
        console.log('📤 PERFORMING TWO-PHASE FACT CHECK');
        console.log('============================================================');
        console.log('📝 Text:', text);
        console.log('📊 Words:', countWords(text));
        console.log('🔗 Quick URL:', quickURL);
        console.log('📍 document.body exists:', !!document.body);
        console.log('============================================================\n');

        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => {
                console.warn('⏱️ Quick check timeout (silent - no popup)');
                isFactCheckPending = false;
                reject(new Error('SILENT_TIMEOUT'));
            }, TIMEOUT_MS);
        });

        try {
            console.log('⚡ Phase 1: Quick authenticity check...');
            const quickFetchPromise = fetch(quickURL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    claim: text,
                    claim_type: null
                })
            });
            
            const quickResponse = await Promise.race([quickFetchPromise, timeoutPromise]);

            if (!quickResponse.ok) {
                let errorMessage = `HTTP ${quickResponse.status} Error`;
                try {
                    const errorData = await quickResponse.json();
                    errorMessage = errorData.detail || errorData.message || errorMessage;
                    
                    if (quickResponse.status === 404) {
                        errorMessage = `Endpoint not found (404). The server may need to be restarted to load the new quick-check endpoint. Try restarting the server.`;
                    }
                } catch (e) {
                    errorMessage = quickResponse.statusText || errorMessage;
                    if (quickResponse.status === 404) {
                        errorMessage = `Endpoint not found (404). Please restart the server to load the new endpoints.`;
                    }
                }
                throw new Error(errorMessage);
            }

            const quickData = await quickResponse.json();
            console.log('✅ Quick result received:', quickData);
            
            if (quickData.status === 'skipped' || quickData.quick_result.verdict === 'Not Islamic Content') {
                console.log('⏭️ Non-Islamic content detected - skipping verification silently');
                isFactCheckPending = false;
                accumulatedCaptions = '';
                pendingCaptions = '';
                return;
            }
            
            const quickResult = {
                verdict: quickData.quick_result.verdict,
                confidence: quickData.quick_result.confidence,
                explanation: quickData.quick_result.quick_analysis,
                is_quick: true
            };
            
            try {
                lastPopupTime = Date.now();
                showFactCheckPopup(quickResult, text, true);
                console.log('✅ Quick popup shown');
            } catch (popupError) {
                console.error('❌ Error showing quick popup:', popupError);
            }
            
            if (quickData.task_id) {
                currentTaskId = quickData.task_id;
                console.log(`🔄 Phase 2: Starting to poll for comprehensive result (task_id: ${currentTaskId})`);
                
                pollComprehensiveResult(currentTaskId).then((comprehensiveResult) => {
                    isFactCheckPending = false;
                    if (comprehensiveResult) {
                        console.log('✅ Comprehensive analysis completed and popup updated');
                    }
                    accumulatedCaptions = '';
                    pendingCaptions = '';
                }).catch((error) => {
                    console.error('❌ Error polling comprehensive result:', error);
                    isFactCheckPending = false;
                });
            } else {
                isFactCheckPending = false;
                accumulatedCaptions = '';
                pendingCaptions = '';
            }
            
            
        } catch (error) {
            console.error('❌ Error performing fact check:', error);
            isFactCheckPending = false;
            
            if (error.message === 'SILENT_TIMEOUT' || error.message.includes('timeout') || error.message.includes('Timeout')) {
                console.warn('⚠️ Request timed out silently - no popup shown');
                return;
            }
            
            let errorMessage = error.message || 'Unknown error occurred';
            let errorTitle = '⚠️ Verification Error';
            
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                errorTitle = '🔌 Connection Error';
                errorMessage = 'Cannot connect to server. Make sure the server is running on localhost:8004';
            } else if (error.message.includes('Ollama') || error.message.includes('ollama')) {
                errorTitle = '🤖 Ollama Error';
                errorMessage = `${error.message}<br><br><strong>To fix:</strong><br>1. Run: <code>ollama serve</code><br>2. Pull model: <code>ollama pull mistral</code>`;
            } else if (error.message.includes('HTTP 503')) {
                errorTitle = '⚠️ Service Unavailable';
                errorMessage = 'Service unavailable. The server may be initializing or Ollama is not running.';
            } else if (error.message.includes('HTTP 500')) {
                errorTitle = '⚠️ Server Error';
                errorMessage = `Server error: ${error.message}<br><br>Check server logs for details.`;
            }
            
            showErrorPopup(errorMessage, errorTitle);
        }
    }

    function injectStyles() {
        const styleSheet = document.createElement("style");
        styleSheet.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            .islamic-fact-check-popup {
                position: fixed !important;
                bottom: 20px !important;
                right: 20px !important;
                background: linear-gradient(135deg, #065f46 0%, #047857 100%) !important;
                border: 3px solid #d97706 !important;
                border-radius: 12px;
                padding: 15px;
                z-index: 999999 !important;
                max-width: 350px;
                max-height: 500px;
                overflow-y: auto;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.4;
                color: white !important;
                backdrop-filter: blur(5px);
                animation: slideIn 0.3s ease-out;
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                pointer-events: auto !important;
            }

            .fact-check-title {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
                color: #fbbf24;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .fact-check-claim {
                font-style: italic;
                margin-bottom: 12px;
                padding: 8px;
                background-color: rgba(255,255,255,0.1);
                border-radius: 6px;
                border-left: 4px solid #fbbf24;
            }

            .fact-check-verdict {
                margin-bottom: 10px;
                padding: 8px 12px;
                border-radius: 8px;
                display: inline-block;
                font-weight: bold;
            }

            .verdict-authentic {
                background-color: #10b981;
                color: white;
            }

            .verdict-likely-authentic {
                background-color: #34d399;
                color: white;
            }

            .verdict-likely-fabricated {
                background-color: #f59e0b;
                color: white;
            }

            .verdict-fabricated {
                background-color: #ef4444;
                color: white;
            }

            .verdict-unable {
                background-color: #6b7280;
                color: white;
            }

            .hadith-grade {
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                margin-left: 8px;
                display: inline-block;
            }

            .grade-sahih {
                background-color: #10b981;
            }

            .grade-hasan {
                background-color: #3b82f6;
            }

            .grade-daif {
                background-color: #f59e0b;
            }

            .grade-mawdu {
                background-color: #ef4444;
            }

            .fact-check-warning {
                background-color: rgba(239, 68, 68, 0.2);
                border: 2px solid #ef4444;
                padding: 10px;
                border-radius: 8px;
                margin-top: 10px;
                font-size: 13px;
            }

            .quran-verse {
                background-color: rgba(255,255,255,0.15);
                padding: 10px;
                border-radius: 8px;
                margin-top: 10px;
                font-size: 13px;
            }

            .arabic-text {
                direction: rtl;
                text-align: right;
                font-size: 18px;
                margin: 8px 0;
                font-family: 'Arabic Typesetting', 'Times New Roman', serif;
            }

            .fact-check-link {
                display: inline-block;
                margin-top: 8px;
                color: #fbbf24;
                text-decoration: none;
                font-weight: 500;
                transition: color 0.3s;
            }

            .fact-check-link:hover {
                color: #fcd34d;
                text-decoration: underline;
            }

            .confidence-score {
                font-size: 12px;
                opacity: 0.9;
                margin-top: 5px;
                margin-left: 8px;
            }

            .islamic-fact-check-popup code {
                background-color: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: #fbbf24;
            }

            .islamic-fact-check-popup strong {
                font-weight: bold;
                color: #fcd34d;
            }
        `;
        document.head.appendChild(styleSheet);
    }

    injectStyles();

    function showFactCheckPopup(result, originalText, isQuick = false, existingPopupElement = null) {
        console.log('🎯 showFactCheckPopup called');
        console.log('📍 isQuick:', isQuick);
        console.log('📍 existingPopupElement:', !!existingPopupElement);
        console.log('📍 document:', !!document);
        console.log('📍 document.body:', !!document.body);
        console.log('📍 result:', result);

        let popup = existingPopupElement;

        if (!popup) {
            const existingPopup = document.querySelector('.islamic-fact-check-popup');
            if (existingPopup) {
                console.log('🗑️ Removing existing popup');
                existingPopup.remove();
            }

            if (!document.body) {
                console.error('❌ document.body not found! Waiting...');
                setTimeout(() => {
                    console.log('🔄 Retrying showFactCheckPopup, document.body:', !!document.body);
                    showFactCheckPopup(result, originalText, isQuick, existingPopupElement);
                }, 100);
                return;
            }
            
            console.log('✅ document.body exists, creating popup element');
            popup = document.createElement('div');
            popup.className = 'islamic-fact-check-popup';
            
            popup.style.position = 'fixed';
            popup.style.bottom = '20px';
            popup.style.right = '20px';
            popup.style.zIndex = '999999';
            popup.style.display = 'block';
            popup.style.visibility = 'visible';
            
            document.body.appendChild(popup);
            currentPopupElement = popup;
        }

        const verdict = result.verdict || 'Unable to Verify';
        const grade = result.grade;
        const confidence = result.confidence ? Math.round(result.confidence * 100) : 0;
        
        let verdictClass = 'verdict-unable';
        if (verdict === 'Authentic' || verdict === 'Likely Authentic') {
            verdictClass = verdict === 'Authentic' ? 'verdict-authentic' : 'verdict-likely-authentic';
        } else if (verdict === 'Fabricated' || verdict === 'Likely Fabricated') {
            verdictClass = verdict === 'Fabricated' ? 'verdict-fabricated' : 'verdict-likely-fabricated';
        }

        let gradeBadge = '';
        if (grade) {
            const gradeClass = `grade-${grade.toLowerCase().replace("'", '')}`;
            gradeBadge = `<span class="hadith-grade ${gradeClass}">${grade}</span>`;
        }

        let html = `
            <div class="fact-check-title">
                🛡️ Islamic Truth Verifier ${isQuick ? '<span style="font-size: 11px; opacity: 0.7;">(Quick Analysis)</span>' : ''}
            </div>
            <div class="fact-check-claim">
                "${originalText.substring(0, 150)}${originalText.length > 150 ? '...' : ''}"
            </div>
            <div>
                <span class="fact-check-verdict ${verdictClass}">${verdict}</span>
                ${gradeBadge}
                <div class="confidence-score">Confidence: ${confidence}%</div>
            </div>
        `;

        if (isQuick) {
            html += `
                <div style="margin-top: 12px; font-size: 13px; opacity: 0.9;">
                    ${result.explanation || result.quick_analysis || 'Quick pattern analysis completed.'}
                </div>
                <div class="comprehensive-status" style="margin-top: 15px; padding: 10px; background-color: rgba(255, 255, 255, 0.1); border-radius: 8px; text-align: center;">
                    <div style="font-size: 12px; opacity: 0.8;">🔄 Comprehensive analysis in progress...</div>
                    <div style="font-size: 11px; opacity: 0.6; margin-top: 5px;">This may take 20-120 seconds</div>
                </div>
            `;
        } else {
            if (result.warnings && result.warnings.length > 0) {
                html += `<div class="fact-check-warning">⚠️ ${result.warnings[0]}</div>`;
            }

            const quranVerses = result.islamic_verification?.quran_verses || [];
            if (quranVerses.length > 0) {
                const verse = quranVerses[0];
                html += `
                    <div class="quran-verse">
                        <strong>📖 ${verse.surah_name} ${verse.ayah}</strong>
                        ${verse.arabic_text ? `<div class="arabic-text">${verse.arabic_text}</div>` : ''}
                        <div>${verse.translation}</div>
                    </div>
                `;
            }

            const hadiths = result.islamic_verification?.hadiths || [];
            if (hadiths.length > 0) {
                const hadith = hadiths[0];
                html += `
                    <div class="quran-verse">
                        <strong>📜 Hadith (${hadith.collection || 'Unknown'})</strong>
                        <div>Grade: ${hadith.grade}</div>
                        <div>${hadith.text.substring(0, 100)}...</div>
                    </div>
                `;
            }

            if (result.explanation) {
                html += `<div style="margin-top: 12px; font-size: 13px; opacity: 0.9;">${result.explanation.substring(0, 300)}${result.explanation.length > 300 ? '...' : ''}</div>`;
            }

            if (result.sources && result.sources.length > 0) {
                const source = result.sources[0];
                html += `<a href="${source.url}" target="_blank" class="fact-check-link">Read Full Source</a>`;
            }
        }

        popup.innerHTML = html;
        
        if (!existingPopupElement) {
            document.body.appendChild(popup);
        }
        
        console.log('✅ Popup appended to body');
        console.log('📍 Popup element:', popup);
        console.log('📍 Popup in DOM:', document.body.contains(popup));
        console.log('📍 Popup computed style display:', window.getComputedStyle(popup).display);
        console.log('📍 Popup computed style visibility:', window.getComputedStyle(popup).visibility);
        console.log('📍 Popup computed style position:', window.getComputedStyle(popup).position);
        console.log('📍 Popup computed style z-index:', window.getComputedStyle(popup).zIndex);
        console.log('📍 Popup computed style bottom:', window.getComputedStyle(popup).bottom);
        console.log('📍 Popup computed style right:', window.getComputedStyle(popup).right);
        
        setTimeout(() => {
            if (popup.parentElement) {
                popup.style.setProperty('display', 'block', 'important');
                popup.style.setProperty('visibility', 'visible', 'important');
                popup.style.setProperty('opacity', '1', 'important');
                popup.style.setProperty('z-index', '999999', 'important');
                console.log('🔧 Forced popup visibility styles applied');
            }
        }, 50);

        setTimeout(() => {
            if (popup && popup.parentElement) {
                console.log(`⏰ Removing popup after ${POPUP_DURATION/1000} seconds`);
                popup.remove();
            }
        }, POPUP_DURATION);
        
        popup.addEventListener('click', () => {
            console.log('👆 Popup clicked, removing...');
            popup.remove();
        });
    }

    function showErrorPopup(message, title = '⚠️ Verification Error') {
        console.log('⚠️ Showing error popup:', message);
        
        const existingPopup = document.querySelector('.islamic-fact-check-popup');
        if (existingPopup) {
            console.log('🗑️ Removing existing popup');
            existingPopup.remove();
        }

        if (!document.body) {
            console.error('❌ document.body not found!');
            setTimeout(() => showErrorPopup(message, title), 100);
            return;
        }

        const popup = document.createElement('div');
        popup.className = 'islamic-fact-check-popup';
        
        popup.style.position = 'fixed';
        popup.style.bottom = '20px';
        popup.style.right = '20px';
        popup.style.zIndex = '999999';
        popup.style.display = 'block';
        popup.style.visibility = 'visible';
        
        const displayMessage = message.includes('<br>') || message.includes('<code>') 
            ? message 
            : message.replace(/\n/g, '<br>').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        
        popup.innerHTML = `
            <div class="fact-check-title">${title}</div>
            <div class="fact-check-claim" style="color: #fca5a5; white-space: pre-wrap;">
                ${displayMessage}
            </div>
            <div class="fact-check-verdict verdict-unable" style="margin-top: 10px;">
                Unable to Verify
            </div>
            ${!message.includes('Ollama') ? `
            <div style="margin-top: 12px; font-size: 13px; opacity: 0.9;">
                Please check that:
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li>The server is running on localhost:8004</li>
                    <li>Ollama is running (if using Ollama)</li>
                    <li>Your internet connection is active</li>
                </ul>
            </div>
            ` : ''}
        `;
        
        document.body.appendChild(popup);
        
        console.log('✅ Error popup appended to body, should be visible on screen');
        console.log('📍 Position: bottom-right corner');

        setTimeout(() => {
            if (popup && popup.parentElement) {
                console.log('⏰ Removing error popup after duration');
                popup.remove();
            }
        }, 10000);
        
        popup.addEventListener('click', () => {
            console.log('👆 Error popup clicked, removing...');
            popup.remove();
        });
    }

    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        console.log('📨 Message received:', request.type);
        
        if (request.type === 'PING') {
            sendResponse({ success: true, ready: true, timestamp: Date.now() });
            return true;
        }
        
        if (request.type === 'RESET_FACT_CHECK') {
            console.log('🔄 RESET_FACT_CHECK message received');
            try {
                isFactCheckPending = false;
                accumulatedCaptions = '';
                pendingCaptions = '';
                lastCheckedText = '';
                checkedTextHashes.clear();
                lastPopupTime = 0;
                console.log('✅ Fact check flag and captions reset');
                
                if (sendResponse) {
                    sendResponse({ success: true, message: 'Fact check reset successfully' });
                }
            } catch (error) {
                console.error('❌ Error in reset handler:', error);
                if (sendResponse) {
                    sendResponse({ success: false, message: error.message });
                }
            }
            return true;
        }
        
        if (request.type === 'DEBUG_FACT_CHECK') {
            console.log('\n🔧 ============================================================');
            console.log('🔧 DEBUG FACT CHECK TRIGGERED FROM POPUP');
            console.log('============================================================');
            
            if (isFactCheckPending) {
                console.log('⚠️ Flag was stuck, resetting it...');
                isFactCheckPending = false;
            }
            
            let factCheckText = '';
            
            const currentCaption = getCaptions();
            if (currentCaption && currentCaption.trim().length > 0) {
                factCheckText = currentCaption.trim();
                console.log('✅ Using current caption from video');
            } 
            else if (accumulatedCaptions && accumulatedCaptions.trim().length > 0) {
                factCheckText = accumulatedCaptions.trim();
                console.log('✅ Using accumulated captions');
            }
            else if (pendingCaptions && pendingCaptions.trim().length > 0) {
                factCheckText = pendingCaptions.trim();
                console.log('✅ Using pending captions');
            }
            else {
                factCheckText = request.testText || 'The Prophet Muhammad said peace be upon him that Islam is the final religion. In Surah 2:255 Allah mentions the Throne Verse.';
                console.log('⚠️ No captions available, using test text');
            }
            
            if (countWords(factCheckText) < 3) {
                factCheckText = request.testText || 'The Prophet Muhammad said peace be upon him that Islam is the final religion. In Surah 2:255 Allah mentions the Throne Verse.';
                console.log('⚠️ Caption too short, using test text');
            }
            
            console.log('📝 Text to check:', factCheckText.substring(0, 100) + '...');
            console.log('📊 Words:', countWords(factCheckText));
            console.log('📍 document.body exists:', !!document.body);
            console.log('============================================================\n');
            
            console.log('🎬 Creating checking popup...');
            console.log('📍 document.body:', !!document.body);
            
            if (!document.body) {
                console.error('❌ Cannot show popup: document.body does not exist!');
                sendResponse({ success: false, message: 'Page not ready. Please refresh the page.' });
                return false;
            }
            
            const checkingPopup = document.createElement('div');
            checkingPopup.className = 'islamic-fact-check-popup';
            checkingPopup.style.cssText = `
                position: fixed !important;
                bottom: 20px !important;
                right: 20px !important;
                z-index: 999999 !important;
                display: block !important;
                visibility: visible !important;
                opacity: 1 !important;
                background: linear-gradient(135deg, #065f46 0%, #047857 100%) !important;
                border: 3px solid #d97706 !important;
                border-radius: 12px !important;
                padding: 15px !important;
                max-width: 350px !important;
                color: white !important;
                font-family: 'Segoe UI', Arial, sans-serif !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            `;
            checkingPopup.innerHTML = `
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px; color: #fbbf24;">🔄 Checking...</div>
                <div style="font-style: italic; margin-bottom: 12px;">Verifying claim with server...</div>
            `;
            
            try {
                document.body.appendChild(checkingPopup);
                console.log('✅ Checking popup appended to body');
                console.log('📍 Checking popup in DOM:', document.body.contains(checkingPopup));
            } catch (appendError) {
                console.error('❌ Failed to append checking popup:', appendError);
                sendResponse({ success: false, message: 'Failed to show popup: ' + appendError.message });
                return false;
            }
            
            performFactCheck(factCheckText)
                .then(() => {
                    console.log('✅ performFactCheck completed successfully');
                    if (checkingPopup && checkingPopup.parentElement) {
                        checkingPopup.remove();
                    }
                    if (sendResponse) {
                        sendResponse({ success: true, message: 'Fact check completed' });
                    }
                })
                .catch((error) => {
                    console.error('❌ performFactCheck error:', error);
                    if (checkingPopup && checkingPopup.parentElement) {
                        checkingPopup.remove();
                    }
                    if (sendResponse) {
                        sendResponse({ success: false, message: error.message });
                    }
                });
            
            return true;
        }
    });

    setInterval(() => {
        const newCaption = getCaptions();
        const currentTime = Date.now();
        
        if (newCaption) {
            pendingCaptions += ' ' + newCaption;
            pendingCaptions = pendingCaptions.trim();
            console.log('📝 New caption captured:', {
                caption: newCaption,
                pendingCaptions: pendingCaptions
            });
        }
        
        if (currentTime - lastRequestTime >= MIN_REQUEST_INTERVAL) {
            lastRequestTime = currentTime;
            
            if (pendingCaptions) {
                if (accumulatedCaptions) {
                    accumulatedCaptions += ' ' + pendingCaptions;
                } else {
                    accumulatedCaptions = pendingCaptions;
                }
                pendingCaptions = '';
            }

            if (countWords(accumulatedCaptions) > MAX_WORD_COUNT) {
                accumulatedCaptions = trimToMaxWords(accumulatedCaptions);
            }

            const hasQuickIslamicCheck = hasIslamicKeywordsQuick(accumulatedCaptions);
            
            const timeSinceLastPopup = currentTime - lastPopupTime;
            const canShowNewPopup = timeSinceLastPopup >= MIN_POPUP_INTERVAL;
            
            const existingPopupVisible = document.querySelector('.islamic-fact-check-popup') !== null;
            
            const textHash = hashText(accumulatedCaptions);
            const textIsNew = !checkedTextHashes.has(textHash);
            
            if (!isFactCheckPending && accumulatedCaptions && countWords(accumulatedCaptions) >= MAX_WORD_COUNT && 
                canShowNewPopup && !existingPopupVisible && textIsNew && hasQuickIslamicCheck) {
                lastPopupTime = currentTime;
                lastCheckedText = accumulatedCaptions;
                checkedTextHashes.add(textHash);
                
                if (checkedTextHashes.size > MAX_CHECKED_HASHES) {
                    const firstHash = Array.from(checkedTextHashes)[0];
                    checkedTextHashes.delete(firstHash);
                }
                
                performFactCheck(accumulatedCaptions);
            } else if (!isFactCheckPending && accumulatedCaptions && countWords(accumulatedCaptions) >= MAX_WORD_COUNT) {
                if (!hasQuickIslamicCheck) {
                    accumulatedCaptions = '';
                    pendingCaptions = '';
                } else if (!canShowNewPopup) {
                    console.log(`⏸️ Skipping fact check - only ${Math.round(timeSinceLastPopup/1000)}s since last popup (need ${MIN_POPUP_INTERVAL/1000}s)`);
                } else if (existingPopupVisible) {
                    console.log(`⏸️ Skipping fact check - popup already visible`);
                } else if (!textIsNew) {
                    console.log(`⏸️ Skipping fact check - duplicate text (hash: ${textHash})`);
                }
            }
        }
    }, 1000);

    console.log('✅ Extension script initialized and running!');
    console.log('📺 Looking for YouTube captions...');
    console.log('⚠️  IMPORTANT: Make sure captions/subtitles are ENABLED on the video!');
}
