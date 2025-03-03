// Automatically detect the current tab's domain
document.addEventListener("DOMContentLoaded", () => {
    const domainInput = document.getElementById("domain");
  
    // Get the active tab's URL
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length > 0) {
        const url = new URL(tabs[0].url);
        const domain = url.hostname; // Get the hostname (e.g., example.com)
        domainInput.value = domain; // Populate the input field
      } else {
        domainInput.value = "Unable to detect domain.";
      }
    });
  });
  
  // Handle the "Check Website" button click
  document.getElementById("check").addEventListener("click", async () => {
    const domain = document.getElementById("domain").value.trim();
    const resultElement = document.getElementById("result");
  
    if (!domain) {
      resultElement.textContent = "Failed to detect a valid domain.";
      return;
    }
  
    try {
      // Fetch the IP using a public DNS resolver
      const ipResponse = await fetch(`https://dns.google/resolve?name=${domain}&type=A`);
      const ipData = await ipResponse.json();
  
      if (!ipData.Answer || !ipData.Answer.length) {
        resultElement.textContent = "Failed to resolve domain IP.";
        return;
      }
  
      const ip = ipData.Answer[0].data;
  
      // Send the domain and IP to your Python backend
      const backendResponse = await fetch("http://127.0.0.1:5000/check-website", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domain, ip })
      });
  
      const backendResult = await backendResponse.json();
      resultElement.textContent = JSON.stringify(backendResult, null, 2);
    } catch (error) {
      console.error(error);
      resultElement.textContent = "Error checking the website.";
    }
  });
  