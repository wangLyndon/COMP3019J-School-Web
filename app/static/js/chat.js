const inputMsg = document.querySelector(".chat .footer textarea");
const chatBody = document.querySelector(".chat .body");
const sendBtn = document.querySelector(".chat .send");
const openBtn = document.querySelector(".openBot");
const chat = document.querySelector(".chat");
const closeBtn = document.querySelector(".chat .header .close");

let isSending = false;

// Deal with user input
inputMsg.addEventListener("keydown", function (e) {
    const message = e.target.value.trim();
    if (e.key === "Enter" && !e.shiftKey && message && !isSending) {
        // Prevent default actions
        e.preventDefault();
        sendMessage(message);
    }
})

sendBtn.addEventListener("click", function () {
    const message = inputMsg.value.trim();
    if (message && !isSending) {
        sendMessage(message);
    }
})

openBtn.addEventListener("click", function () {
    chat.style.display = "block";
    openBtn.style.display = "none";
})

closeBtn.addEventListener("click", function () {
    openBtn.style.display = "block";
    chat.style.display = "none";
})

function searchAi(message, div) {
    let raw = JSON.stringify({
        "messages": [
            {
                "role": "system",
                "content": message
            }
        ],
        "stream": false,
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 1
    });

    let requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "message" : message
        }),
        redirect: "follow"
    };

    fetch("chat", requestOptions)
        .then(response => response.json())
        .then(result => {
                div.querySelector(".text").innerHTML = result.choices[0].message.content.replace(/```.*?\n|```/g, "")
                    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                    .replace(/"/g, "&quot;").replace(/'/g, "&#039;").replace(/\n/g, "<br>")
                // Prevent the returned information from containing HTML or code elements and changing \n to <br>

                isSending = false;
            }
        );
}

function sendMessage(message) {
    // Clear the input
    inputMsg.value = "";

    // Make sure only send one message
    isSending = true;

    // Create user input message
    const fromUser = document.createElement("div");
    fromUser.classList.add("fromUser");
    fromUser.innerHTML = "<div class=\"text\"></div>";
    fromUser.querySelector(".text").textContent = message;
    // Add to chat body
    chatBody.appendChild(fromUser);

    const fromBot = document.createElement("div");
    fromBot.classList.add("fromBotThinking");
    fromBot.innerHTML = "<div class=\"text\"></div>";
    fromBot.querySelector(".text").textContent = "thinking";

    chatBody.appendChild(fromBot);

    searchAi(message, fromBot);
}
