from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
import requests
import os
import pyttsx3
import io

app = Flask(__name__)

# Load Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file received'}), 400

    audio_file = request.files['audio']

    # Convert audio to text
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(io.BytesIO(audio_file.read()))

    with audio_data as source:
        audio_content = recognizer.record(source)
        try:
            user_text = recognizer.recognize_google(audio_content)
        except sr.UnknownValueError:
            return jsonify({'user_text': '', 'bot_response': "I couldn't understand that."})
        except sr.RequestError:
            return jsonify({'user_text': '', 'bot_response': "Error with speech recognition service."})

    # Send text to Groq API
    groq_response = get_groq_response(user_text)

    # Convert response to speech (Non-blocking)
    tts_engine.say(groq_response)
    tts_engine.runAndWait()

    return jsonify({'user_text': user_text, 'bot_response': groq_response})

def get_groq_response(text):
    url = "https://api.groq.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistral",  # Use "mistral" instead of "gpt-4-turbo" since Groq supports Mistral.
        "messages": [{"role": "user", "content": text}]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "I couldn't get a response.")
    except Exception as e:
        return f"Error contacting Groq API: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6111, debug=True)
