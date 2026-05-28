import streamlit as st

from components.common import render_result_card
from components.styles import inject_global_styles
from services.ai_advisor import GROQ_MODEL, MISSING_KEY_MESSAGE, get_api_key, get_recommendation


def render_ai_advisor_page() -> None:
    st.markdown("## 🌱 AI Advisor")
    st.markdown(
        '<p class="section-subtitle">Smart crop insights powered by cloud AI - enter your field data and get tailored guidance.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("#### Plant Symptom Guidance")
    st.markdown(
        "- Add clear symptom details such as yellowing, wilting, spots, or stunted growth.\n"
        "- Include severity and where symptoms appear (roots, lower leaves, new leaves).\n"
        "- Mention how long symptoms have been visible for more accurate recommendations."
    )

    if not get_api_key():
        st.error(MISSING_KEY_MESSAGE)

    with st.form("crop_form", clear_on_submit=False):
        col_left, col_right = st.columns(2)

        with col_left:
            crop_name = st.text_input("Crop name", placeholder="e.g. Tomato, Wheat, Rice")
            ph_value = st.number_input("pH value", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
            temperature = st.number_input("Temperature (C)", min_value=-20.0, max_value=60.0, value=25.0, step=0.5)

        with col_right:
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
            plant_symptoms = st.text_area(
                "Plant symptoms",
                placeholder="e.g. yellowing leaves, brown spots, wilting, stunted growth",
                height=120,
            )

        submitted = st.form_submit_button("Get AI Recommendation", disabled=not get_api_key())

    if submitted:
        if not crop_name.strip():
            st.warning("Please enter a crop name before requesting a recommendation.")
        else:
            with st.spinner(f"Analyzing with {GROQ_MODEL}..."):
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
                    st.markdown("### AI Recommendation")
                    render_result_card("Plant Health Summary", "💚", result.get("plant_health_summary", "-"))
                    render_result_card("Nutrient Recommendation", "🧪", result.get("nutrient_recommendation", "-"))
                    render_result_card("Possible Disease / Issues", "🔍", result.get("possible_disease_issues", "-"))
                    render_result_card("Suggested Action", "✅", result.get("suggested_action", "-"))

    st.caption(f"Terra Fresh AI · Powered by Groq · Model: {GROQ_MODEL}")


def render_ai_advisor_standalone() -> None:
    st.set_page_config(
        page_title="Terra Fresh AI Advisor",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_global_styles()
    render_ai_advisor_page()


if __name__ == "__main__":
    render_ai_advisor_standalone()
