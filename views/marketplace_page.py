import streamlit as st

from components.styles import inject_global_styles
from data.growers import NEARBY_GROWERS
from data.products import PRODUCTS


def render_marketplace_page() -> None:
    st.markdown("## Grow Fresh. Sell Local.")
    st.markdown(
        '<p class="section-subtitle">AI Powered Terrace Farming Ecosystem for neighborhood growers, buyers, and home entrepreneurs.</p>',
        unsafe_allow_html=True,
    )

    st.markdown("### Start Selling From Home")
    st.info(
        "You can start with a small terrace setup, grow clean hydroponic produce, "
        "and sell directly to nearby families. Terra Fresh helps you start, grow, and earn locally."
    )
    st.markdown(
        """
        <div style="background:#ffffff;border:1px solid #bbf7d0;border-radius:14px;padding:1rem 1.15rem;margin-bottom:1rem;">
            <h4 style="margin:0;color:#14532d;">Become a Local Seller</h4>
            <p style="margin:0.45rem 0 0;color:#4b5563;">Set up a terrace grow unit, list your daily harvest, and connect with WhatsApp buyers in your area.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "show_sell_form" not in st.session_state:
        st.session_state.show_sell_form = False

    if st.button("Sell Your Product", type="primary", key="sell_product_toggle"):
        st.session_state.show_sell_form = not st.session_state.show_sell_form

    if st.session_state.show_sell_form:
        with st.form("sell_product_form", clear_on_submit=True):
            seller_name = st.text_input("Seller Name")
            product_name = st.text_input("Product Name")
            product_category = st.selectbox(
                "Category",
                options=["Produce", "Seeds", "Nutrients", "Equipment"],
                key="seller_product_category",
            )
            product_price = st.text_input("Price")
            whatsapp_number = st.text_input("WhatsApp Number")
            product_description = st.text_area("Product Description", height=100)
            submit_sell = st.form_submit_button("Submit Product")

        if submit_sell:
            if all(
                [
                    seller_name.strip(),
                    product_name.strip(),
                    product_category.strip(),
                    product_price.strip(),
                    whatsapp_number.strip(),
                    product_description.strip(),
                ]
            ):
                st.success("Product submitted successfully")
            else:
                st.warning("Please fill in all fields before submitting.")

    st.markdown("### Nearby Growers")
    grower_cols = st.columns(3)
    for idx, grower in enumerate(NEARBY_GROWERS):
        with grower_cols[idx % 3]:
            st.image(grower["image"], use_container_width=True)
            st.markdown(f"#### {grower['name']}")
            st.markdown('<span class="badge">Terrace Grower</span>', unsafe_allow_html=True)
            st.write(f"📍 {grower['location']}")
            st.write(f"🌾 Crops: {', '.join(grower['products'])}")
            st.write(f"🧠 Experience: {grower['experience']}")
            wa_url = f"https://wa.me/{grower['whatsapp']}?text=Hello%20I%20am%20interested%20in%20your%20produce."
            st.link_button(
                "WhatsApp Contact",
                wa_url,
                use_container_width=True,
                key=f"grower_wa_{idx}",
            )

    st.markdown("---")
    st.markdown("### Seller Profiles")
    profile_cols = st.columns(3)
    for idx, grower in enumerate(NEARBY_GROWERS):
        with profile_cols[idx % 3]:
            st.markdown(
                f"""
                <div style="background:#ffffff;border:1px solid #dcfce7;border-radius:14px;padding:1rem;min-height:200px;">
                    <p style="margin:0;color:#14532d;font-weight:700;">{grower["name"]}</p>
                    <p style="margin:0.35rem 0;color:#4b5563;">{grower["location"]}</p>
                    <p style="margin:0.3rem 0;color:#374151;"><b>Crops grown:</b> {", ".join(grower["products"])}</p>
                    <p style="margin:0.3rem 0;color:#374151;"><b>Experience:</b> {grower["experience"]}</p>
                    <p style="margin:0.3rem 0;color:#374151;"><b>Available products:</b> {", ".join(grower["products"][:2])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### Nearby Produce Listings")
    categories = ["All", "Produce", "Seeds", "Nutrients", "Equipment"]
    selected_category = st.selectbox("Filter by Category", options=categories, index=0)
    filtered_products = PRODUCTS if selected_category == "All" else [p for p in PRODUCTS if p["category"] == selected_category]

    cols_per_row = 3
    for start in range(0, len(filtered_products), cols_per_row):
        row_items = filtered_products[start : start + cols_per_row]
        cols = st.columns(cols_per_row)
        for i, product in enumerate(row_items):
            with cols[i]:
                st.image(product["image"], use_container_width=True)
                st.markdown(f"#### {product['name']}")
                badge = "🟢 Fresh Today" if product.get("fresh_today") else "Community Listing"
                st.caption(badge)
                st.write(f"Price: {product['price']}")
                st.write(f"Category: {product['category']}")
                st.write(product["description"])
                wa_message = f"Hello Terra Fresh, I am interested in {product['name']}."
                wa_url = f"https://wa.me/919999999999?text={wa_message.replace(' ', '%20')}"
                st.link_button(
                    "WhatsApp Contact",
                    wa_url,
                    use_container_width=True,
                    key=f"product_wa_{start}_{i}_{product['name']}",
                )


def render_marketplace_standalone() -> None:
    st.set_page_config(
        page_title="Terra Fresh Marketplace",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_global_styles()
    render_marketplace_page()


if __name__ == "__main__":
    render_marketplace_standalone()
