from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# আপনার Gemini API Key (Verified from your screenshot)
API_KEY = "AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA"

# গুগলের নতুন ২০২৬ এডিটর SDK ব্যবহার করে কানেকশন
client = genai.Client(api_key=API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_task():
    data = request.json
    point_id = data.get('point_id')
    user_input = data.get('input_text')

    prompts = {
        "P1": f"Human touch writing: Rewrite this thriller novel scene to be emotional and cinematic: {user_input}",
        "P2": f"KDP Keywords: Suggest 7 trending Amazon SEO keywords for: {user_input}",
        "P10": f"Translator: Translate this into beautiful Bengali: {user_input}",
        "P12": f"Grammar: Fix and improve the flow of this text: {user_input}"
    }

    selected_prompt = prompts.get(point_id, user_input)

    try:
        # ২০২৬ সালের ড্যাশবোর্ড অনুযায়ী আধুনিক মডেল ব্যবহার (Gemini 3.1)
        response = client.models.generate_content(
            model="gemini-3.1-flash", 
            contents=selected_prompt
        )
        return jsonify({"success": True, "result": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": f"Nexus Prime Sync Error: {str(e)}"})

if __name__ == '__main__':
    print("🚀 NEXUS PRIME 2026: QUANTUM LINK ESTABLISHED")
    app.run(debug=True, port=5000)
