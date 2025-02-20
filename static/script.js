document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("sendButton");
    const introBox = document.getElementById("intro"); // Select the intro box
    const fillerBox = document.getElementById("fillerBox"); // Select the loading message box
    const promptInput = document.getElementById("prompt"); // Select the input box

    // Click event for the Submit button
    sendButton.addEventListener("click", function () {
        submitPrompt();
    });

    // **Listen for "Enter" key press inside the input field**
    promptInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // **Prevents adding a new line in the textarea**
            submitPrompt();
        }
    });

    function submitPrompt() {
        if (introBox) {
            introBox.classList.add("hidden"); // Hide the intro box
        }
        if (fillerBox) {
            fillerBox.classList.remove("hidden"); // Show the loading message
        }
        sendPrompt(); // Call the existing sendPrompt function
    }
});

async function sendPrompt() {
    let prompt = document.getElementById("prompt").value;
    let responseDiv = document.getElementById("response");
    let fillerBox = document.getElementById("fillerBox"); // Select the loading message box

    responseDiv.innerHTML = ""; // Clear previous response

    if (!prompt.trim()) { // **Prevents submission of empty input**
        responseDiv.innerHTML = "<p style='color:red;'>Please enter a message.</p>";
        responseDiv.classList.remove("hidden"); // Show error message
        if (fillerBox) {
            fillerBox.classList.add("hidden"); // Hide loading message if there's an error
        }
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
            if (fillerBox) {
                fillerBox.classList.add("hidden"); // Hide loading message on error
            }
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let completeResponse = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            let chunk = decoder.decode(value, { stream: true });

            // **🔹 Check for "END_RESPONSE" marker but keep response text**
            if (chunk.includes("END_RESPONSE")) {
                chunk = chunk.replace("END_RESPONSE", ""); // **Remove marker but keep text**
                completeResponse += chunk;
                responseDiv.innerHTML = completeResponse; // **Ensure final response is shown**
                break;
            }

            completeResponse += chunk;
            responseDiv.innerHTML = completeResponse; // Update response box
        }

        // **Ensure `fillerBox` is hidden after response completes**
        if (fillerBox) {
            fillerBox.classList.add("hidden");
        }

    } catch (error) {
        responseDiv.innerHTML = `<p style='color:red;'>Error: ${error.message}</p>`;
        if (fillerBox) {
            fillerBox.classList.add("hidden"); // Ensure loading box is hidden on error
        }
    }
}
