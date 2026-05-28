import streamlit as st

from data.growers import NEARBY_GROWERS


def render_home_page() -> None:
    st.write("Home page loaded")
    st.markdown(
        """
        <div class="home-hero">
            <span class="hero-pill">Sustainable Urban Farming</span>
            <h1>Grow Fresh. Sell Local.</h1>
            <p>Turn your terrace into an AI-powered hydroponic farm and connect with local buyers. Build cleaner food systems while creating reliable neighborhood income.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta1, cta2, cta3 = st.columns(3)
    with cta1:
        if st.button("Start Selling", use_container_width=True, key="home_cta_selling", type="primary"):
            st.info("Go to 'Marketplace' from the sidebar to start selling.")
    with cta2:
        if st.button("Explore Marketplace", use_container_width=True, key="home_cta_marketplace"):
            st.info("Open 'Marketplace' from the sidebar to explore products and growers.")
    with cta3:
        if st.button("Use AI Advisor", use_container_width=True, key="home_cta_ai"):
            st.info("Open 'AI Advisor' from the sidebar for crop recommendations.")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Platform Overview")
    ov1, ov2, ov3 = st.columns(3)
    with ov1:
        st.info("🌱 AI crop recommendations based on pH, temperature, humidity, and symptoms.")
    with ov2:
        st.info("🛒 Community marketplace to discover nearby hydroponic produce and supplies.")
    with ov3:
        st.info("🏡 Enable terrace growers to list and sell locally using WhatsApp-first workflows.")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Nearby Growers Preview")
    grower_cols = st.columns(3)
    for idx, grower in enumerate(NEARBY_GROWERS):
        with grower_cols[idx]:
            st.image(grower["image"], use_container_width=True)
            st.markdown(f"**{grower['name']}**")
            st.markdown('<span class="badge">Terrace Grower</span>', unsafe_allow_html=True)
            st.caption(grower["location"])
