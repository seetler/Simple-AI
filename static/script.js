document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("sendButton");
    const introBox = document.getElementById("intro"); // Select the intro box

    sendButton.addEventListener("click", function () {
        if (introBox) {
            introBox.classList.add("hidden"); // Hide the intro box
        }
        sendPrompt(); // Call the existing sendPrompt function
    });
});

async function sendPrompt() {
    let prompt = document.getElementById("prompt").value;
    let responseDiv = document.getElementById("response");
    responseDiv.innerHTML = ""; // Clear previous response

    if (!prompt) {
        responseDiv.innerHTML = "<p style='color:red;'>Please enter a message.</p>";
        responseDiv.classList.remove("hidden"); // Show error message
        return;
    }

    responseDiv.classList.remove("hidden"); // Make response box visible

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt: prompt })
        });

        if (!response.ok) {
            responseDiv.innerHTML = "<p style='color:red;'>Error: Failed to get a response.</p>";
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            responseDiv.innerHTML += decoder.decode(value);
        }
    } catch (error) {
        responseDiv.innerHTML = `<p style='color:red;'>Error: ${error.message}</p>`;
    }
}
