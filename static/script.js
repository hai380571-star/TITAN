// Elements ko pakadna
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

// Message bhejne ka main function
async function sendMessage() {
    const msg = userInput.value.trim();
    if (!msg) return;

    console.log("Sending message:", msg); // Browser console mein check karne ke liye

    // 1. User ka message turant screen pe dikhao
    appendMsg('user', msg);
    userInput.value = ''; // Box khali karo

    try {
        // 2. Python Backend se baat karo
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg })
        });

        const data = await response.json();
        
        // 3. AI ka jawab dikhao
        if (data.reply) {
            appendMsg('ai', data.reply);
        } else {
            appendMsg('ai', "Error: AI ne kuch nahi bola.");
        }

    } catch (error) {
        console.error("Fetch Error:", error);
        appendMsg('ai', "Server Connection Fail! Render Logs check karo.");
    }
}

// Button Click Event
sendBtn.addEventListener('click', sendMessage);

// Enter Key Event (BCA Pro Tip)
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Screen pe message add karne ka function
function appendMsg(sender, text) {
    const div = document.createElement('div');
    div.className = `msg ${sender}`;
    div.innerText = text;
    chatBox.appendChild(div);
    
    // Auto Scroll niche tak
    chatBox.scrollTop = chatBox.scrollHeight;
}
