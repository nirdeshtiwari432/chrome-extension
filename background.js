chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: getDomainFromURL
    });
});

function getDomainFromURL() {
    const url = window.location.href;
    const domain = new URL(url).hostname;

    fetch(`https://dns.google/resolve?name=${domain}&type=A`)
        .then(response => response.json())
        .then(data => {
            if (data.Answer && data.Answer.length > 0) {
                alert(`IP Address of ${domain}: ${data.Answer[0].data}`);
            } else {
                alert(`Could not resolve domain: ${domain}`);
            }
        })
        .catch(error => {
            alert(`Error: ${error.message}`);
        });
}
