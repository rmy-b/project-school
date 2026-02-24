function sendMessage(action) {

    const chatBox = document.getElementById("chat-box");

    // Remove previous buttons
    const existingOptions = document.querySelector(".options");
    if (existingOptions) {
        existingOptions.remove();
    }

    // Show user message
    const userMsg = document.createElement("div");
    userMsg.classList.add("message", "user");
    userMsg.innerText = action.replace("_", " ").toUpperCase();
    chatBox.appendChild(userMsg);

    fetch("/student/ai-response/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {

        const botMsg = document.createElement("div");
        botMsg.classList.add("message", "bot");
        botMsg.innerText = data.message;
        chatBox.appendChild(botMsg);

        if (data.next_level === "actions") {
            showActionButtons();
        }

        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function showActionButtons() {

    const chatBox = document.getElementById("chat-box");

    const optionsDiv = document.createElement("div");
    optionsDiv.classList.add("options");

    optionsDiv.innerHTML = `
        <button onclick="sendMessage('study_plan')">Generate Study Plan</button>
        <button onclick="sendMessage('analysis')">View Subject Analysis</button>
        <button onclick="sendMessage('tips')">Improvement Tips</button>
    `;

    chatBox.appendChild(optionsDiv);
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