"""pages/test_selection.py"""

import streamlit as st

from components.navigation import render_progress
from state import go_to, reset_quiz_state, reset_speaking_state


def render() -> None:
    render_progress(active_index=3)

    st.markdown('<div class="alp-section-title">Choose a challenge</div>', unsafe_allow_html=True)
    st.write("Test your understanding of the lecture in either format -- or both.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="alp-card">
                <strong>MCQ Challenge</strong><br>
                <span style="color:#5B6478">Test your knowledge with timed multiple-choice questions.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start MCQ Challenge", type="primary", use_container_width=True):
            reset_quiz_state()
            go_to("mcq")

    with col2:
        st.markdown(
            """
            <div class="alp-card accent">
                <strong>Speaking Challenge</strong><br>
                <span style="color:#5B6478">Explain a concept out loud and get AI feedback.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start Speaking Challenge", type="primary", use_container_width=True):
            reset_speaking_state()
            go_to("speaking")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Study Notes"):
        go_to("study")
