import streamlit as st

from styles import load_css
from state import init_state
from components.navigation import render_navigation
from components.footer import render_footer

from pages.home import render_home
from pages.upload import render_upload
from pages.study import render_study


st.set_page_config(
    page_title="AI Lecture Learning",
    page_icon="✦",
    layout="wide",
)


init_state()

load_css()

render_navigation()


if st.session_state.page == "home":

    render_home()

elif st.session_state.page == "upload":

    render_upload()

elif st.session_state.page == "study":

    render_study()

render_footer()