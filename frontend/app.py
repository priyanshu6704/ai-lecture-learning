

import streamlit as st

from state import init_state
from styles import inject_global_styles
from components.navigation import render_nav
from components.footer import render_footer
from views import home, upload, study, test_selection, mcq, speaking, report

st.set_page_config(
    page_title="LectureIQ",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

init_state()
inject_global_styles()
render_nav()

PAGES = {
    "home": home.render,
    "upload": upload.render,
    "study": study.render,
    "test_selection": test_selection.render,
    "mcq": mcq.render,
    "speaking": speaking.render,
    "report": report.render,
}

current_page = st.session_state.get("page", "home")
PAGES.get(current_page, home.render)()

render_footer()
