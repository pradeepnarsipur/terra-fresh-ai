import json
import re

import ollama
import streamlit as st

OLLAMA_MODEL = "qwen2.5:1.5b"

st.set_page_config(
    page_title="Terra Fresh AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

    .stApp {
        background: linear-gradient(165deg, #f0fdf4 0%, #ecfdf5 35%, #f8fafc 100%);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent; }

    .terra-hero {
        text-align: center;
        padding: 1.5rem 1rem 2rem;
        margin-bottom: 0.5rem;
    }
    .terra-hero h1 {
        font-size: 2.4rem;
        font-weight: 700;
        color: #14532d;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .terra-hero p {
        color: #4b5563;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        max-width: 520px;
        margin-left: auto;
        margin-right: auto;
    }

    [data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #d1fae5;
        border-radius: 16px;
        padding: 1.5rem 1.75rem 1.25rem;
        box-shadow: 0 4px 24px rgba(20, 83, 45, 0.06);
    }

    .stTextInput > label, .stNumberInput > label, .stTextArea > label {
        font-weight: 600 !important;
        color: #166534 !important;
    }

    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.65rem 1.5rem !important;
        width: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        box-shadow: 0 8px 20px rgba(22, 163, 74, 0.35) !important;
        transform: translateY(-1px);
    }

    .result-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #22c55e;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    }
    .result-card h3 {
        color: #14532d;
        font-size: 1.1rem;
        margin: 0 0 0.65rem 0;
        font-weight: 600;
    }
    .result-card p, .result-card li {
        color: #374151;
        line-height: 1.6;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="terra-hero">
        <h1>🌱 Terra Fresh AI</h1>
        <p>Smart crop insights powered by local AI — enter your field data and get tailored plant care guidance.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def build_prompt(crop: str, ph: float, temp: float, humidity: float, symptoms: str) -> str:
    return f"""You are Terra Fresh AI, an expert agronomist assistant.

Analyze the following crop conditions and respond ONLY with valid JSON (no markdown fences) using this exact structure:
{{
  "plant_health_summary": "2-4 sentences on overall plant health",
  "nutrient_recommendation": "specific nutrients, amounts or ratios if applicable",
  "possible_disease_issues": "likely diseases, pests, or environmental issues",
  "suggested_action": "clear step-by-step actions the farmer should take"
}}

Crop data:
- Crop: {crop}
- Soil pH: {ph}
- Temperature (°C): {temp}
- Humidity (%): {humidity}
- Plant symptoms: {symptoms or "None reported"}

Be practical, concise, and actionable. Base advice on the provided values and symptoms."""


def parse_ai_response(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {
        "plant_health_summary": text,
        "nutrient_recommendation": "Could not parse structured response. See summary above.",
        "possible_disease_issues": "—",
        "suggested_action": "Retry or check Ollama model output.",
    }


def get_recommendation(crop: str, ph: float, temp: float, humidity: float, symptoms: str) -> dict:
    prompt = build_prompt(crop, ph, temp, humidity, symptoms)
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response["message"]["content"]
    return parse_ai_response(content)


def render_result_card(title: str, icon: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="result-card">
            <h3>{icon} {title}</h3>
            <p>{body.replace(chr(10), "<br>")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.form("crop_form", clear_on_submit=False):
    col_left, col_right = st.columns(2)

    with col_left:
        crop_name = st.text_input("Crop name", placeholder="e.g. Tomato, Wheat, Rice")
        ph_value = st.number_input("pH value", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=-20.0,
            max_value=60.0,
            value=25.0,
            step=0.5,
        )

    with col_right:
        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0,
        )
        plant_symptoms = st.text_area(
            "Plant symptoms",
            placeholder="e.g. yellowing leaves, brown spots, wilting, stunted growth…",
            height=120,
        )

    submitted = st.form_submit_button("Get AI Recommendation")

if submitted:
    if not crop_name.strip():
        st.warning("Please enter a crop name before requesting a recommendation.")
    else:
        with st.spinner(f"Analyzing with {OLLAMA_MODEL}…"):
            try:
                result = get_recommendation(
                    crop=crop_name.strip(),
                    ph=ph_value,
                    temp=temperature,
                    humidity=humidity,
                    symptoms=plant_symptoms.strip(),
                )
            except Exception as exc:
                st.error(
                    f"Could not reach Ollama. Ensure Ollama is running and the model is installed:\n\n"
                    f"`ollama pull {OLLAMA_MODEL}`\n\n"
                    f"Error: {exc}"
                )
            else:
                st.markdown("### 📋 AI Recommendation")
                render_result_card(
                    "Plant Health Summary",
                    "💚",
                    result.get("plant_health_summary", "—"),
                )
                render_result_card(
                    "Nutrient Recommendation",
                    "🧪",
                    result.get("nutrient_recommendation", "—"),
                )
                render_result_card(
                    "Possible Disease / Issues",
                    "🔍",
                    result.get("possible_disease_issues", "—"),
                )
                render_result_card(
                    "Suggested Action",
                    "✅",
                    result.get("suggested_action", "—"),
                )

st.caption("Terra Fresh AI · Local inference via Ollama · Model: qwen2.5:1.5b")
