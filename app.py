from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# ===== MEMORY =====
memory = {"lazy": 0, "success": 0}
history = []
last_reply = ""
CREATOR = "Abdul Hai"

# ===== HELPER (NO REPEAT) =====
def pick(options):
    global last_reply
    random.shuffle(options)
    for opt in options:
        if opt != last_reply:
            last_reply = opt
            return opt
    return options[0]

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

# ===== REPLY =====
def reply(mode, msg):
    global history
    m = (msg or "").lower()

    history.append(m)
    if len(history) > 6:
        history.pop(0)

    # creator
    if any(x in m for x in ["creator", "kisne banaya", "who made you"]):
        return "Mujhe " + CREATOR + " ne banaya hai"

    # patterns
    repeat_count = history.count(m)

    avoid_words = ["kuch nhi", "nhi", "pata nhi"]
    avoid_count = sum(1 for h in history if any(w in h for w in avoid_words))

    frustration = any(w in m for w in ["abe", "yaar", "bhag"])

    # ===== RESPONSES =====

    if "hi" in m or "hello" in m:
        return pick([
            "Aaj kya chal raha hai dimaag me",
            "Seedha bol, kya soch raha hai",
            "Kya scene hai aaj",
        ])

    if repeat_count >= 2:
        return pick([
            "Tu same cheez repeat kar raha hai",
            "Ye line tu pehle bhi bol chuka hai",
            "Repeat karne se baat change nahi hogi",
        ])

    if avoid_count >= 3:
        return pick([
            "Tu lagataar avoid kar raha hai",
            "Itna ignore karega to problem wahi rahegi",
            "Tu sach bolne se bach raha hai",
        ])

    if frustration:
        return pick([
            "Tone change ho raha hai tera",
            "Gussa aa raha hai kya",
            "Relax kar, phir bol",
        ])

    # ===== MODE =====

    if mode == "STRICT":
        if memory["lazy"] > 3:
            return pick([
                "Ye teri habit ban rahi hai delay karne ki",
                "Tu khud ko seriously nahi le raha",
                "Tu bas push kar raha hai, action nahi le raha",
            ])
        return pick([
            "Tu avoid kar raha hai, start kar",
            "Action le warna kuch change nahi hoga",
            "Bahane kam, kaam zyada",
        ])

    elif mode == "SOFT":
        return pick([
            "Good, tu effort daal raha hai",
            "Progress ho raha hai, rukna mat",
            "Consistency aa rahi hai",
        ])

    elif mode == "FUN":
        return pick([
            "Thoda chill bhi zaroori hai",
            "Mood halka kar raha hai tu",
            "Break bhi important hota hai",
        ])

    return pick([
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
body {margin:0;font-family:sans-serif;background:#0f172a;color:white;display:flex;flex-direction:column;height:100vh;}
.header {padding:12px;background:#020617;}
#chat {flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;}
.msg {padding:10px;margin:6px;border-radius:12px;max-width:75%;}
.user {background:#22c55e;margin-left:auto;}
.bot {background:#1e293b;}
.footer {display:flex;padding:10px;background:#020617;}
input {flex:1;padding:12px;border-radius:20px;border:none;}
button {margin-left:5px;padding:10px;background:#22c55e;color:white;border:none;border-radius:20px;}
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
