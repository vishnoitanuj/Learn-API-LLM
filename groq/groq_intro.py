import os
import requests

groq_api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json",
}

data = {
    "model": "llama3-8b-8192",
    "messages": [{"role": "user", "content": "Tell me a really funny joke?"}],
}

response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print(response.json()["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
