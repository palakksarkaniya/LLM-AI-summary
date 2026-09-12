import streamlit as st
import requests

st.set_page_config(
    page_title="CarerBridge AI Test",
    layout="centered"
)

API_BASE = "https://llm-ai-summary.onrender.com"

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>

.stApp {
    background-color: #f7f5fb;
}

.block-container {
    max-width: 430px;
    padding-top: 1rem;
}

.header {
    background: white;
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
}

.brand {
    color: #5c2ca3;
    font-size: 18px;
    font-weight: 700;
}

.tabbar {
    display: flex;
    margin-top: 10px;
    border-radius: 10px;
    overflow: hidden;
}

.tab-purple {
    width: 50%;
    background: #6427a6;
    color: white;
    text-align: center;
    padding: 9px;
    font-size: 13px;
    font-weight: 600;
}

.tab-green {
    width: 50%;
    background: #0f6a4d;
    color: white;
    text-align: center;
    padding: 9px;
    font-size: 13px;
    font-weight: 600;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 14px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
}

.facility-name {
    font-size: 20px;
    font-weight: 700;
    color: #222;
}

.muted {
    color: #777;
    font-size: 13px;
}

.section-title {
    font-size: 15px;
    font-weight: 700;
    color: #333;
    margin-bottom: 10px;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 14px;
}

.metric-label {
    color: #555;
}

.metric-value {
    font-weight: 600;
}

.ai-card {
    background: #f4ecff;
    border: 1px solid #e0d2f6;
    padding: 16px;
    border-radius: 16px;
    margin-top: 12px;
}

.ai-title {
    color: #5c2ca3;
    font-weight: 700;
    margin-bottom: 8px;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    background-color: #6427a6;
    color: white;
    border: none;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
<div class="header">
<div class="brand">CarerBridge</div>

<div class="tabbar">
<div class="tab-purple">CareNavigator</div>
<div class="tab-green">Carer Space</div>
</div>
</div>
""",
    unsafe_allow_html=True
)
# -----------------------------
# LOAD FACILITY LIST
# -----------------------------
try:
    response = requests.get(
        f"{API_BASE}/api/facilities",
        timeout=30
    )

    response.raise_for_status()
    facilities = response.json()

except Exception as e:
    st.error(f"Could not load facilities: {e}")
    st.stop()

# -----------------------------
# SELECT FACILITY
# -----------------------------
st.markdown("### Find a care service")

facility_options = {
    f'{f["facility_name"]} — {f["suburb"]}, {f["state"]}': f["facility_id"]
    for f in facilities
}

selected_label = st.selectbox(
    "Search or select a facility",
    options=list(facility_options.keys())
)

selected_id = facility_options[selected_label]

# -----------------------------
# LOAD SELECTED FACILITY
# -----------------------------
try:
    response = requests.get(
        f"{API_BASE}/api/facilities/{selected_id}/details",
        timeout=30
    )

    response.raise_for_status()
    facility = response.json()

except Exception as e:
    st.error(f"Could not load facility: {e}")
    st.stop()

facility_name = facility.get("facility_name", "")
suburb = facility.get("address", {}).get("suburb", "")
state = facility.get("address", {}).get("state", "")
care_type = facility.get("care_type", "")

st.markdown(f"""
<div class="card">
    <div class="facility-name">{facility_name}</div>
    <div class="muted">{care_type}</div>
    <div class="muted">{suburb}, {state}</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# CARE QUALITY
# -----------------------------
care_quality = facility.get("care_quality", {})

st.markdown("""
<div class="card">
<div class="section-title">Care Quality</div>
""", unsafe_allow_html=True)

rows = [
    ("Overall", care_quality.get("overall_rating")),
    ("Resident Experience", care_quality.get("resident_experience_rating")),
    ("Staffing", care_quality.get("staffing_rating")),
    ("Compliance", care_quality.get("compliance_rating")),
    ("Quality Measures", care_quality.get("quality_measures_rating")),
]

for label, value in rows:
    st.markdown(
        f"""
        <div class="metric-row">
            <span class="metric-label">{label}</span>
            <span class="metric-value">
                {value if value is not None else "N/A"}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# VISIT PRACTICALITY
# -----------------------------
visit = facility.get("visit_practicality", {})

st.markdown("""
<div class="card">
<div class="section-title">Visit Practicality</div>
""", unsafe_allow_html=True)

visit_rows = [
    ("Public Transport", visit.get("public_transport_score")),
    ("Parking", visit.get("parking_score")),
    ("Accessible Toilets", visit.get("accessible_toilet_score")),
]

for label, value in visit_rows:
    st.markdown(
        f"""
        <div class="metric-row">
            <span class="metric-label">{label}</span>
            <span class="metric-value">
                {value if value is not None else "N/A"}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# AI EXPLAIN
# -----------------------------
st.markdown(
    f"""
<div style="
    background-color: #f4ecff;
    border: 1px solid #d8c6f2;
    padding: 18px;
    border-radius: 16px;
    margin-top: 12px;
">
    <div style="
        color: #5c2ca3;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
    ">
        AI Summary
    </div>

    <div style="
        color: #2b2b2b;
        font-size: 15px;
        line-height: 1.6;
    ">
        {summary}
    </div>
</div>
""",
    unsafe_allow_html=True
)

if st.button("✦ Explain Results"):

    with st.spinner("Generating summary..."):

        try:
            ai_response = requests.get(
                f"{API_BASE}/api/ai/explain/{selected_id}",
                timeout=120
            )

            ai_response.raise_for_status()

            ai_data = ai_response.json()

            summary = ai_data.get(
                "summary",
                "No summary was returned."
            )

            st.markdown(
                f"""
                <div class="ai-card">
                    <div class="ai-title">AI Summary</div>
                    {summary}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"AI summary failed: {e}")