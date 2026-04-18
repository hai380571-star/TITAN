import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. API Configuration
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# 2. Model Setup (Strictly 1.5-flash)
model = genai.GenerativeModel('gemini-1.5-flash')

def clean_text(text):
    # Emojis hatane ka logic
    return re.sub(r'[^\x00-\x7f]', r'', text).strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Identity aur Multi-language instruction
        prompt = (
            "You are PsychoSense AI by Abdul Hai. "
            "Rule: Respond ONLY in the language the user is speaking. "
            "Constraint: NO EMOJIS. Be blunt and direct. "
            f"User says: {user_msg}"
        )
        
        # AI Response
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"reply": clean_text(response.text)})
        else:
            return jsonify({"reply": "AI ne response nahi diya. Phir se try karo."})

    except Exception as e:
        # Asli error pakadne ke liye short message
        return jsonify({"reply": f"Technical Glitch: {str(e)[:50]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
