import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompts import getSystemPromptForSearchVerify

load_dotenv()
# API_KEY = os.getenv("GEMINI_API")
genai.configure(api_key="AIzaSyCOtgEfrf_lq_MNXmriNPbbg_QAVmBMbE4")

def geminiInit(system_prompt):
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
        system_instruction=system_prompt
    )
    chat_session = model.start_chat()
       
    return chat_session

def getGeminiResponse(user_query, chatSession=None):
    response = chatSession.send_message(user_query)
    return response.text 

def upload_to_gemini(path):
  file = genai.upload_file(path, mime_type=None)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

if __name__ == "__main__":
    system_prompt = getSystemPromptForSearchVerify()  
    chat_session = geminiInit(system_prompt) 
    print(getGeminiResponse("What is AI?", ""))
