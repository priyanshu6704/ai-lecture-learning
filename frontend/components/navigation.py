import streamlit as st
from state import navigate


def render_navigation():
    st.markdown(
        """
        <div class="nav">
            <div class="logo">AI Lecture Learning</div>
            <div class="nav-links">
                <span>Home</span>
                <span>Summary</span>
                <span>Test</span>
            </div>
            <div class="profile">◉</div>
        </div>
        """,
        unsafe_allow_html=True,
    )