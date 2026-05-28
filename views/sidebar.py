import base64
import os
import streamlit as st

def render_sidebar():
    # Initialize active page in session state from query params on first run
    if "active_page" not in st.session_state:
        st.session_state.active_page = st.query_params.get("page", "Editor")

    with st.sidebar:
        logo_b64 = ""
        logo_file = "assets/logo.png"
        if os.path.exists(logo_file):
            with open(logo_file, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()

        if logo_b64:
            brand_html = f'<img src="data:image/png;base64,{logo_b64}" class="brand-logo" />'
        else:
            brand_html = """
            <div class="brand-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 20px; height: 20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" /></svg></div>
            <div class="brand-text-container">
                <span class="brand-title">ATSCraft</span>
            </div>
            """

        active_page = st.session_state.active_page

        sidebar_html = f"""<style>
.sidebar-container {{
    padding: 0px 0px;
    font-family: 'Inter', sans-serif;
}}
.brand-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    padding: 0 5px;
}}
.brand-logo {{
    width: 80px;
    height: 80px;
    display: block;
    margin: 0 auto;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.15);
}}
.brand-icon {{
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    border-radius: 8px;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 12px;
    color: white;
    font-size: 18px;
}}
.brand-text-container {{
    display: flex;
    flex-direction: column;
}}
.brand-title {{
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.2;
}}
.brand-subtitle {{
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 500;
    margin-top: 2px;
}}

/* Custom styled Streamlit buttons to avoid full browser reload */
[data-testid="stSidebar"] .stButton > button {{
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-align: left !important;
    width: 100% !important;
    transition: background-color 0.2s, color 0.2s !important;
    border: none !important;
    height: auto !important;
    box-shadow: none !important;
    outline: none !important;
}}

/* Secondary (Inactive) style override */
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"] {{
    background-color: transparent !important;
    color: #94a3b8 !important;
    border: none !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:hover {{
    background-color: rgba(255, 255, 255, 0.05) !important;
    color: #f8fafc !important;
    border: none !important;
    box-shadow: none !important;
}}

/* Primary (Active) style override */
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {{
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: none !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover {{
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: none !important;
    box-shadow: none !important;
}}
</style>

<div class="sidebar-container">
    <div class="brand-container">
        {brand_html}
    </div>
</div>
"""
        st.markdown(sidebar_html, unsafe_allow_html=True)

        if st.button("Editor", type="primary" if active_page == "Editor" else "secondary", use_container_width=True):
            st.session_state.active_page = "Editor"
            st.query_params["page"] = "Editor"
            st.rerun()

        if st.button("Analysis", type="primary" if active_page == "Analysis" else "secondary", use_container_width=True):
            st.session_state.active_page = "Analysis"
            st.query_params["page"] = "Analysis"
            st.rerun()

        if st.button("Job Insights", type="primary" if active_page == "JobInsights" else "secondary", use_container_width=True):
            st.session_state.active_page = "JobInsights"
            st.query_params["page"] = "JobInsights"
            st.rerun()

        if st.button("About", type="primary" if active_page == "About" else "secondary", use_container_width=True):
            st.session_state.active_page = "About"
            st.query_params["page"] = "About"
            st.rerun()

    return st.session_state.active_page, brand_html
