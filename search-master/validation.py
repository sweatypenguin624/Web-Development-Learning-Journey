from geminiTemplate import getGeminiResponse

def checkAgain(resultLLama, resultGemini, question, searchContext, chat_session):
    prompt = ""
    prompt += "Question: " + question + "\n"
    prompt += "\nSearch Context: " + searchContext + "\n"
    prompt += "<YOUR_RESPONSE>" + resultGemini + "</YOUR_RESPONSE>\n"
    prompt += "<OTHER_RESPONSE>" + resultGemini + "</OTHER_RESPONSE>"
    return getGeminiResponse(prompt, chatSession=chat_session)