import streamlit as st
from utils import load_css
from views.sidebar import render_sidebar

# Initialize page config at the very beginning
st.set_page_config(page_title="ATSCraft", layout="wide")

# Initialize counts in session state early
if "exp_count" not in st.session_state:
    st.session_state.exp_count = 1
if "edu_count" not in st.session_state:
    st.session_state.edu_count = 1
if "preview_page_count" not in st.session_state:
    st.session_state.preview_page_count = 1

# Load external CSS
load_css("style.css")

# Render Sidebar and get the active page route
active_page, brand_html = render_sidebar()

# Route to the appropriate view
if active_page == "Editor":
    from views.editor import render_editor
    render_editor()
elif active_page == "About":
    from views.about import render_about
    render_about(brand_html)
elif active_page == "Analysis":
    from views.analysis import render_analysis
    render_analysis()
else:
    st.markdown(f"<h2>{active_page}</h2>", unsafe_allow_html=True)
    st.info("This section is under development.")
