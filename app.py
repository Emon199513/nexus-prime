import os
import requests
from flask import Flask, render_template, request, jsonify
from google import genai
from openai import OpenAI

app = Flask(__name__)

# --- আপনার ভেরিফাইড এপিআই কি-সমূহ ---
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
        # ১. জেমিনি টেক্সট লজিক (P1, P2) - Using 1.5 Flash for higher quota
        if point_id in ["P1", "P2"]:
            prompt_map = {
                "P1": f"Human touch writing: Rewrite this thriller scene to be cinematic and emotional: {user_input}",
                "P2": f"Amazon KDP SEO: Suggest 7 high-ranking keywords for: {user_input}"
            }
            response = gemini_client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt_map.get(point_id, user_input)
            )
            return jsonify({"success": True, "type": "text", "result": response.text})

        # ২. ডাল-ই ৩ ইমেজ লজিক (P14)
        elif point_id == "P14":
            response = openai_client.images.generate(
                model="dall-e-3",
                prompt=f"Cinematic thriller book cover art, high resolution, professional lighting, style: {user_input}",
                n=1, size="1024x1024"
            )
            return jsonify({"success": True, "type": "image", "result": response.data[0].url})

        # ৩. ইলেভেনল্যাবস ভয়েস লজিক (P15)
        elif point_id == "P15":
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
            payload = {"text": user_input, "model_id": "eleven_multilingual_v2"}
            v_res = requests.post(url, json=payload, headers=headers)
            
            # অডিও ফাইল সেভ
            audio_filename = "voice_output.mp3"
            audio_path = os.path.join('static', audio_filename)
            with open(audio_path, "wb") as f:
                f.write(v_res.content)
            return jsonify({"success": True, "type": "audio", "result": f"/static/{audio_filename}"})

        # ৪. বাফার অটোমেশন লজিক (P17)
        elif point_id == "P17":
            buffer_url = "https://api.bufferapp.com/graphql"
            buffer_headers = {"Authorization": f"Bearer {BUFFER_KEY}", "Content-Type": "application/json"}
            mutation = {
                "query": "mutation CreateIdea($input: CreateIdeaInput!) { createIdea(input: $input) { success } }",
                "variables": {"input": {"organizationId": BUFFER_ORG_ID, "content": {"text": user_input, "title": "Nexus Prime AI Concept"}}}
            }
            requests.post(buffer_url, json=mutation, headers=buffer_headers)
            return jsonify({"success": True, "type": "text", "result": "Successfully sent to Buffer Ideas!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    if not os.path.exists('static'): os.makedirs('static')
    print("🚀 NEXUS PRIME ONLINE: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
