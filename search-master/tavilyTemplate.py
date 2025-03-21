from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()
# API_KEY = os.getenv("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")

def getTavilySearchResults(query: str):
    tavily_client = TavilyClient(api_key="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")
    response = tavily_client.search(query, search_depth="advanced")
    print(response)

    finalRes = ""
    for result in response.get("results"):
        finalRes += result["content"] + "\n"

    everyRes = []
    for res in response.get("results"):
        if 'quora' not in res.get('url') or 'facebook' not in res.get('url') or 'instagram' not in res.get('url') or 't.me' not in res.get('url'):
            everyRes.append(res)

    return everyRes, finalRes

if __name__ == "__main__":
    print(getTavilySearchResults("Who is Narendra Modi?"))