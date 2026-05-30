import streamlit as st
from dotenv import load_dotenv


from services.database import init_database
from components.styles import inject_global_styles
from pages.ai_advisor_page import render_ai_advisor_page
from pages.home_page import render_home_page
from pages.marketplace_page import render_marketplace_page


load_dotenv()
init_database()

st.set_page_config(
    page_title="Terra Fresh AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()
st.markdown("### Terra Fresh Platform")

with st.sidebar:
    st.markdown("## Terra Fresh")
    selected_page = st.radio(
        "Navigation",
        options=["Home", "AI Advisor", "Marketplace"],
        index=0,
        key="sidebar_navigation_radio",
    )

if selected_page == "Home":
    render_home_page()
elif selected_page == "AI Advisor":
    render_ai_advisor_page()
elif selected_page == "Marketplace":
    render_marketplace_page()
else:
    st.warning("Please select a valid page from the sidebar.")
