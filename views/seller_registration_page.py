import streamlit as st
import hashlib

from services.supabase_database import create_seller_supabase


def render_seller_registration_page():

    st.title("Seller Registration")

    full_name = st.text_input(
        "Full Name",
        key="full_name"
    )

    business_name = st.text_input(
        "Business Name",
        key="business_name"
    )

    whatsapp = st.text_input(
        "WhatsApp Number",
        key="whatsapp"
    )

    city = st.text_input(
        "City",
        key="city"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    if st.button("Register"):

        if (
            not full_name.strip()
            or not business_name.strip()
            or not whatsapp.strip()
            or not city.strip()
            or not password.strip()
            or not confirm_password.strip()
        ):
            st.error("Please fill all required fields")

        elif password != confirm_password:
            st.error("Passwords do not match")

        else:

            password_hash = hashlib.sha256(
                password.encode()
            ).hexdigest()

            try:

                create_seller_supabase(
                    full_name,
                    business_name,
                    whatsapp,
                    city,
                    password_hash
                )

                st.success(
                    "Registration successful! Please login to continue."
                )

            except Exception as e:

                if "duplicate key value" in str(e):

                    st.error(
                        "This WhatsApp number is already registered. Please login or use a different number."
                    )

                else:

                    st.error(
                        "Registration failed. Please try again."
                    )