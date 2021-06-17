import requests
url = "http://localhost:8000/?filename=1019315 Guido Sava - Fever (Original Mix).wav"
response = requests.get(url, stream=True)
print(response.content)
print('don')