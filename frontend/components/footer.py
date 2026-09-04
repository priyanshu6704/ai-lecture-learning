"""components/footer.py"""

import streamlit as st

from api_client import check_health


def render_footer() -> None:
    healthy = check_health()
    status_label = "Backend connected" if healthy else "Backend unreachable"
    badge_cls = "success" if healthy else "danger"

    st.markdown(
        f"""
        <div class="alp-footer">
            <span>LectureIQ &middot; AI study companion</span>
            <span class="alp-badge {badge_cls}">{status_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
