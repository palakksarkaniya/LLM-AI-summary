import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")
base_url = os.getenv("CARERBRIDGE_BASE_URL")

facility_id = "00bdfbe0-18fa-59f7-a485-dfffd67fb32e"

# 1. Get facility data
facility_url = f"{base_url}/api/facilities/{facility_id}/details"

facility_response = requests.get(
    facility_url,
    timeout=30
)

facility_response.raise_for_status()

facility_data = facility_response.json()

print("Facility loaded:")
print(facility_data["facility_name"])


# 2. Send facility data to NVIDIA
nvidia_url = "https://integrate.api.nvidia.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

prompt = f"""
You are an AI assistant for CarerBridge.

The caregiver can already see all ratings, scores, distances and other
numbers on the screen. DO NOT repeat them.

Your job is to give a short overall summary of what the displayed
information suggests.

Rules:
- Write ONLY 3 to 4 short sentences.
- Do NOT repeat any ratings, scores, distances, percentages or other numbers.
- Do NOT list information already visible on the UI.
- Summarise the main strengths, weaker areas and practical considerations.
- Compare areas relatively, for example "staffing is weaker than other care areas."
- Only use information supported by the provided data.
- Do not invent causes or explanations.
- Do not call something safe, unsafe, concerning, excellent, poor, or recommended unless explicitly supported.
- Mention important uncertainty, such as unconfirmed dementia classification.
- Do not recommend whether the caregiver should choose the facility.
- Use simple, neutral language.
- No headings or bullet points.

FACILITY DATA:
{json.dumps(facility_data, indent=2)}

Give only the short caregiver summary.
"""

payload = {
    "model": "nvidia/nemotron-3.5-lightning-30b-a3b",
    "messages": [
        {
            "role": "system",
            "content": "Give only the final answer. Do not show reasoning."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 500,
    "temperature": 0.2,
    "stream": False,
    "chat_template_kwargs": {
        "enable_thinking": False
    }
}

print("\nSending facility data to NVIDIA...")

response = requests.post(
    nvidia_url,
    headers=headers,
    json=payload,
    timeout=90
)

response.raise_for_status()

result = response.json()

print("\nAI EXPLANATION:\n")
print(result["choices"][0]["message"]["content"])