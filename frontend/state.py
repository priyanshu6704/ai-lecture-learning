import streamlit as st


def init_state():
    defaults = {
        "page": "home",
        "lecture_file": None,
        "lecture_uploaded": False,
        "filename": None,
        "study_notes": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def navigate(page):
    st.session_state.page = page
    st.rerun()


def get_page():
    return st.session_state.page