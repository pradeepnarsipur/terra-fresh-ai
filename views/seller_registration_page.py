import streamlit as st
import hashlib

from services.database import create_seller


def render_seller_registration_page():
    st.write("Seller Registration Loaded")
    st.title("Seller Registration")

    full_name = st.text_input("Full Name")
    business_name = st.text_input("Business Name")
    whatsapp = st.text_input("WhatsApp Number")
    city = st.text_input("City")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):

        if password != confirm_password:
            st.error("Passwords do not match")

        elif not full_name or not business_name or not whatsapp or not city:
            st.error("Please fill all fields")

        else:
            password_hash = hashlib.sha256(
                password.encode()
            ).hexdigest()

            try:
                create_seller(
                    full_name,
                    business_name,
                    whatsapp,
                    city,
                    password_hash
                )

                st.success("Registration successful")

            except Exception as e:
                st.error(f"Registration failed: {e}")