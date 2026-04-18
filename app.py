import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# API Setup
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 1.5-flash model name (Latest & Stable)
model = genai.GenerativeModel('gemini-1.5-flash')

def clean_text(text):
    return re.sub(r'[^\x00-\x7f]', r'', text).strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Identity Logic
        prompt = (
            "You are PsychoSense AI by Abdul Hai. "
            "Respond in the same language as the user. NO EMOJIS. "
            f"User: {user_msg}"
        )
        
        # Response with latest API handling
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"reply": clean_text(response.text)})
        else:
            return jsonify({"reply": "AI khamosh hai, phir se pucho."})

    except Exception as e:
        # Is baar error message short rakha hai
        return jsonify({"reply": f"Technical Glitch: {str(e)[:50]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
