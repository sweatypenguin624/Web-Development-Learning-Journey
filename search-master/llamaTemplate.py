from groq import Groq
from dotenv import load_dotenv
import os
from utils import getFacts

load_dotenv()
# GROQ_API_KEY = os.getenv("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")

def getLlamaResponse(user_claim, system_prompt):
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_claim
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    res = ""
    for chunk in completion:
        res = res + str(chunk.choices[0].delta.content)
    
    return res


if __name__ == "__main__":
    print(getLlamaResponse("Hi there!"))