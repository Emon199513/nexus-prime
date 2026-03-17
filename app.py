import os
import requests
from flask import Flask, render_template, request, jsonify
from google import genai
from openai import OpenAI

app = Flask(__name__)

# --- হারুন মাস্টারমাইন্ডের সিক্রেট এপিআই কি-সমূহ ---
GEMINI_KEY = "AIzaSyDJklchI6NEI0g1yvCj0mkLfBe-IRuMn74"
ELEVENLABS_KEY = "sk_6aac1d90880b183fb92c1aaf796fcfb4bd537bace2669e12"
OPENAI_KEY = "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"
BUFFER_KEY = "RgbAKwpgSK1AOZhZPo4dwkzT54hZyDzwzgtqgSX1-Bp"
BUFFER_ORG_ID = "69b8e1c63efcfa6297a32393"

# এআই ক্লায়েন্ট সেটআপ
gemini_client = genai.Client(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_task():
    data = request.json
    point_id = data.get('point_id')
    user_input = data.get('input_text')

    try:
        # ১. জেমিনি টেক্সট লজিক (P1, P2, P10, P12)
        if point_id in ["P1", "P2", "P10", "P12"]:
            prompt_prefix = {
                "P1": "Rewrite this scene cinematic and emotional: ",
                "P2": "Amazon KDP high-ranking keywords for: ",
                "P10": "Translate this into beautiful Bengali: ",
                "P12": "Fix grammar and improve flow: "
            }
            final_prompt = prompt_prefix.get(point_id, "") + user_input
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash", contents=final_prompt
            )
            return jsonify({"success": True, "type": "text", "result": response.text})

        # ২. ডাল-ই ইমেজ লজিক (P14)
        elif point_id == "P14":
            response = openai_client.images.generate(
                model="dall-e-3",
                prompt=f"Cinematic thriller book cover, high resolution, professional lighting, theme: {user_input}",
                n=1, size="1024x1024"
            )
            return jsonify({"success": True, "type": "image", "result": response.data[0].url})

        # ৩. ইলেভেনল্যাবস ভয়েস লজিক (P15)
        elif point_id == "P15":
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
            payload = {"text": user_input, "model_id": "eleven_multilingual_v2"}
            v_res = requests.post(url, json=payload, headers=headers)
            
            # অডিও ফাইল সেভ করা
            audio_path = os.path.join('static', 'voice_output.mp3')
            with open(audio_path, "wb") as f:
                f.write(v_res.content)
            return jsonify({"success": True, "type": "audio", "result": "/static/voice_output.mp3"})

        # ৪. বাফার অটোমেশন লজিক (P17)
        elif point_id == "P17":
            buffer_url = "https://api.bufferapp.com/graphql"
            buffer_headers = {"Authorization": f"Bearer {BUFFER_KEY}", "Content-Type": "application/json"}
            mutation = {
                "query": "mutation CreateIdea($input: CreateIdeaInput!) { createIdea(input: $input) { success } }",
                "variables": {"input": {"organizationId": BUFFER_ORG_ID, "content": {"text": user_input, "title": "Nexus Prime Post"}}}
            }
            requests.post(buffer_url, json=mutation, headers=buffer_headers)
            return jsonify({"success": True, "type": "text", "result": "Successfully sent to Buffer Ideas!"})

        return jsonify({"success": False, "error": "Unknown Command ID"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    if not os.path.exists('static'): os.makedirs('static')
    print("🚀 NEXUS PRIME: SYSTEM LINKED. GO TO http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
