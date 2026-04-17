from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

memory = {"lazy": 0, "success": 0}
CREATOR = "Abdul Hai"

def analyze(text):
    t = text.lower()

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
    m = msg.lower()

    if "creator" in m or "kisne banaya" in m:
        return f"Mujhe {CREATOR} ne banaya hai 😏"

    if mode == "STRICT":
        return "Sach bol—tu avoid kar raha hai. Start kar abhi."

    elif mode == "SOFT":
        return "Good. Tu effort daal raha hai—continue kar."

    elif mode == "FUN":
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
