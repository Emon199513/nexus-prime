from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# আপনার Gemini API Key
API_KEY = "AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA"
client = genai.Client(api_key=API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_task():
    data = request.json
    point_id = data.get('point_id')
    user_input = data.get('input_text')

    # আপনার ১৭টি পয়েন্টের জন্য এআই ইনস্ট্রাকশন
    prompts = {
        "P1": f"Human touch writing: Rewrite this text to sound emotional, cinematic and human-like for a thriller novel: {user_input}",
        "P2": f"KDP Keywords: Suggest 7 high-ranking Amazon KDP SEO keywords for: {user_input}",
        "P10": f"Translator: Translate this text into fluent and poetic Bengali: {user_input}",
        "P12": f"Grammar: Fix any grammar or spelling mistakes and improve the flow: {user_input}"
    }

    selected_prompt = prompts.get(point_id, user_input)

    try:
        # এখানে মডেলের নাম 'gemini-1.5-pro' দিয়ে ট্রাই করা হচ্ছে যা বেশি স্টেবল
        response = client.models.generate_content(
            model="gemini-1.5-pro", 
            contents=selected_prompt
        )
        return jsonify({"success": True, "result": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": f"Connection Error: {str(e)}"})

if __name__ == '__main__':
    print(f"🚀 NEXUS PRIME ONLINE | PROTOCOL FIX APPLIED")
    app.run(debug=True, port=5000)
