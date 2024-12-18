// API Endpoint for backend
const apiEndpoint = 'https://your-backend-api.com/endpoint';

// Function to send the URL to the backend and inject modal
function sendUrlToBackend(url, tabId) {

  //https://joyfurpets.com/wp-content/uploads/2020/05/vrei-caine-buldog-francez-1.jpg
  //showModalOnPage(tabId, "https://joyfurpets.com/wp-content/uploads/2020/05/vrei-caine-buldog-francez-1.jpg", "" || '#');

      // Check if modals are enabled
      chrome.storage.sync.get(['modalsEnabled'], (result) => {
        if (result.modalsEnabled !== false) { // Default to true if not set
          // Show modal on active tab
          showModalOnPage(tabId, "https://joyfurpets.com/wp-content/uploads/2020/05/vrei-caine-buldog-francez-1.jpg", "" || '#');
        } else {
          console.log('Modal generation is disabled.');
        }
      });

  // // Make API request to send URL
  // fetch(apiEndpoint, {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ url: url }),
  // })
  //   .then((response) => {
  //     if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
  //     return response.json(); // Expect backend to return image URL and optional link
  //   })
  //   .then((data) => {
  //     console.log('Received data from backend:', data);
  //     // Inject the image as a modal (you can swap for bottom or right popup)
  //     showModalOnPage(tabId, data.imageUrl, data.linkUrl || '#');
  //   })
  //   .catch((error) => {
  //     console.error('Error sending URL or receiving image:', error);
  //   });
}

// Function to inject modal popup into a tab
function showModalOnPage(tabId, imageUrl, linkUrl) {
  chrome.scripting.executeScript({
    target: { tabId: tabId },
    func: createPopup, // Generalized popup creation
    args: [imageUrl, linkUrl, 'right'], // Pass popup type ('modal', 'bottom', 'right')
  });
}

// Generalized function to create popups (modal, bottom-fixed, right-fixed)
function createPopup(imageUrl, linkUrl, type) {
  const popupId = `extension-popup-${type}`;
  if (document.getElementById(popupId)) return; // Prevent duplicates

  // Create the container
  const popupContainer = document.createElement('div');
  popupContainer.id = popupId;
  popupContainer.style.position = 'fixed';
  popupContainer.style.zIndex = '9999';
  popupContainer.style.display = 'flex';
  popupContainer.style.justifyContent = 'center';
  popupContainer.style.alignItems = 'center';
  popupContainer.style.padding = '10px';
  popupContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';

  // Position based on type
  if (type === 'modal') {
    popupContainer.style.top = '0';
    popupContainer.style.left = '0';
    popupContainer.style.width = '100vw';
    popupContainer.style.height = '100vh';
  } else if (type === 'bottom') {
    popupContainer.style.bottom = '0';
    popupContainer.style.left = '0';
    popupContainer.style.width = '100%';
  } else if (type === 'right') {
    popupContainer.style.right = '0';
    popupContainer.style.top = '50%';
    popupContainer.style.transform = 'translateY(-50%)';
  }

  // Add image and close button
  const anchor = document.createElement('a');
  anchor.href = linkUrl;
  anchor.target = '_blank';

  const img = document.createElement('img');
  img.src = imageUrl;
  img.style.maxHeight = '350px';
  img.style.cursor = 'pointer';
  img.style.border = '2px solid white';

  anchor.appendChild(img);

  const closeButton = document.createElement('button');
  closeButton.textContent = '×';
  closeButton.style.position = 'absolute';
  closeButton.style.top = '5px';
  closeButton.style.right = '5%';
  closeButton.style.background = 'transparent';
  closeButton.style.color = 'white';
  closeButton.style.border = 'none';
  closeButton.style.fontSize = '4rem';
  closeButton.style.cursor = 'pointer';

  closeButton.addEventListener('click', () => document.body.removeChild(popupContainer));

  popupContainer.appendChild(anchor);
  popupContainer.appendChild(closeButton);
  document.body.appendChild(popupContainer);
}

// Listen for tab activation or update events
chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.get(activeInfo.tabId, (tab) => {
    if (tab.url) sendUrlToBackend(tab.url, activeInfo.tabId);
  });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    sendUrlToBackend(tab.url, tabId);
  }
});
