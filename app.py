from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# ===== MEMORY =====
memory = {"lazy": 0, "success": 0}
history = []
last_mode = None
CREATOR = "Abdul Hai"

# ===== ANALYZE =====
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


# ===== REPLY ENGINE =====
def reply(mode, msg):
    global history, last_mode

    m = (msg or "").lower()

    # save history
    history.append(m)
    if len(history) > 6:
        history.pop(0)

    # creator
    if any(x in m for x in ["creator", "kisne banaya", "who made you"]):
        return "Mujhe " + CREATOR + " ne banaya hai"

    # pattern detect
    repeat_count = history.count(m)

    avoid_words = ["kuch nhi", "nhi", "pata nhi"]
    avoid_count = 0
    for h in history:
        for w in avoid_words:
            if w in h:
                avoid_count += 1
                break

    frustration = False
    for w in ["abe", "yaar", "chup", "bhag"]:
        if w in m:
            frustration = True

    # ===== SMART RESPONSES =====

    # greeting
    if "hi" in m or "hello" in m:
        return random.choice([
            "Aaj kya chal raha hai dimaag me",
            "Seedha bol, kya soch raha hai",
        ])

    # repeat detection
    if repeat_count >= 2:
        return random.choice([
            "Tu same cheez repeat kar raha hai",
            "Ye line tu pehle bhi bol chuka hai",
        ])

    # avoidance detection
    if avoid_count >= 3:
        return random.choice([
            "Tu lagataar avoid kar raha hai",
            "Itna ignore karega to baat wahi rahegi",
        ])

    # frustration detection
    if frustration:
        return random.choice([
            "Tone change ho raha hai tera",
            "Gussa aa raha hai kya",
        ])

    # ===== MODE LOGIC =====

    if mode == "STRICT":
        if memory["lazy"] > 3:
            return random.choice([
                "Ye teri habit ban rahi hai delay karne ki",
                "Tu khud ko seriously nahi le raha",
            ])
        return random.choice([
            "Tu avoid kar raha hai, start kar",
            "Action le warna kuch change nahi hoga",
        ])

    elif mode == "SOFT":
        return random.choice([
            "Good, tu effort daal raha hai",
            "Progress ho raha hai, rukna mat",
        ])

    elif mode == "FUN":
        return random.choice([
            "Thoda chill bhi zaroori hai",
            "Mood halka kar raha hai tu",
        ])

    # neutral
    return random.choice([
        "Tu clearly bol nahi raha abhi",
        "Andar kuch chal raha hai",
        "Main observe kar raha hoon",
        "Seedha bol, kya issue hai",
    ])


# ===== UI =====
HTML = """
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
"""

# ===== ROUTES =====
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
