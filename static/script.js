document.getElementById('send-btn').addEventListener('click', sendMessage);

function sendMessage() {
    const input = document.getElementById('user-input');
    const msg = input.value.trim();
    if (!msg) return;

    appendMessage('user', msg);
    input.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage('ai', data.reply);
    })
    .catch(err => appendMessage('ai', "Server Down hai!"));
}

function appendMessage(sender, text) {
    const box = document.getElementById('chat-box');
    const div = document.createElement('div');
    div.className = `msg ${sender}`;
    div.innerText = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
body {
    margin:0;
    font-family:sans-serif;
    background:#0f172a;
    color:white;
    display:flex;
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

sendBtn.addEventListener('click', () => {
    const msg = userInput.value.trim();
    if (!msg) return;

    appendMsg('user', msg);
    userInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => appendMsg('ai', data.reply))
    .catch(() => appendMsg('ai', "Server thak gaya hai!"));
});

function appendMsg(sender, text) {
    const div = document.createElement('div');
    div.className = `msg ${sender}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}
    flex-direction:column;
    height:100vh;
}

/* HEADER */
.header {
    padding:12px;
    background:#020617;
    flex-shrink:0;
}

/* CHAT AREA */
#chat {
    flex:1;
    overflow-y:auto;
    padding:10px;
    display:flex;
    flex-direction:column;
}

/* MESSAGES */
.msg {
    padding:10px;
    margin:6px;
    border-radius:12px;
    max-width:75%;
    word-wrap:break-word;
}

.user {
    background:#22c55e;
    margin-left:auto;
}

.bot {
    background:#1e293b;
}

/* FOOTER INPUT */
.footer {
    display:flex;
    padding:10px;
    background:#020617;
    flex-shrink:0;
}

input {
    flex:1;
    padding:12px;
    border-radius:20px;
    border:none;
    outline:none;
}

button {
    margin-left:5px;
    padding:10px 14px;
    background:#22c55e;
    color:white;
    border:none;
    border-radius:20px;
    }
