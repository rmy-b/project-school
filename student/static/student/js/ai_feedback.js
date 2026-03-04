function sendMessage() {

    const inputField = document.getElementById("user-input");
    const userMessage = inputField.value.trim();

    if (!userMessage) return;

    const chatBox = document.getElementById("chat-box");

    // Show user message
    const userMsg = document.createElement("div");
    userMsg.classList.add("message", "user");
    userMsg.innerText = userMessage;
    chatBox.appendChild(userMsg);

    inputField.value = "";

    fetch("/student/ai-response/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {

        const botMsg = document.createElement("div");
        botMsg.classList.add("message", "bot");
        botMsg.innerText = data.reply;
        chatBox.appendChild(botMsg);

        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: "smooth"
        });
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("user-input");

    inputField.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});