import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        .stApp {
            background: #f8fafc;
            color: #172554;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 0.5rem;
            padding-bottom: 1rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        footer {
            visibility: hidden;
        }

        /* Navigation */

        .nav {
            height: 48px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 25px;
        }

        .logo {
            font-size: 15px;
            font-weight: 700;
            color: #123b91;
            flex: 1;
        }

        .nav-links {
            display: flex;
            gap: 24px;
            font-size: 11px;
            color: #64748b;
        }

        .profile {
            margin-left: auto;
            padding-left: 40px;
            font-size: 13px;
            color: #123b91;
        }

        /* Hero */

        .hero {
            text-align: center;
            padding: 35px 10px 25px;
        }

        .badge {
            display: inline-block;
            background: #eff6ff;
            color: #1d4ed8;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 700;
        }

        .hero h1 {
            font-size: 38px;
            line-height: 1.15;
            margin: 15px 0 10px;
            color: #123b91;
            font-weight: 800;
        }

        .gradient {
            color: #2563eb;
        }

        .hero p {
            max-width: 550px;
            margin: auto;
            font-size: 13px;
            line-height: 1.5;
            color: #64748b;
        }

        /* Cards */

        .card {
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 8px;
            padding: 20px;
            min-height: 150px;
            box-shadow: 0 2px 5px rgba(15, 23, 42, 0.05);
        }

        .card-icon {
            width: 34px;
            height: 34px;
            border-radius: 6px;
            background: #eff6ff;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #1d4ed8;
            margin-bottom: 15px;
            font-size: 16px;
        }

        .card h3 {
            margin: 0 0 8px;
            color: #172554;
            font-size: 17px;
        }

        .card p {
            margin: 0;
            color: #64748b;
            font-size: 11px;
            line-height: 1.5;
        }

        /* Section */

        .section-title {
            text-align: center;
            color: #123b91;
            font-size: 19px;
            font-weight: 700;
            margin: 35px 0 18px;
        }

        /* Streamlit buttons */

        .stButton > button {
            border-radius: 20px;
            height: 35px;
            font-size: 11px;
            font-weight: 600;
        }

        /* Footer */

        .footer {
            border-top: 1px solid #e2e8f0;
            margin-top: 40px;
            padding: 15px 0;
            text-align: center;
            color: #94a3b8;
            font-size: 9px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )