# import requests

# def googleSearch(query):
#     SERPER_API_KEY = "6a54bcd16f78b7062899d2121ed6f84c7d3b3f2d"
#     sites = "site:factly.in OR site:boomlive.in OR site:snopes.com OR site:factcheck.org"
#     q = f"{query} {sites}"

#     url = "https://google.serper.dev/search"
#     headers = {
#         "X-API-KEY": SERPER_API_KEY,
#         "Content-Type": "application/json"
#     }
#     data = {"q": q}

#     response = requests.post(url, json=data, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": response.status_code, "message": response.text}

# # Example usage:
# result = googleSearch("COVID-19 vaccine myths")
# print(result)
