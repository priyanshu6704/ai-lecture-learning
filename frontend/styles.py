"""
styles.py

Design tokens + a single CSS injector used across the app.

Palette / type rationale (kept here as a comment so it survives refactors):
  - Subject: a calm, focused study tool -- not a marketing site, not a
    generic SaaS dashboard. Whitespace and quiet color do the work.
  - Background : #F6F7FB (cool paper, not the cliche warm cream)
  - Surface     : #FFFFFF
  - Ink         : #1C2333 (near-navy, softer than pure black)
  - Ink muted   : #5B6478
  - Line        : #E4E7EF
  - Primary     : #2F5D9F (study-blue -- used sparingly, mainly on the
                  primary action per screen)
  - Accent      : #E08A3C (warm amber -- reserved for progress / highlight,
                  never paired with primary on the same element)
  - Success     : #2F8F6B
  - Danger      : #C1554D
  - Display type: "Newsreader" (serif) for headings -- gives the product an
    academic, book-like character that fits "study notes".
  - Body/UI type: "Inter" for body copy, labels, buttons -- neutral and
    highly legible at small sizes inside Streamlit widgets.
"""

import streamlit as st

COLORS = {
    "bg": "#F6F7FB",
    "surface": "#FFFFFF",
    "ink": "#1C2333",
    "ink_muted": "#5B6478",
    "line": "#E4E7EF",
    "primary": "#2F5D9F",
    "primary_soft": "#E8EFFA",
    "accent": "#E08A3C",
    "accent_soft": "#FBEEE0",
    "success": "#2F8F6B",
    "success_soft": "#E7F4EE",
    "danger": "#C1554D",
    "danger_soft": "#FBECEA",
}


def inject_global_styles() -> None:
    """Call once per page render (top of app.py) to load fonts + CSS."""
    c = COLORS
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,500&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background-color: {c['bg']};
        }}

        h1, h2, h3, .alp-display {{
            font-family: 'Newsreader', serif;
            color: {c['ink']};
            font-weight: 500;
            letter-spacing: -0.01em;
        }}

        p, li, span, label, div {{
            color: {c['ink']};
        }}

        /* ---- layout shell ---- */
        .block-container {{
            max-width: 880px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }}

        /* ---- hero ---- */
        .alp-kicker {{
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: {c['primary']};
            font-weight: 600;
            margin-bottom: 0.4rem;
        }}
        .alp-hero-title {{
            font-family: 'Newsreader', serif;
            font-size: 2.6rem;
            line-height: 1.15;
            color: {c['ink']};
            margin: 0 0 0.9rem 0;
        }}
        .alp-hero-sub {{
            font-size: 1.05rem;
            color: {c['ink_muted']};
            max-width: 60ch;
            line-height: 1.6;
            margin-bottom: 1.6rem;
        }}

        /* ---- section headings with a rule, not a card ---- */
        .alp-section-title {{
            font-family: 'Newsreader', serif;
            font-size: 1.35rem;
            color: {c['ink']};
            margin: 2.2rem 0 0.6rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {c['line']};
        }}
        .alp-section-title:first-of-type {{
            margin-top: 0.5rem;
        }}

        /* ---- content card: left accent bar, no drop shadow ---- */
        .alp-card {{
            background: {c['surface']};
            border: 1px solid {c['line']};
            border-left: 3px solid {c['primary']};
            border-radius: 6px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.8rem;
            line-height: 1.6;
        }}
        .alp-card.accent {{
            border-left-color: {c['accent']};
        }}
        .alp-card.quiet {{
            border-left-color: {c['line']};
        }}

        /* ---- pill / status badges ---- */
        .alp-badge {{
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            background: {c['primary_soft']};
            color: {c['primary']};
        }}
        .alp-badge.success {{ background: {c['success_soft']}; color: {c['success']}; }}
        .alp-badge.danger  {{ background: {c['danger_soft']};  color: {c['danger']};  }}
        .alp-badge.accent  {{ background: {c['accent_soft']};  color: {c['accent']};  }}

        /* ---- step / progress rail used on multi-stage pages ---- */
        .alp-steps {{
            display: flex;
            gap: 0.4rem;
            margin: 0.4rem 0 1.6rem 0;
        }}
        .alp-step {{
            flex: 1;
            height: 4px;
            border-radius: 2px;
            background: {c['line']};
        }}
        .alp-step.done {{ background: {c['primary']}; }}
        .alp-step.current {{ background: {c['accent']}; }}

        /* ---- nav strip ---- */
        .alp-nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 0.8rem;
            margin-bottom: 1.2rem;
            border-bottom: 1px solid {c['line']};
        }}
        .alp-nav-brand {{
            font-family: 'Newsreader', serif;
            font-size: 1.15rem;
            color: {c['ink']};
        }}
        .alp-nav-brand span {{ color: {c['primary']}; }}

        /* ---- footer ---- */
        .alp-footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid {c['line']};
            color: {c['ink_muted']};
            font-size: 0.82rem;
            display: flex;
            justify-content: space-between;
        }}

        /* ---- primary buttons: give them the study-blue ---- */
        div.stButton > button[kind="primary"] {{
            background-color: {c['primary']};
            border: none;
        }}
        div.stButton > button[kind="primary"]:hover {{
            background-color: #274d84;
        }}
        div.stButton > button:not([kind="primary"]) {{
            border-color: {c['line']};
            color: {c['ink']};
        }}

        /* ---- empty state ---- */
        .alp-empty {{
            text-align: center;
            padding: 2.4rem 1rem;
            color: {c['ink_muted']};
            border: 1px dashed {c['line']};
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
