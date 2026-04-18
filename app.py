import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. API Configuration
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 2. Model Setup
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
        
        prompt = (
            "You are PsychoSense AI by Abdul Hai. "
            "Respond ONLY in the user's language. NO EMOJIS. "
            f"User says: {user_msg}"
        )
        
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"reply": clean_text(response.text)})
        else:
            return jsonify({"reply": "AI ne response nahi diya."})

    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)[:50]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
