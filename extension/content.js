chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === "makeEmojiPasta") {
    const paragraphs = document.getElementsByTagName("p");

    for (let p of paragraphs) {
      const originalText = p.innerText;

      fetch("https://emoji-pasta-maker.fly.dev/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic: originalText }),
      })
        .then((response) => response.json())
        .then((data) => {
          p.innerHTML = data.data;
        })
        .catch((error) => console.error("Error:", error));
    }
  }
});
