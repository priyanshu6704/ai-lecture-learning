"""
styles.py

Design tokens + a single CSS injector used across the app.
"""

import streamlit as st

COLORS = {
    "bg_top": "#0B1120",
    "bg_bottom": "#121A2E",
    "surface": "rgba(255,255,255,0.045)",
    "surface_hover": "rgba(255,255,255,0.075)",
    "ink": "#E9EDF8",
    "ink_muted": "#93A0C2",
    "line": "rgba(255,255,255,0.10)",
    "primary_start": "#4C7CFF",
    "primary_end": "#8B5CF6",
    "primary_solid": "#5B7FFF",
    "accent": "#2DE6C4",
    "accent_soft": "rgba(45,230,196,0.14)",
    "success": "#34D399",
    "success_soft": "rgba(52,211,153,0.14)",
    "danger": "#F87171",
    "danger_soft": "rgba(248,113,113,0.14)",
}


def inject_global_styles() -> None:
    """Call once per page render (top of app.py) to load fonts + CSS."""
    c = COLORS
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,500&family=Inter:wght@400;500;600;700;800&display=swap');

        header[data-testid="stHeader"] {{
            display: none;
        }}
        div[data-testid="stToolbar"] {{
            display: none;
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background: radial-gradient(1200px 600px at 15% -10%, rgba(76,124,255,0.16), transparent 60%),
                        radial-gradient(1000px 500px at 100% 0%, rgba(139,92,246,0.12), transparent 55%),
                        linear-gradient(180deg, {c['bg_top']} 0%, {c['bg_bottom']} 100%);
        }}

        h1, h2, h3, .alp-display {{
            font-family: 'Newsreader', serif;
            color: {c['ink']} !important;
            font-weight: 500;
            letter-spacing: -0.01em;
        }}

        p, li, span, label, div {{
            color: {c['ink']};
        }}

        .block-container {{
            max-width: 900px;
            padding-top: 1.4rem;
            padding-bottom: 4rem;
        }}

        .alp-kicker {{
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            letter-spacing: 0.06em;
            color: {c['accent']} !important;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 18px rgba(45,230,196,0.35);
        }}
        .alp-hero-title {{
            font-family: 'Newsreader', serif;
            font-size: 2.7rem;
            line-height: 1.15;
            color: {c['ink']} !important;
            margin: 0 0 1rem 0;
        }}
        .alp-hero-title .grad {{
            background: linear-gradient(135deg, {c['primary_start']}, {c['primary_end']});
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
        }}
        .alp-hero-sub {{
            font-size: 1.05rem;
            color: {c['ink_muted']} !important;
            max-width: 62ch;
            line-height: 1.65;
            margin-bottom: 1.7rem;
        }}

        .alp-section-title {{
            font-family: 'Newsreader', serif;
            font-size: 1.35rem;
            color: {c['ink']} !important;
            margin: 2.2rem 0 0.7rem 0;
            padding-bottom: 0.55rem;
            border-bottom: 1px solid {c['line']};
        }}
        .alp-section-title:first-of-type {{
            margin-top: 0.5rem;
        }}

        .alp-card {{
            background: {c['surface']};
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid {c['line']};
            border-left: 3px solid {c['primary_solid']};
            border-radius: 10px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.8rem;
            line-height: 1.65;
            color: {c['ink']} !important;
            box-shadow: 0 4px 24px rgba(0,0,0,0.18);
        }}
        .alp-card, .alp-card * {{
            color: {c['ink']} !important;
        }}
        .alp-card.accent {{
            border-left-color: {c['accent']};
            box-shadow: 0 4px 28px rgba(45,230,196,0.10), 0 4px 24px rgba(0,0,0,0.18);
        }}
        .alp-card.quiet {{
            border-left-color: {c['line']};
        }}

        .alp-badge {{
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            background: rgba(91,127,255,0.16);
            color: #A9BEFF !important;
            border: 1px solid rgba(91,127,255,0.3);
        }}
        .alp-badge.success {{ background: {c['success_soft']}; color: {c['success']} !important; border-color: rgba(52,211,153,0.3); }}
        .alp-badge.danger  {{ background: {c['danger_soft']};  color: {c['danger']}  !important; border-color: rgba(248,113,113,0.3); }}
        .alp-badge.accent  {{ background: {c['accent_soft']};  color: {c['accent']}  !important; border-color: rgba(45,230,196,0.3); }}

        .alp-steps {{
            display: flex;
            gap: 0.4rem;
            margin: 0.4rem 0 1.7rem 0;
        }}
        .alp-step {{
            flex: 1;
            height: 4px;
            border-radius: 2px;
            background: {c['line']};
        }}
        .alp-step.done {{ background: {c['primary_solid']}; }}
        .alp-step.current {{
            background: {c['accent']};
            box-shadow: 0 0 10px rgba(45,230,196,0.6);
        }}

        .alp-nav-brand {{
            font-family: 'Newsreader', serif;
            font-size: 1.3rem;
            color: {c['ink']} !important;
            padding-top: 0.4rem;
        }}
        .alp-nav-brand .grad {{
            background: linear-gradient(135deg, {c['primary_start']}, {c['accent']});
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
            font-weight: 600;
        }}

        .alp-footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid {c['line']};
            color: {c['ink_muted']} !important;
            font-size: 0.82rem;
            display: flex;
            justify-content: space-between;
        }}

        div.stButton > button {{
            border-radius: 8px !important;
            font-weight: 600 !important;
            white-space: nowrap !important;
            transition: all 0.15s ease !important;
        }}

        div.stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {c['primary_start']}, {c['primary_end']}) !important;
            border: none !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 18px rgba(76,124,255,0.35) !important;
        }}
        div.stButton > button[kind="primary"]:hover {{
            filter: brightness(1.08);
            box-shadow: 0 6px 22px rgba(76,124,255,0.5) !important;
        }}
        div.stButton > button[kind="primary"] p {{
            color: #FFFFFF !important;
        }}

        div.stButton > button:not([kind="primary"]) {{
            background: {c['surface']} !important;
            border: 1px solid {c['line']} !important;
            color: {c['ink']} !important;
        }}
        div.stButton > button:not([kind="primary"]):hover {{
            background: {c['surface_hover']} !important;
            border-color: rgba(91,127,255,0.5) !important;
            color: #FFFFFF !important;
        }}
        div.stButton > button:not([kind="primary"]) p {{
            color: inherit !important;
        }}

        div.stButton > button:disabled {{
            background: {c['accent_soft']} !important;
            border: 1px solid rgba(45,230,196,0.45) !important;
            color: {c['accent']} !important;
            opacity: 1 !important;
        }}
        div.stButton > button:disabled p {{
            color: {c['accent']} !important;
        }}

        div[data-testid="stFileUploaderDropzone"] {{
            background: {c['surface']} !important;
            border: 1px dashed {c['line']} !important;
        }}
        .stTextInput input, .stNumberInput input {{
            background: {c['surface']} !important;
            color: {c['ink']} !important;
            border-color: {c['line']} !important;
        }}
        .stRadio label, .stRadio p {{
            color: {c['ink']} !important;
        }}
        .stAlert p {{
            color: {c['ink']} !important;
        }}

        .alp-empty {{
            text-align: center;
            padding: 2.4rem 1rem;
            color: {c['ink_muted']} !important;
            border: 1px dashed {c['line']};
            border-radius: 10px;
            background: {c['surface']};
        }}

        hr {{
            border-color: {c['line']} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )