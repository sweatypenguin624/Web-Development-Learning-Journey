import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# API_KEY = os.getenv("GEMINI_API")
genai.configure(api_key="AIzaSyCOtgEfrf_lq_MNXmriNPbbg_QAVmBMbE4")

def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

def caption(file):
    files = [
        upload_to_gemini(file, mime_type="image/jpeg"),
    ]

    chat_session = model.start_chat(
        history=[
                {
                "role": "user",
                    "parts": [
                        files[0],
                    ],
                },
            ]
    )
    response = chat_session.send_message("Provide a descriptive caption for this image.")
    print(response.text)
    return response.text