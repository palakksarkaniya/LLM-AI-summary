import streamlit as st
import requests

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CarerBridge AI Summary",
    page_icon="💜",
    layout="centered"
)

# Deployed FastAPI backend
API_BASE = "https://llm-ai-summary.onrender.com"


# =========================================================
# STYLING
# =========================================================

st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: #f8f6fb;
}

.block-container {
    max-width: 500px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}


/* CarerBridge header */
.cb-header {
    background-color: white;
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 16px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
}

.cb-brand {
    color: #5c2ca3;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}


/* Purple + green navigation */
.cb-tabs {
    display: flex;
    width: 100%;
    overflow: hidden;
    border-radius: 9px;
}

.cb-tab-purple {
    width: 50%;
    background-color: #6427a6;
    color: white;
    padding: 10px;
    text-align: center;
    font-size: 13px;
    font-weight: 600;
}

.cb-tab-green {
    width: 50%;
    background-color: #12664f;
    color: white;
    padding: 10px;
    text-align: center;
    font-size: 13px;
    font-weight: 600;
}


/* Cards */
.cb-card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
}

.cb-facility-name {
    color: #222222;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 5px;
}

.cb-muted {
    color: #707070;
    font-size: 14px;
    line-height: 1.5;
}

.cb-section-title {
    color: #303030;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 14px;
}


/* Metrics */
.cb-metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 11px;
    gap: 20px;
}

.cb-metric-label {
    color: #555555;
    font-size: 14px;
}

.cb-metric-value {
    color: #292929;
    font-size: 14px;
    font-weight: 600;
}


/* Explain button */
div.stButton > button {
    width: 100%;
    background-color: #6427a6;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-weight: 600;
    font-size: 15px;
}

div.stButton > button:hover {
    background-color: #54208e;
    color: white;
    border: none;
}

div.stButton > button:focus {
    color: white;
    border: none;
}


/* AI summary */
.ai-card {
    background-color: #f3ebff;
    border: 1px solid #d8c6f2;
    padding: 20px;
    border-radius: 18px;
    margin-top: 16px;
}

.ai-title {
    color: #5c2ca3 !important;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
}

.ai-text {
    color: #292929 !important;
    font-size: 15px;
    line-height: 1.65;
}


/* Selectbox */
div[data-baseweb="select"] > div {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
"""
<div class="cb-header">
<div class="cb-brand">CarerBridge</div>

<div class="cb-tabs">
<div class="cb-tab-purple">CareNavigator</div>
<div class="cb-tab-green">Carer Space</div>
</div>
</div>
""",
unsafe_allow_html=True
)


# =========================================================
# LOAD FACILITY LIST
# =========================================================

try:

    response = requests.get(
        f"{API_BASE}/api/facilities",
        timeout=60
    )

    response.raise_for_status()

    facilities = response.json()

except Exception as e:

    st.error(
        f"Could not load facilities. Please try again. Error: {e}"
    )

    st.stop()


# =========================================================
# FACILITY SEARCH / SELECT
# =========================================================

st.markdown("### Find a care service")

facility_options = {}

for facility in facilities:

    name = facility.get(
        "facility_name",
        "Unknown facility"
    )

    suburb = facility.get(
        "suburb",
        ""
    )

    state = facility.get(
        "state",
        ""
    )

    facility_id = facility.get(
        "facility_id"
    )

    label = f"{name} — {suburb}, {state}"

    facility_options[label] = facility_id


selected_label = st.selectbox(
    "Search or select a facility",
    options=list(facility_options.keys())
)

selected_id = facility_options[selected_label]


# =========================================================
# LOAD SELECTED FACILITY DETAILS
# =========================================================

try:

    response = requests.get(
        f"{API_BASE}/api/facilities/{selected_id}/details",
        timeout=60
    )

    response.raise_for_status()

    facility = response.json()

except Exception as e:

    st.error(
        f"Could not load facility details. Error: {e}"
    )

    st.stop()


# =========================================================
# FACILITY INFORMATION
# =========================================================

facility_name = facility.get(
    "facility_name",
    "Facility"
)

