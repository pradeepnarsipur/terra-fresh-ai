import streamlit as st

from services.supabase_database import create_product_supabase


def render_seller_dashboard_page():

    if not st.session_state.get("logged_in"):
        st.warning("Please login first")
        return

    st.title("Seller Dashboard")

    st.success(
        f"Welcome {st.session_state['seller_name']}"
    )

    st.subheader("Add Product")

    product_name = st.text_input(
        "Product Name"
    )

    category = st.text_input(
        "Category"
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        step=1.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=0,
        step=1
    )

    description = st.text_area(
        "Description"
    )

    if st.button("Add Product"):

        if not product_name.strip():

            st.error(
                "Please enter product name"
            )

        else:

            try:

                create_product_supabase(
                    st.session_state["seller_id"],
                    product_name,
                    category,
                    price,
                    quantity,
                    description
                )

                st.success(
                    "Product added successfully"
                )

            except Exception as e:

                st.error(
                    f"Failed to add product: {e}"
                )