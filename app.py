from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# API key set karo
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Updated model (important)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")

        response = model.generate_content(user_message)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