provider_name = facility.get(
    "provider_name",
    ""
)

care_type = facility.get(
    "care_type",
    ""
)

address = facility.get(
    "address",
    {}
)

suburb = address.get(
    "suburb",
    ""
)

state = address.get(
    "state",
    ""
)


st.markdown(
f"""
<div class="cb-card">

<div class="cb-facility-name">
{facility_name}
</div>

<div class="cb-muted">
{provider_name}
</div>

<div class="cb-muted">
{care_type}
</div>

<div class="cb-muted">
{suburb}, {state}
</div>

</div>
""",
unsafe_allow_html=True
)


# =========================================================
# CARE QUALITY
# =========================================================

care_quality = facility.get(
    "care_quality",
    {}
)

st.markdown(
"""
<div class="cb-card">
<div class="cb-section-title">
Care Quality
</div>
""",
unsafe_allow_html=True
)


quality_rows = [

    (
        "Overall",
        care_quality.get("overall_rating")
    ),

    (
        "Resident Experience",
        care_quality.get(
            "resident_experience_rating"
        )
    ),

    (
        "Staffing",
        care_quality.get(
            "staffing_rating"
        )
    ),

    (
        "Compliance",
        care_quality.get(
            "compliance_rating"
        )
    ),

    (
        "Quality Measures",
        care_quality.get(
            "quality_measures_rating"
        )
    )

]


for label, value in quality_rows:

    display_value = (
        value
        if value is not None
        else "N/A"
    )

    st.markdown(
    f"""
<div class="cb-metric-row">
<span class="cb-metric-label">
{label}
</span>

<span class="cb-metric-value">
{display_value}
</span>
</div>
""",
    unsafe_allow_html=True
    )


st.markdown(
"</div>",
unsafe_allow_html=True
)


# =========================================================
# VISIT PRACTICALITY
# =========================================================

visit = facility.get(
    "visit_practicality",
    {}
)

st.markdown(
"""
<div class="cb-card">
<div class="cb-section-title">
Visit Practicality
</div>
""",
unsafe_allow_html=True
)


visit_rows = [

    (
        "Public Transport",
        visit.get(
            "public_transport_score"
        )
    ),

    (
        "Parking",
        visit.get(
            "parking_score"
        )
    ),

    (
        "Accessible Toilets",
        visit.get(
            "accessible_toilet_score"
        )
    )

]


for label, value in visit_rows:

    if isinstance(value, float):
        display_value = round(value, 1)

    elif value is None:
        display_value = "N/A"

    else:
        display_value = value


    st.markdown(
    f"""
<div class="cb-metric-row">

<span class="cb-metric-label">
{label}
</span>

<span class="cb-metric-value">
{display_value}
</span>

</div>
""",
    unsafe_allow_html=True
    )


st.markdown(
"</div>",
unsafe_allow_html=True
)


# =========================================================
# AI EXPLANATION SECTION
# =========================================================

st.markdown(
"""
<div class="cb-card">

<div class="cb-section-title">
AI Summary
</div>

<div class="cb-muted">
Get a short explanation of what stands out in these results.
</div>

</div>
""",
unsafe_allow_html=True
)


# =========================================================
# EXPLAIN RESULTS BUTTON
# =========================================================

if st.button(
    "✦ Explain Results",
    use_container_width=True
):

    with st.spinner(
        "Explaining these results..."
    ):

        try:

            ai_response = requests.get(
                f"{API_BASE}/api/ai/explain/{selected_id}",
                timeout=120
            )

            ai_response.raise_for_status()

            ai_data = ai_response.json()

            summary = ai_data.get(
                "summary",
                "No AI summary was returned."
            )


            # AI SUMMARY CARD
            st.markdown(
            f"""
<div class="ai-card">

<div class="ai-title">
AI Summary
</div>

<div class="ai-text">
{summary}
</div>

</div>
""",
            unsafe_allow_html=True
            )


        except requests.exceptions.Timeout:

            st.error(
                "The AI took too long to respond. Please try again."
            )


        except Exception as e:

            st.error(
                f"AI summary could not be generated. Error: {e}"
            )