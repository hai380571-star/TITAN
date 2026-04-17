import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# API Setup
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')

def clean_text(text):
    # Strict No-Emoji Policy
    return re.sub(r'[^\x00-\x7f]', r'', text).strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Multi-Language Prompt Logic
        prompt = (
            "Identity: You are PsychoSense AI, created by Abdul Hai. "
            "Role: Professional and blunt psychology coach. "
            "Language Rule: Detect the user's language and respond in the SAME language. "
            "If the user speaks Bengali, reply in Bengali. If Urdu, reply in Urdu. "
            "If Hindi/English, reply in Hinglish. "
            "Constraint: STRICTLY NO EMOJIS. Be direct and observant. "
            f"User message: {user_msg}"
        )
        
        response = model.generate_content(prompt)
        reply = clean_text(response.text) if response.text else "Dimaag blank ho gaya, phir se bol."
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"System Error: Thoda wait kar le."})

if __name__ == "__main__":
    # Render Port Binding
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
