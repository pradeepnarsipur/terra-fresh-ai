import streamlit as st
import hashlib

from services.supabase_database import get_seller_by_whatsapp_supabase


def render_login_page():
    st.title("Seller Login")

    whatsapp = st.text_input("WhatsApp Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        seller = get_seller_by_whatsapp_supabase(whatsapp)

        if seller is None:
            st.error("Seller not found")

        else:
            password_hash = hashlib.sha256(
                password.encode()
            ).hexdigest()

            stored_hash = seller["password_hash"]

            if password_hash == stored_hash:
                st.session_state["logged_in"] = True
                st.session_state["seller_id"] = seller["id"]
                st.session_state["seller_name"] = seller["business_name"]

                st.session_state["redirect_dashboard"] = True
                st.rerun()
            else:
                st.error("Invalid password")