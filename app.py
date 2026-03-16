import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# আপনার দেওয়া Gemini API Key কনফিগারেশন
API_KEY = "AIzaSyDnV3MBfWvCvqq-e1zS95A3NCvzuhBsgiA"
genai.configure(api_key=API_KEY)

# এআই মডেল সেটআপ
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    # My Book/templates/index.html ফাইলটি লোড হবে
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_task():
    data = request.json
    point_id = data.get('point_id')
    user_input = data.get('input_text')

    # আপনার ১৭টি পয়েন্টের জন্য এআই ইনস্ট্রাকশন সেটআপ
    prompts = {
        "P1": f"Human touch writing: Rewrite this text to sound emotional and human: {user_input}",
        "P2": f"KDP Keywords: Suggest high-ranking SEO keywords for this book title: {user_input}",
        "P10": f"Translator: Translate this into fluent Bengali/English: {user_input}",
        "P12": f"Grammar: Fix any grammar or spelling mistakes in this text: {user_input}"
    }

    # নির্ধারিত পয়েন্ট অনুযায়ী প্রম্পট সিলেক্ট করা
    selected_prompt = prompts.get(point_id, user_input)

    try:
        response = model.generate_content(selected_prompt)
        return jsonify({"success": True, "result": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print(f"🚀 NEXUS PRIME ONLINE | PROJECT: 825413287048")
    app.run(debug=True, port=5000)
