function toggleChat() {
    var chatWindow = document.getElementById("chat-window");
    if (chatWindow.style.display === "none" || chatWindow.style.display === "") {
        chatWindow.style.display = "flex";
    } else {
        chatWindow.style.display = "none";
    }
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

async function sendMessage() {
    var inputField = document.getElementById("chat-input");
    var message = inputField.value.trim();
    if (message === "") return;

    // Add User Message
    addMessage(message, "user");
    inputField.value = "";

    // Show typing...
    var typingId = addMessage("Thinking...", "bot", true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();

        // Remove typing and add bot response
        removeMessage(typingId);
        addMessage(data.response, "bot");
    } catch (error) {
        removeMessage(typingId);
        addMessage("Sorry, something went wrong.", "bot");
    }
}

function addMessage(text, sender, isTyping = false) {
    var chatBody = document.getElementById("chat-body");
    var msgDiv = document.createElement("div");
    msgDiv.className = "message " + sender;
    msgDiv.innerText = text;
    if (isTyping) msgDiv.id = "typing-" + Date.now();

    chatBody.appendChild(msgDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
    return msgDiv.id;
}

function removeMessage(id) {
    if (!id) return;
    var el = document.getElementById(id);
    if (el) el.remove();
}
