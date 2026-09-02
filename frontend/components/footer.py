import streamlit as st


def render_footer():
    st.markdown(
        """
        <div class="footer">
            © 2026 AI Lecture Learning. Optimized for Academic Excellence.
        </div>
        """,
        unsafe_allow_html=True,
    )