import streamlit as st

from data.growers import NEARBY_GROWERS
from services.supabase_database import (
    get_all_products_supabase,
    get_seller_by_id_supabase
)


def render_marketplace_page():

    st.title("Marketplace")

    st.markdown("### Nearby Growers")

    grower_cols = st.columns(3)

    for idx, grower in enumerate(NEARBY_GROWERS):

        with grower_cols[idx % 3]:

            st.image(
                grower["image"],
                use_container_width=True
            )

            st.subheader(
                grower["name"]
            )

            st.write(
                f"📍 {grower['location']}"
            )

            st.write(
                f"🌾 Crops: {', '.join(grower['products'])}"
            )

            st.write(
                f"🧠 Experience: {grower['experience']}"
            )

    st.divider()

    st.markdown("### Marketplace Products")

    products = get_all_products_supabase()

    if not products:

        st.info(
            "No products available yet."
        )

    else:

        for product in products:

            with st.container():

                st.subheader(
                    product["product_name"]
                )

                st.write(
                    f"📦 Category: {product['category']}"
                )

                st.write(
                    f"💰 Price: ₹{product['price']}"
                )

                st.write(
                    f"📊 Quantity: {product['quantity']}"
                )

                seller = get_seller_by_id_supabase(
                    product["seller_id"]
                )

                if seller:

                    st.write(
                        f"🏪 Seller: {seller['business_name']}"
                    )

                    st.write(
                        f"📱 WhatsApp: {seller['whatsapp']}"
                    )

                    whatsapp_url = (
                        f"https://wa.me/91{seller['whatsapp']}"
                        f"?text=Hello%20I%20am%20interested%20in%20{product['product_name']}"
                    )

                    st.link_button(
                        "Contact Seller",
                        whatsapp_url
                    )

                st.write(
                    f"📝 Description: {product['description']}"
                )

                st.divider()