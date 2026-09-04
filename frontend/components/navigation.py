"""components/navigation.py -- slim top nav + step rail."""

import streamlit as st

# Ordered list of (page_key, label) for the main learning flow.
FLOW = [
    ("home", "Home"),
    ("upload", "Upload"),
    ("study", "Study Notes"),
    ("test_selection", "Test"),
    ("report", "Report"),
]


def render_nav() -> None:
    current = st.session_state.get("page", "home")

    left, right = st.columns([3, 2])
    with left:
        st.markdown(
            '<div class="alp-nav-brand">Lecture<span>IQ</span></div>',
            unsafe_allow_html=True,
        )
    with right:
        cols = st.columns(len(FLOW))
        for col, (key, label) in zip(cols, FLOW):
            with col:
                disabled = key == current
                if st.button(label, key=f"nav_{key}", disabled=disabled, use_container_width=True):
                    st.session_state.page = key
                    st.rerun()

    st.markdown("<hr style='margin:0 0 1.2rem 0;border-color:#E4E7EF'>", unsafe_allow_html=True)


def render_progress(active_index: int, total: int = 5) -> None:
    """Thin step rail shown under the hero on flow pages.

    active_index is 0-based position within FLOW (Home..Report).
    """
    segments = []
    for i in range(total):
        if i < active_index:
            cls = "done"
        elif i == active_index:
            cls = "current"
        else:
            cls = ""
        segments.append(f'<div class="alp-step {cls}"></div>')
    st.markdown(f'<div class="alp-steps">{"".join(segments)}</div>', unsafe_allow_html=True)
