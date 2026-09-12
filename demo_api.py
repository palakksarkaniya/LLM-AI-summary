from fastapi import FastAPI, HTTPException
import pandas as pd
import math
import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

app = FastAPI(
    title="CarerBridge Demo API",
    version="1.0"
)

DATASET_PATH = "facility_iteration2.csv"

df = pd.read_csv(DATASET_PATH)


def clean_value(value):
    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def build_facility_response(row):

    return {
        "facility_id": clean_value(row["facility_id"]),
        "facility_name": clean_value(row["facility_name"]),
        "provider_name": clean_value(row["provider_name"]),

        "address": {
            "street": clean_value(row["address"]),
            "suburb": clean_value(row["suburb"]),
            "state": clean_value(row["state"]),
            "postcode": clean_value(row["postcode"])
        },

        "care_type": clean_value(row["care_type"]),

        "dementia_classification": {
            "code": clean_value(row["classification_code"]),
            "label": clean_value(row["classification_label"]),
            "evidence_state": clean_value(row["evidence_state"])
        },

        "care_quality": {
            "overall_rating": clean_value(row["overall_rating"]),
            "resident_experience_rating": clean_value(
                row["residents_experience_rating"]
            ),
            "staffing_rating": clean_value(row["staffing_rating"]),
            "compliance_rating": clean_value(row["compliance_rating"]),
            "quality_measures_rating": clean_value(
                row["quality_measures_rating"]
            ),
            "care_quality_score": clean_value(
                row["care_quality_score"]
            ),
            "rating_period": clean_value(row["rating_period"])
        },

        "visit_practicality": {
            "score": clean_value(row["visit_static_score"]),

            "public_transport_score": clean_value(
                row["public_transport_score"]
            ),

            "nearest_public_transport_distance_m": clean_value(
                row["nearest_public_transport_distance_m"]
            ),

            "parking_score": clean_value(row["parking_score"]),

            "nearest_parking_distance_m": clean_value(
                row["nearest_parking_distance_m"]
            ),

            "accessible_toilet_score": clean_value(
                row["accessible_toilet_score"]
            ),

            "nearest_accessible_toilet_distance_m": clean_value(
                row["nearest_accessible_toilet_distance_m"]
            )
        },

        "surrounding_support": {
            "score": clean_value(
                row["surrounding_support_score"]
            ),

            "healthcare_score": clean_value(
                row["healthcare_score"]
            ),

            "pharmacy_score": clean_value(
                row["pharmacy_score"]
            ),

            "open_space_score": clean_value(
                row["open_space_score"]
            ),

            "community_support_score": clean_value(
                row["community_support_score"]
            )
        },

        "full_fit_ready": clean_value(row["full_fit_ready"])
    }


@app.get("/api/facilities/{facility_id}/details")
def get_facility_details(facility_id: str):

    result = df[df["facility_id"] == facility_id]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Facility not found"
        )

    row = result.iloc[0]

    return build_facility_response(row)

@app.get("/api/ai/explain/{facility_id}")
def explain_facility(facility_id: str):

    # Find facility
    result = df[df["facility_id"] == facility_id]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Facility not found"
        )

    row = result.iloc[0]

    # Use the SAME structured facility data
    # that your normal API already returns
    facility_data = build_facility_response(row)

    if not NVIDIA_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="NVIDIA API key not found"
        )

    prompt = f"""
You are an AI assistant for CarerBridge.

The caregiver can already see the facility's ratings,
scores, distances and numbers on the screen.

Your job is to briefly explain what the results mean
when viewed together.

Rules:
- Write ONLY 3 to 4 short sentences.
- Do NOT repeat ratings, scores, distances or percentages.
- Do NOT simply list information already shown on the UI.
- Summarise the main strengths, weaker areas and practical considerations.
- Compare areas relatively when useful.
- Only use information supported by the supplied data.
- Do not invent causes or explanations.
- Do not recommend whether the caregiver should choose the facility.
- Mention important uncertainty if the data explicitly shows it.
- Use simple, neutral language.
- No headings.
- No bullet points.

FACILITY DATA:

{json.dumps(facility_data, indent=2)}

Return only the short caregiver summary.
"""

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
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
                "content": prompt
            }
        ],
        "max_tokens": 180,
        "temperature": 0.2,
        "stream": False,
        "chat_template_kwargs": {
            "enable_thinking": False
        }
    }

    try:
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=90
        )

        response.raise_for_status()

        data = response.json()

        summary = data["choices"][0]["message"]["content"]

        return {
            "facility_id": facility_id,
            "facility_name": facility_data["facility_name"],
            "summary": summary
        }

    except requests.exceptions.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"NVIDIA API request failed: {str(error)}"
        )

@app.get("/api/facilities")
def list_facilities():
    facilities = []

    for _, row in df.iterrows():
        facilities.append({
            "facility_id": clean_value(row["facility_id"]),
            "facility_name": clean_value(row["facility_name"]),
            "suburb": clean_value(row["suburb"]),
            "state": clean_value(row["state"]),
            "care_type": clean_value(row["care_type"])
        })

    return facilities