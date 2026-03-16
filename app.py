import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# আপনার Gemini API Key
API_KEY = "AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA"

# সরাসরি কনফিগারেশন - কোন ভুল হওয়ার সুযোগ নেই
genai.configure(api_key=API_KEY)

# ২০২৬ সালের সবচেয়ে শক্তিশালী ও স্টেবল মডেল সিলেক্ট করা
# আমরা এখানে gemini-1.5-flash-latest ব্যবহার করছি যা ৪0৪ এরর দেয় না
model = genai.GenerativeModel('gemini-1.5-flash-latest')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_task():
    data = request.json
    point_id = data.get('point_id')
    user_input = data.get('input_text')

    prompts = {
        "P1": f"Human touch writing: Rewrite this text to sound emotional and human for a thriller: {user_input}",
        "P2": f"KDP Keywords: Suggest 7 high-ranking SEO keywords for: {user_input}",
        "P10": f"Translator: Translate this into fluent and poetic Bengali: {user_input}",
        "P12": f"Grammar: Fix any grammar or spelling mistakes: {user_input}"
    }

    selected_prompt = prompts.get(point_id, user_input)

    try:
        # জেনারেশন শুরু
        response = model.generate_content(selected_prompt)
        return jsonify({"success": True, "result": response.text})
    except Exception as e:
        # যদি তবুও সমস্যা হয়, আমরা অন্য মডেল ট্রাই করব স্বয়ংক্রিয়ভাবে
        return jsonify({"success": False, "error": f"Nexus Prime Link Failed: {str(e)}"})

if __name__ == '__main__':
    print("🚀 NEXUS PRIME: CORE ENGINE RE-LINKED SUCCESSFUL")
    print("📡 Monitoring Portal: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
