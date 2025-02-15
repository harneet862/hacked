let currentTab = null;
let startTime = null;

// Helper function to format time as HH:MM:SS
function formatTime(timestamp) {
    const date = new Date(timestamp);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
}

// Helper function to format date as DD/MM/YYYY
function formatDate(timestamp) {
    const date = new Date(timestamp);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
}

// Function to update website time
function updateWebsiteTime() {
    if (currentTab && startTime) {
        let endTime = Date.now();
        let timeSpent = (endTime - startTime) / 1000; // Convert to seconds

        // Only update if time spent is 10 seconds or more
        if (timeSpent >= 10) {
            // Format start time, end time, and date
            const startTimeFormatted = formatTime(startTime);
            const endTimeFormatted = formatTime(endTime);
            const dateFormatted = formatDate(startTime);

            // Create the log entry
            const logEntry = `Updated: ${currentTab}, StartTime: ${startTimeFormatted}, EndTime: ${endTimeFormatted}, Date: ${dateFormatted}\n`;

            // Retrieve existing log from storage
            chrome.storage.local.get(['websiteLog'], (result) => {
                let websiteLog = result.websiteLog || ''; // Initialize if it doesn't exist

                // Append the new log entry
                websiteLog += logEntry;

                // Save the updated log back to storage
                chrome.storage.local.set({ websiteLog }, () => {
                    console.log(logEntry.trim()); // Log to console for debugging
                });
            });
        }
    }
}

// Detect when a new tab is activated
chrome.tabs.onActivated.addListener(activeInfo => {
    chrome.tabs.get(activeInfo.tabId, tab => {
        if (chrome.runtime.lastError || !tab.url || !tab.url.startsWith("http")) {
            return; // Ignore invalid URLs
        }
        updateWebsiteTime();
        currentTab = new URL(tab.url).hostname;
        startTime = Date.now();
    });
});

// Detect when the tab is updated (e.g., new URL)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url && changeInfo.url.startsWith("http")) {
        updateWebsiteTime();
        currentTab = new URL(changeInfo.url).hostname;
        startTime = Date.now();
    }
});

// Detect when the window is closed
chrome.windows.onRemoved.addListener(() => {
    updateWebsiteTime();
});