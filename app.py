import json
import os
import re

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_MODEL = "llama-3.1-8b-instant"
MISSING_KEY_MESSAGE = "Groq API key missing"
WHATSAPP_NUMBER = "919999999999"

PRODUCTS = [
    {
        "name": "Lettuce",
        "price": "₹120 / kg",
        "category": "Produce",
        "description": "Fresh hydroponic lettuce with crisp texture and high nutrition.",
        "image": "https://images.unsplash.com/photo-1556801712-76c8eb07bbc9?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Spinach",
        "price": "₹95 / bunch",
        "category": "Produce",
        "description": "Pesticide-free spinach harvested from controlled hydroponic systems.",
        "image": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Hydroponic Nutrients",
        "price": "₹1,450 / kit",
        "category": "Nutrients",
        "description": "Balanced A+B nutrient formula for fast and healthy vegetative growth.",
        "image": "https://images.unsplash.com/photo-1584473457409-ce9d1ac572f9?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Grow Lights",
        "price": "₹3,999 / unit",
        "category": "Equipment",
        "description": "Full-spectrum LED grow light for indoor hydroponic farming.",
        "image": "https://images.unsplash.com/photo-1632204901225-ef1c5e5f963b?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Seeds",
        "price": "₹350 / pack",
        "category": "Seeds",
        "description": "High-germination hydroponic seed mix for leafy greens and herbs.",
        "image": "https://images.unsplash.com/photo-1615486363972-a9004f6f1044?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "NFT Pipes",
        "price": "₹2,250 / set",
        "category": "Equipment",
        "description": "Food-grade NFT channels and pipes for efficient nutrient flow.",
        "image": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=80",
    },
]

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

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #14532d 0%, #166534 100%);
    }
    [data-testid="stSidebar"] * {
        color: #ecfdf5 !important;
    }
    [data-testid="stSidebar"] .stRadio > label {
        color: #bbf7d0 !important;
        font-weight: 600 !important;
    }

    .market-header {
        text-align: center;
        margin: 0.25rem 0 1.5rem;
    }
    .market-header h2 {
        color: #14532d;
        margin-bottom: 0.4rem;
    }
    .market-header p {
        color: #4b5563;
        max-width: 640px;
        margin: 0 auto;
    }
    .product-card {
        background: #ffffff;
        border: 1px solid #dcfce7;
        border-radius: 14px;
        padding: 1rem 1rem 1.15rem;
        margin-bottom: 1rem;
        box-shadow: 0 6px 18px rgba(20, 83, 45, 0.07);
        min-height: 530px;
    }
    .product-image {
        width: 100%;
        height: 185px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 0.9rem;
    }
    .product-name {
        color: #14532d;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .product-meta {
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;
        margin-bottom: 0.55rem;
        font-size: 0.9rem;
    }
    .product-price {
        color: #047857;
        font-weight: 700;
    }
    .product-category {
        color: #166534;
        background: #dcfce7;
        border-radius: 999px;
        padding: 0.12rem 0.6rem;
        font-weight: 600;
    }
    .product-description {
        color: #374151;
        font-size: 0.95rem;
        line-height: 1.5;
        min-height: 66px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_api_key() -> str | None:
    key = (os.getenv("GROQ_API_KEY") or "").strip()
    return key or None


def get_groq_client() -> Groq:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(MISSING_KEY_MESSAGE)
    return Groq(api_key=api_key)


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
        "suggested_action": "Retry or check the model response format.",
    }


def get_recommendation(crop: str, ph: float, temp: float, humidity: float, symptoms: str) -> dict:
    client = get_groq_client()
    prompt = build_prompt(crop, ph, temp, humidity, symptoms)

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1024,
    )

    content = completion.choices[0].message.content or ""
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


def render_ai_advisor_page() -> None:
    st.markdown(
        """
        <div class="terra-hero">
            <h1>🌱 Terra Fresh AI</h1>
            <p>Smart crop insights powered by cloud AI — enter your field data and get tailored plant care guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not get_api_key():
        st.error(MISSING_KEY_MESSAGE)

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

        submitted = st.form_submit_button("Get AI Recommendation", disabled=not get_api_key())

    if submitted:
        if not crop_name.strip():
            st.warning("Please enter a crop name before requesting a recommendation.")
        else:
            with st.spinner(f"Analyzing with {GROQ_MODEL}…"):
                try:
                    result = get_recommendation(
                        crop=crop_name.strip(),
                        ph=ph_value,
                        temp=temperature,
                        humidity=humidity,
                        symptoms=plant_symptoms.strip(),
                    )
                except RuntimeError as exc:
                    st.error(str(exc))
                except Exception as exc:
                    st.error(
                        "Could not get a recommendation from Groq. "
                        "Check your API key, network connection, and Groq service status.\n\n"
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

    st.caption(f"Terra Fresh AI · Powered by Groq · Model: {GROQ_MODEL}")


def render_marketplace_page() -> None:
    st.markdown(
        """
        <div class="market-header">
            <h2>🛒 Terra Fresh Marketplace</h2>
            <p>Discover premium hydroponic produce and farming essentials curated for modern agriculture.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    categories = ["All", "Produce", "Seeds", "Nutrients", "Equipment"]
    selected_category = st.selectbox("Filter by Category", options=categories, index=0)

    filtered_products = PRODUCTS
    if selected_category != "All":
        filtered_products = [product for product in PRODUCTS if product["category"] == selected_category]

    if not filtered_products:
        st.info("No products found for this category.")
        return

    cols_per_row = 3
    for idx in range(0, len(filtered_products), cols_per_row):
        row_items = filtered_products[idx : idx + cols_per_row]
        cols = st.columns(cols_per_row)
        for col_idx, product in enumerate(row_items):
            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div class="product-card">
                        <img class="product-image" src="{product["image"]}" alt="{product["name"]}">
                        <div class="product-name">{product["name"]}</div>
                        <div class="product-meta">
                            <span class="product-price">{product["price"]}</span>
                            <span class="product-category">{product["category"]}</span>
                        </div>
                        <div class="product-description">{product["description"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                whatsapp_message = f"Hello Terra Fresh, I'm interested in {product['name']}."
                whatsapp_url = (
                    f"https://wa.me/{WHATSAPP_NUMBER}"
                    f"?text={whatsapp_message.replace(' ', '%20')}"
                )
                st.link_button("WhatsApp Contact", whatsapp_url, use_container_width=True)


with st.sidebar:
    st.markdown("## Terra Fresh")
    selected_page = st.radio("Navigation", options=["AI Advisor", "Marketplace"], index=0)

if selected_page == "AI Advisor":
    render_ai_advisor_page()
else:
    render_marketplace_page()
