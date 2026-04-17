import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# API Key setup from Render Environment
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Safety Settings: Taaki AI har baat pe block na kare
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel('gemini-pro')

def clean_text(text):
    # Emojis hatane ke liye regex
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
            "Identity: You are PsychoSense AI, created by Abdul Hai. "
            "Role: Strict Psychology Coach. Language: Hinglish. "
            "Rules: NO EMOJIS. Be blunt, direct, and observant. "
            f"User says: {user_msg}"
        )
        
        response = model.generate_content(prompt, safety_settings=safety_settings)
        reply = clean_text(response.text) if response.text else "Dimaag kaam nahi kar raha, phir se bol."
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)[:30]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    try:
        context = "\n".join(chat_history[-5:])
        full_prompt = f"{SYSTEM_INSTRUCTION}\nContext:\n{context}\nUser: {user_input}\nPsychoSense:"
        response = model.generate_content(full_prompt)
        reply = remove_emojis(response.text).strip()
        chat_history.append(f"User: {user_input}")
        chat_history.append(f"AI: {reply}")
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "System busy hai, phir se try kar."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
