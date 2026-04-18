import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. API Configuration
# Render ke Environment Variables se key uthayega
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    print("SUCCESS: API Key connected successfully!")
else:
    print("CRITICAL: API Key not found in Environment Variables!")

# Naya Model jo 100% kaam karega
model = genai.GenerativeModel('gemini-1.5-flash')

def clean_text(text):
    # Emojis hatane ke liye
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
            "Identity: You are PsychoSense AI, created by Abdul Hai. "
            "Role: Blunt and observant Psychology Coach. "
            "Rule: Respond ONLY in the language the user is speaking (Bengali/Urdu/Hinglish). "
            "Constraint: STRICTLY NO EMOJIS. Be direct and concise. "
            f"User says: {user_msg}"
        )
        
        # AI Response generate karna
        response = model.generate_content(prompt)
        
        if response.text:
            final_reply = clean_text(response.text)
            return jsonify({"reply": final_reply})
        else:
            return jsonify({"reply": "AI ne koi jawab nahi diya, phir se try kar."})

    except Exception as e:
        # Error screen pe dikhane ke liye debugging line
        return jsonify({"reply": f"Asli Error: {str(e)}"})

if __name__ == "__main__":
    # Render port binding
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
