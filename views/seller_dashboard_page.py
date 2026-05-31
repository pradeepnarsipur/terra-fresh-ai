import streamlit as st


def render_seller_dashboard_page():

    if not st.session_state.get("logged_in"):

        st.warning("Please login first")
        return

    st.title("Seller Dashboard")

    st.success(
        f"Welcome {st.session_state['seller_name']}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Products", "0")

    with col2:
        st.metric("Orders", "0")

    with col3:
        st.metric("Revenue", "₹0")

    st.divider()

