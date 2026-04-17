from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

memory = {"lazy": 0, "success": 0}
last_mode = None
CREATOR = "Abdul Hai"

def analyze(text):
    t = (text or "").lower()

    if any(w in t for w in ["kal", "baad me", "nahi karunga"]):
        memory["lazy"] += 1
        return "STRICT"

    elif any(w in t for w in ["done", "kar liya", "complete"]):
        memory["success"] += 1
        return "SOFT"

    elif any(w in t for w in ["masti", "bakchodi", "fun"]):
        return "FUN"

    return "NEUTRAL"


def reply(mode, msg):
    global last_mode
    m = (msg or "").lower()

    # creator hard control
    if any(x in m for x in ["creator", "kisne banaya", "who made you"]):
        return f"Mujhe {CREATOR} ne banaya hai"

    savage_level = "low"
    if memory["lazy"] > 3:
        savage_level = "high"

    prompt = f"""
You are PsychoSense, a psychological AI created by {CREATOR}.

Mode: {mode}
Savage level: {savage_level}

User message: {msg}

User stats:
- Lazy count: {memory['lazy']}
- Success count: {memory['success']}
- Previous mode: {last_mode}

Rules:
- STRICT: direct, calls out excuses
- SOFT: supportive, motivating
- FUN: light, casual
- NEUTRAL: curious, not repetitive

Savage rules:
- If lazy count high, point out pattern
- Light roast allowed but no insults

General rules:
- No emojis
- Short replies (1-2 lines)
- Human-like tone
- Do not repeat same question

Respond naturally:
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80
        )

        last_mode = mode
        return res.choices[0].message.content.strip()

    except Exception as e:
        print("AI ERROR:", e)

        if mode == "STRICT":
            return "Tu delay kar raha hai. Ye pattern ban raha hai."
        elif mode == "SOFT":
            return "Good. Aise hi continue kar."
        elif mode == "FUN":
            return "Chal thoda chill karte hain."
        else:
            return "Seedha bol. Kya chal raha hai?"


HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>PsychoSense AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
    margin:0;
    font-family:sans-serif;
    background:#0f172a;
    color:white;
    display:flex;
    flex-direction:column;
    height:100vh;
}

.header {
    padding:12px;
    background:#020617;
}

#chat {
    flex:1;
    overflow-y:auto;
    padding:10px;
    display:flex;
    flex-direction:column;
}

.msg {
    padding:10px;
    margin:6px;
    border-radius:12px;
    max-width:75%;
}

.user {
    background:#22c55e;
    margin-left:auto;
}

.bot {
    background:#1e293b;
}

.footer {
    display:flex;
    padding:10px;
    background:#020617;
}

input {
    flex:1;
    padding:12px;
    border-radius:20px;
    border:none;
}

button {
    margin-left:5px;
    padding:10px;
    background:#22c55e;
    color:white;
    border:none;
    border-radius:20px;
}
</style>
</head>

<body>

<div class="header">
<b>PsychoSense AI</b><br>
<small>Created by Abdul Hai</small>
</div>

<div id="chat"></div>

<div class="footer">
<input id="input" placeholder="Type your thoughts...">
<button onclick="send()">Send</button>
</div>

<script>
let chat = document.getElementById("chat");

function addMsg(text, type){
    let div = document.createElement("div");
    div.className = "msg " + type;
    div.innerHTML = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function send(){
    let input = document.getElementById("input");
    let msg = input.value;
    if(!msg) return;

    addMsg(msg,"user");
    input.value="";

    let typing = document.createElement("div");
    typing.className = "msg bot";
    typing.innerHTML = "Typing...";
    chat.appendChild(typing);

    try {
        let res = await fetch("/chat",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({ message: msg })
        });

        let data = await res.json();

        typing.remove();
        addMsg(data.reply,"bot");

    } catch(err){
        typing.remove();
        addMsg("Server error","bot");
    }
}
</script>

</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user = data.get("message") or ""

    if not user:
        return jsonify({"reply": "Say something"})

    mode = analyze(user)
    res = reply(mode, user)

    return jsonify({"reply": res})


if __name__ == "__main__":
    app.run()
