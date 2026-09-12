import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

print("API key found:", api_key is not None)

url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "messages": [
        {
            "role": "system",
            "content": "Give only the final answer. Do not show reasoning."
        },
        {
            "role": "user",
            "content": "Say hello in one short sentence."
        }
    ],
    "max_tokens": 100,
    "temperature": 0.2,
    "stream": False,
    "chat_template_kwargs": {
        "enable_thinking": False
    }
}

print("Sending request...")

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60
)

print("Status code:", response.status_code)
print("Response:")
data = response.json()

print("\nMODEL RESPONSE:")
print(data["choices"][0]["message"]["content"])