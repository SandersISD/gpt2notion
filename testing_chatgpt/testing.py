import requests
import json

url = 'http://127.0.0.1:5000/assistant'  # Replace with the actual URL of your endpoint

payload = {
    'prompt': 'There is a meeting with my teacher on today 8pm. Put it into Notion using the given function. '
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    reply = response.text
    print(reply)
else:
    print('Request failed with status code:', response.status_code)