document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("sendButton");
    const introBox = document.getElementById("intro"); // Select the intro box
    const fillerBox = document.getElementById("fillerBox"); // Select the loading message box
    const promptInput = document.getElementById("prompt"); // Select the input box
    const responseDiv = document.getElementById("response"); // Select the response box

    // Click event for the Submit button
    sendButton.addEventListener("click", function () {
        submitPrompt();
    });

    // **Listen for "Enter" key press inside the input field**
    promptInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) { 
            event.preventDefault(); // **Prevents adding a new line in the textarea**
            submitPrompt();
        }
    });

    function submitPrompt() {
        let promptText = promptInput.value.trim();

        // **🔹 If empty, use the default message**
        if (!promptText) {
            promptText = "Where can I get help with senior housing assistance?";
            promptInput.value = promptText; // Update the input field with the default
        }

        if (introBox) {
            introBox.classList.add("hidden"); // Hide the intro box
        }
        if (fillerBox) {
            fillerBox.classList.remove("hidden"); // Show the loading message
        }

        sendPrompt(promptText);
    }
});

async function sendPrompt(prompt) {
    let responseDiv = document.getElementById("response");
    let fillerBox = document.getElementById("fillerBox"); // Select the loading message box

    responseDiv.innerHTML = ""; // Clear previous response
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
