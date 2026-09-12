import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

print("Starting test...")

BASE_URL = os.getenv("CARERBRIDGE_BASE_URL")

print("Base URL:", BASE_URL)

facility_id = "00bdfbe0-18fa-59f7-a485-dfffd67fb32e"

url = f"{BASE_URL}/api/facilities/{facility_id}/details"

print("Calling:", url)

try:
    response = requests.get(url, timeout=15)

    print("Status:", response.status_code)

    if response.status_code == 200:
        facility_data = response.json()

        print("\nFacility data:")
        print(facility_data)

    else:
        print("Something went wrong.")
        print(response.text)

except Exception as e:
    print("ERROR:", e)