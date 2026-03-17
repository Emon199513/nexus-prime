import os
import requests
from flask import Flask, render_template, request, jsonify
from google import genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # .env ফাইল লোড করা
app = Flask(__name__)

# API Clients
gemini_client = genai.Client(api_key=os.getenv("GEMINI_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_task():
    data = request.json
    point_id = data.get('point_id')
    user_input = data.get('input_text')

    try:
        # P1 & P2: Gemini Logic (Text)
        if point_id in ["P1", "P2"]:
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash", contents=user_input
            )
            return jsonify({"success": True, "type": "text", "result": response.text})

        # P14: OpenAI Logic (Image)
        elif point_id == "P14":
            img_res = openai_client.images.generate(
                model="dall-e-3", prompt=user_input, n=1, size="1024x1024"
            )
            return jsonify({"success": True, "type": "image", "result": img_res.data[0].url})

        # P15: ElevenLabs Logic (Voice)
        elif point_id == "P15":
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {"xi-api-key": os.getenv("ELEVENLABS_KEY"), "Content-Type": "application/json"}
            payload = {"text": user_input, "model_id": "eleven_multilingual_v2"}
            v_res = requests.post(url, json=payload, headers=headers)
            with open("static/voice_output.mp3", "wb") as f: f.write(v_res.content)
            return jsonify({"success": True, "type": "audio", "result": "/static/voice_output.mp3"})

        return jsonify({"success": False, "error": "Unknown Command"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    if not os.path.exists('static'): os.makedirs('static')
    app.run(debug=True, port=5000)
