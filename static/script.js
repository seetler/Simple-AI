document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("sendButton").addEventListener("click", sendPrompt);
});

async function sendPrompt() {
    let prompt = document.getElementById("prompt").value;
    let responseDiv = document.getElementById("response");
    responseDiv.innerHTML = ""; // Clear previous response

    if (!prompt) {
        responseDiv.innerHTML = "<p style='color:red;'>Please enter a message.</p>";
        return;
    }

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
