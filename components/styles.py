import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&display=swap');

        .stApp {
            background: linear-gradient(165deg, #f0fdf4 0%, #ecfdf5 35%, #f8fafc 100%);
            font-family: 'DM Sans', sans-serif;
        }
        [data-testid="stHeader"] { background: transparent; }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #14532d 0%, #166534 100%);
        }
        [data-testid="stSidebar"] * { color: #ecfdf5 !important; }
        [data-testid="stSidebar"] .stRadio > label { color: #bbf7d0 !important; font-weight: 600 !important; }

        .brand-banner {
            background: linear-gradient(140deg, #ecfdf5 0%, #d1fae5 100%);
            border: 1px solid #bbf7d0;
            border-radius: 18px;
            padding: 1.4rem 1rem 1.2rem;
            text-align: center;
            margin: 0.35rem auto 1rem;
            max-width: 760px;
            box-shadow: 0 8px 26px rgba(20, 83, 45, 0.08);
        }
        .brand-icon-wrap {
            width: 72px;
            height: 72px;
            margin: 0 auto 0.65rem;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #22c55e, #166534);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ecfdf5;
            font-size: 2rem;
        }
        .brand-title { margin: 0; color: #14532d; font-size: 2rem; font-weight: 700; }
        .brand-subtitle { margin: 0.35rem auto 0; color: #4b5563; max-width: 640px; font-size: 1.02rem; }

        .section-title { color: #14532d; font-weight: 700; margin-top: 0.2rem; }
        .section-subtitle { color: #4b5563; }
        .badge { display: inline-block; background: #dcfce7; color: #166534; border-radius: 999px; padding: 0.2rem 0.55rem; font-size: 0.8rem; font-weight: 600; }

        .home-hero {
            background: linear-gradient(120deg, rgba(20,83,45,0.92), rgba(22,101,52,0.86)),
                        url('https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1600&q=80');
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            padding: 2rem 2rem 1.8rem;
            color: #ecfdf5;
            margin-bottom: 1.05rem;
            box-shadow: 0 14px 28px rgba(20, 83, 45, 0.18);
        }
        .home-hero h1 {
            margin: 0;
            font-size: 2.4rem;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }
        .home-hero p {
            margin: 0.7rem 0 0;
            max-width: 680px;
            color: #dcfce7;
            font-size: 1.08rem;
        }
        .hero-pill {
            display: inline-block;
            margin-bottom: 0.8rem;
            background: rgba(236, 253, 245, 0.2);
            color: #f0fdf4;
            border: 1px solid rgba(236, 253, 245, 0.38);
            border-radius: 999px;
            padding: 0.22rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .stats-card, .how-card, .featured-card {
            background: #ffffff;
            border: 1px solid #dcfce7;
            border-radius: 14px;
            padding: 1rem;
            box-shadow: 0 6px 18px rgba(20, 83, 45, 0.07);
            height: 100%;
        }
        .stats-value {
            color: #166534;
            font-size: 1.4rem;
            font-weight: 700;
            margin: 0.2rem 0 0.2rem;
        }
        .stats-label, .how-body {
            color: #4b5563;
            margin: 0;
            font-size: 0.95rem;
        }
        .how-title, .featured-title {
            color: #14532d;
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0 0 0.35rem;
        }
        .featured-card img {
            width: 100%;
            height: 160px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 0.6rem;
        }
        .section-divider {
            margin: 1rem 0 0.8rem;
            border-top: 1px solid #bbf7d0;
        }

        @media (max-width: 768px) {
            .home-hero { padding: 1.3rem 1rem 1.25rem; }
            .home-hero h1 { font-size: 1.8rem; }
            .home-hero p { font-size: 0.95rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
