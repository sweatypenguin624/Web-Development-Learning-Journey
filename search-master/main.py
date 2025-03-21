from llamaTemplate import getLlamaResponse
from tavilyTemplate import getTavilySearchResults
from geminiTemplate import getGeminiResponse, geminiInit
from utils import getFacts, splitString
from prompts import getSystemPromptForClaimExtraction, getSystemPromptForSearchVerify, getSystemPromptForCheckAgain, getPromptForfinalSummaryGeneration
from validation import checkAgain

def log(data, name, filename='log1.txt'):
    try:
        with open(filename, 'a') as file:
            file.write(f"{name}:\n")
            if isinstance(data, list):
                for item in data:
                    file.write(f"{item}\n")
            elif isinstance(data, str):
                file.write(f"{data}\n")
            else:
                raise ValueError("Data must be a list or a string.")
            
            file.write("\n\n\n")
        
        print(f"Data successfully appended to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


user_query = "Mahatma Gandhi lives on as India's Father of the Nation, doing alive and well and still leading mass movements at age 120. He was awarded the Bharat Ratna by the State Government of Indianapolis yesterday."
searches = []

def checkVerify(claims, questions):
    chat_session = geminiInit(getSystemPromptForSearchVerify())
    resultSearch = []
    resultGemini = []
    resultLlama = []
    for i in range(len(questions)):
        searchRes, content = getTavilySearchResults(questions[i])
        resultSearch.append(content)
        searches.append(searchRes)
        query = claims[i] + "\nSearch Context: " + resultSearch[i]
        resultGemini.append(getGeminiResponse(query, chatSession=chat_session))
        resultLlama.append(getLlamaResponse(query, system_prompt=getSystemPromptForSearchVerify()))

    return resultSearch, resultGemini, resultLlama

# def answerFurtherQs(result):
#     for res in result:
#         if result[8:18] == "CANNOT SAY":
#             id = result.find("Questions:")
#             newqs =  splitString(result[id:])
#         for q in newqs:
#             resSearch = getTavilySearchResults(q)
#             resultSearch.append(resSearch)
#             gemini_query = q + "\nSearch Context: " + resSearch
#             result.append(getGeminiResponse(gemini_query))


def compareOpinions(gemini, llama):
    if (gemini[8:13] == llama[8:13]):
        return True
    return False

def verifier(questions, resultSearch, resultGemini, resultLlama):
    resultFinal = []
    chat_session_check = geminiInit(getSystemPromptForCheckAgain())
    assert len(resultGemini) == len(resultLlama)
    for i in range(len(resultLlama)):
        if compareOpinions(resultGemini[i], resultLlama[i]):
            resultFinal.append(resultGemini[i])
        else:
            resultFinal.append(checkAgain(resultLlama[i], resultGemini[i], questions[i], resultSearch[i], chat_session_check))
    return resultFinal

def genSummary(claims, questions, resultSearch, resultFinal):
    chat_session_final = geminiInit(getPromptForfinalSummaryGeneration())
    for i in range((len(claims))):
        if resultFinal[i][8:13] != "CANNO":
            conc = "Claim: "
            for c in claims: conc += c
            conc += "\nQuestions: "
            for q in questions: conc += q
            conc += "\nSearch context: "
            for r in resultSearch: conc += r
            conc += "\nVerification results: "
            for v in resultFinal: conc += v
            log(conc, "\n\n\nConcatenated text: \n")
            final_summary = getGeminiResponse(conc, chatSession=chat_session_final)
            log(final_summary, "\n\nFinal Summary: \n")
            return str(final_summary)


def checkAllClaims(claim: str):
    response = getLlamaResponse(claim, system_prompt=getSystemPromptForClaimExtraction())
    log(response, "Llama Response: ")
    claims, questions = getFacts(response)
    resultSearch, resultGemini , resultLlama = checkVerify(claims, questions)
    log(resultSearch, "Results of Tavilly searches: ")
    log(resultGemini, "Gemini responses: ")
    log(resultLlama, "Llama responses: ")
    resultFinal = verifier(questions, resultSearch, resultGemini, resultLlama)
    log(resultFinal, "Final responses: ")
    finalResult = genSummary(claims, questions, resultSearch, resultFinal)
    log(finalResult, "\n\nFinal Result: ")
    print(finalResult)
    return finalResult, searches


if __name__ == "__main__":
    print(checkAllClaims(user_query))