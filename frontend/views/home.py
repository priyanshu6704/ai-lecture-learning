"""pages/home.py"""

import streamlit as st

from state import go_to


def render() -> None:
    st.markdown('<div class="alp-kicker">AI-POWERED LEARNING</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="alp-hero-title">Learn smarter from<br>your lectures.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="alp-hero-sub">Upload a lecture and let AI turn it into structured '
        "study notes, an MCQ challenge, a speaking challenge, and a final report on "
        "where you stand.</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Upload Lecture", type="primary", use_container_width=True):
            go_to("upload")

    st.markdown('<div class="alp-section-title">How it works</div>', unsafe_allow_html=True)

    steps = [
        ("Upload", "Add a PDF, DOCX, or PPTX lecture file."),
        ("Study Notes", "AI extracts a summary, key concepts, definitions, and examples."),
        ("MCQ Challenge", "Answer AI-generated questions against a timer."),
        ("Speaking Challenge", "Explain a concept out loud; AI transcribes and evaluates it."),
        ("Report", "See your combined score with strengths and areas to improve."),
    ]
    for title, desc in steps:
        st.markdown(
            f"""
            <div class="alp-card quiet">
                <strong>{title}</strong><br>
                <span style="color:#5B6478">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
