document.addEventListener('DOMContentLoaded', () => {
    const toggleCheckbox = document.getElementById('toggle-modal');
  
    // Load the current state from chrome.storage
    chrome.storage.sync.get(['modalsEnabled'], (result) => {
      toggleCheckbox.checked = result.modalsEnabled !== false; // Default is true
    });
  
    // Save the state when the checkbox is toggled
    toggleCheckbox.addEventListener('change', () => {
      chrome.storage.sync.set({ modalsEnabled: toggleCheckbox.checked }, () => {
        console.log('Modal generation is now:', toggleCheckbox.checked ? 'Enabled' : 'Disabled');
      });
    });
  });
  