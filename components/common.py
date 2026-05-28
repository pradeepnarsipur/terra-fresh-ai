import streamlit as st


def render_brand_banner() -> None:
    st.markdown(
        """
        <div class="brand-banner">
            <div class="brand-icon-wrap">🌿</div>
            <h1 class="brand-title">Terra Fresh</h1>
            <p class="brand-subtitle">AI Powered Hydroponics & Marketplace Platform</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(title: str, icon: str, body: str) -> None:
    st.markdown(
        f"""
        <div style="background:#ffffff;border:1px solid #e5e7eb;border-left:4px solid #22c55e;border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:0.9rem;">
            <h3 style="color:#14532d;margin:0 0 0.6rem 0;">{icon} {title}</h3>
            <p style="color:#374151;line-height:1.6;margin:0;">{body.replace(chr(10), "<br>")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
