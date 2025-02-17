let currentTab = null;
let startTime = null;

// Helper function to format time as HH:MM:SS
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-GB'); // HH:MM:SS format
}

// Helper function to format date as DD/MM/YYYY
function formatDate(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-GB').replace(/\//g, '-'); // DD-MM-YYYY format
}

// Function to fetch website metadata (title and description)
function fetchWebsiteMetadata(tabId, callback) {
    chrome.scripting.executeScript({
        target: { tabId: tabId },
        func: () => {
            const title = document.title || 'No title available';
            const description = document.querySelector('meta[name="description"]')?.content || 'No description available';
            return { title, description };
        },
        world: "MAIN"
    }, (results) => {
        if (chrome.runtime.lastError || !results || !results[0]) {
            callback({ title: 'No title available', description: 'No description available' });
        } else {
            callback(results[0].result);
        }
    });
}

// Function to update and store log data
function updateWebsiteTime(tabId, isTabClosed = false, url = null) {
    if (currentTab && startTime) {
        let endTime = Date.now();
        let timeSpent = (endTime - startTime) / 1000; // Convert to seconds

        if (timeSpent >= 10) {
            let logEntry = {
                date: formatDate(startTime),
                startTime: formatTime(startTime),
                endTime: formatTime(endTime),
                title: '',
                description: '',
                url: url || 'No URL available' // Add the URL to the log entry
            };

            fetchWebsiteMetadata(tabId, (metadata) => {
                logEntry.title = metadata.title;
                logEntry.description = metadata.description;

                chrome.storage.local.get(['websiteLog'], (result) => {
                    let websiteLog = result.websiteLog || [];
                    websiteLog.push(logEntry);

                    chrome.storage.local.set({ websiteLog }, () => {
                        console.log("Log stored:", logEntry);
                    });
                });
            });
        }

        if (!isTabClosed) {
            startTime = Date.now();
        } else {
            currentTab = null;
            startTime = null;
        }
    }
}

// Detect when a new tab is activated
chrome.tabs.onActivated.addListener(activeInfo => {
    chrome.tabs.get(activeInfo.tabId, tab => {
        if (chrome.runtime.lastError || !tab.url || !tab.url.startsWith("http")) {
            return;
        }

        if (currentTab && startTime) {
            updateWebsiteTime(activeInfo.tabId, false, tab.url); // Pass the URL here
        }

        currentTab = new URL(tab.url).hostname;
        startTime = Date.now();
    });
});

// Detect when a tab is updated (e.g., new URL)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url && changeInfo.url.startsWith("http")) {
        if (currentTab && startTime) {
            updateWebsiteTime(tabId, false, changeInfo.url); // Pass the URL here
        }

        currentTab = new URL(changeInfo.url).hostname;
        startTime = Date.now();
    }
});

// Detect when a tab is closed
chrome.tabs.onRemoved.addListener((tabId) => {
    if (currentTab && startTime) {
        updateWebsiteTime(tabId, true, currentTab); // Pass the URL here
    }
});

// Detect when a browser window is closed
chrome.windows.onRemoved.addListener(() => {
    if (currentTab && startTime) {
        updateWebsiteTime(null, true, currentTab); // Pass the URL here
    }
});

// Function to download stored logs as a .json file
function downloadLogs() {
    chrome.storage.local.get(['websiteLog'], (result) => {
        let websiteLog = result.websiteLog || [];

        let blob = new Blob([JSON.stringify(websiteLog, null, 2)], { type: "application/json" });
        let url = URL.createObjectURL(blob);

        let downloadElement = document.createElement("a");
        downloadElement.href = url;
        downloadElement.download = "website_log.json";
        document.body.appendChild(downloadElement);
        downloadElement.click();
        document.body.removeChild(downloadElement);

        URL.revokeObjectURL(url);
    });
}

// Add a listener for a message from the popup to trigger download
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "downloadLogs") {
        downloadLogs();
        sendResponse({ status: "Downloading JSON log..." });
    }
});