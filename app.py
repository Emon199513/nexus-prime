import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# আপনার Gemini API Key
API_KEY = "AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA"

# গুগলের ২০২৬ এডিশন এসডিকে কানেকশন
client = genai.Client(api_key=API_KEY)

# আপনার ১৭টি পয়েন্টের জন্য এআই ইনস্ট্রাকশন সেটআপ
PROMPT_MAP = {
    "P1": "Human Touch: Rewrite the following thriller scene to make it more emotional, visceral, and human. Focus on senses and internal monologue: ",
    "P2": "KDP SEO: Provide 7 high-performing, niche-specific Amazon KDP keywords for a book titled: ",
    "P3": "Prompt Creation: Create a highly detailed Midjourney/DALL-E prompt for a cyberpunk/neo-noir scene described as: ",
    "P10": "Translator: Translate the following text into professional, poetic, and cinematic Bengali: ",
    "P12": "Grammar: Correct all grammatical errors and enhance the vocabulary for this paragraph: ",
    "P13": "Plagiarism: Analyze if the following text sounds too generic or AI-generated, and suggest unique rewrites: ",
    "P14": "Image Gen Assistant: Describe a visually stunning book cover concept for: ",
    "P16": "KDP Calculator: Based on page count, suggest the spine width and bleed requirements for: "
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_task():
    data = request.json
    point_id = data.get('point_id')
    user_input = data.get('input_text')

    # সঠিক প্রম্পট নির্বাচন
    base_prompt = PROMPT_MAP.get(point_id, "Analyze and help with: ")
    final_prompt = f"{base_prompt}\n\nInput: {user_input}"

    try:
        # ২০২৬ সালে সচল সবচেয়ে স্টেবল টেক্সট মডেল
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=final_prompt
        )
        return jsonify({"success": True, "result": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("🚀 NEXUS PRIME 2.0: AUTHOR COMMAND CENTER ONLINE")
    app.run(debug=True, port=5000)
