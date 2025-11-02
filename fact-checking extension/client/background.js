// background.js - Islamic Truth Verifier Background Service Worker

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'CHECK_SERVER_STATUS') {
        // Check if backend server is available
        fetch('http://localhost:8004/health', { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                sendResponse({ status: 'online', data: data });
            })
            .catch(() => {
                sendResponse({ status: 'offline' });
            });
        return true; // Keep channel open for async response
    }
    
    // Forward settings changes to content scripts
    if (request.type === 'SETTING_CHANGED') {
        chrome.tabs.query({}, (tabs) => {
            tabs.forEach(tab => {
                chrome.tabs.sendMessage(tab.id, {
                    type: 'SETTING_CHANGED',
                    enableFactCheck: request.enableFactCheck
                }).catch(() => {
                    // Ignore errors for tabs without content script
                });
            });
        });
    }
});

// Handle extension installation
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        // Set default settings
        chrome.storage.sync.set({ enableFactCheck: true });
        console.log('Islamic Truth Verifier extension installed');
    }
});
