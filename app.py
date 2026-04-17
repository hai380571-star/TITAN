from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 🔥 Memory + Creator
memory = {"lazy": 0, "success": 0}
CREATOR = "Abdul Hai"

# 🧠 Analyze Function
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


# 🧠 Reply Function
def reply(mode, msg):
    m = (msg or "").lower()

    if "creator" in m or "kisne banaya" in m:
        return f"Mujhe {CREATOR} ne banaya hai 😏"

    if mode == "STRICT":
        return "Sach bol—tu avoid kar raha hai. Start kar abhi."

    elif mode == "SOFT":
        return "Good. Tu effort daal raha hai—continue kar."

    elif mode == "FUN":
        return "Bakchodi mode ON 😏 bol kya kare?"

    return "Seedha bol—andar kya chal raha hai?"


# 🎨 HTML (inline UI)
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PsychoSense</title>
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
    word-wrap:break-word;
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
</style>
</head>

<body>

<div class="header">
<b>PsychoSense</b><br>
<small>AI Behavioral Mirror</small>
</div>

<div id="chat"></div>

<div class="footer">
<input id="input" placeholder="Type your thoughts...">
<button onclick="send()">➤</button>
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

        addMsg(data.reply + "<br><small>"+data.mode+"</small>","bot");

    } catch(err){
        typing.remove();
        addMsg("Server error 😵","bot");
    }
}
</script>

</body>
</html>
"""

# 🌐 Routes
@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user = data.get("message") or data.get("msg") or ""

        if not user:
            return jsonify({"reply": "Kuch to bol 😄", "mode": "error"})

        mode = analyze(user)
        res = reply(mode, user)

        return jsonify({"reply": res, "mode": mode})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Server error 😵", "mode": "error"})


if __name__ == "__main__":
    app.run(debug=True)    elif mode == "FUN":
        return "Bakchodi mode ON 😏 bol kya kare?"

    return "Seedha bol—andar kya chal raha hai?"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user = request.json.get("msg")
    mode = analyze(user)
    res = reply(mode, user)

    return jsonify({"reply": res, "mode": mode})


if __name__ == "__main__":
    app.run(debug=True)
