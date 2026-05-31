import streamlit as st
from dotenv import load_dotenv

from services.database import init_database
from components.styles import inject_global_styles

from views.home_page import render_home_page
from views.ai_advisor_page import render_ai_advisor_page
from views.marketplace_page import render_marketplace_page
from views.seller_registration_page import render_seller_registration_page
from views.login_page import render_login_page
from views.seller_dashboard_page import render_seller_dashboard_page


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

# --------------------
# SIDEBAR
# --------------------

with st.sidebar:

    st.markdown("## Terra Fresh")

    if st.session_state.get("logged_in"):

        nav_options = [
            "Home",
            "Marketplace",
            "AI Advisor",
            "Seller Dashboard",
            "Logout"
        ]

    else:

        nav_options = [
            "Home",
            "Marketplace",
            "AI Advisor",
            "Seller Registration",
            "Login"
        ]

    selected_page = st.radio(
        "Navigation",
        options=nav_options,
        index=0,
        key="sidebar_navigation_radio"
    )

# --------------------
# LOGIN REDIRECT
# --------------------

if st.session_state.get("redirect_dashboard"):

    st.session_state["redirect_dashboard"] = False

    render_seller_dashboard_page()

    st.stop()

# --------------------
# ROUTING
# --------------------

if selected_page == "Home":

    render_home_page()

elif selected_page == "Marketplace":

    render_marketplace_page()

elif selected_page == "AI Advisor":

    render_ai_advisor_page()

elif selected_page == "Seller Registration":

    render_seller_registration_page()

elif selected_page == "Login":

    render_login_page()

elif selected_page == "Seller Dashboard":

    render_seller_dashboard_page()

elif selected_page == "Logout":

    st.session_state.clear()

    st.rerun()

else:

    st.warning("Please select a valid page.")