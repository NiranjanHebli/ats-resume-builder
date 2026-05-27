import json
import re
import streamlit as st
import os
from ui_components import (
    render_contact_info,
    render_summary,
    render_experience_section,
    render_education_section,
    render_skills_section,
    render_preview_pane,
)

st.set_page_config(page_title="Resume Builder", layout="wide")


def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")


TEMPLATE_DIR = "templates"
os.makedirs(TEMPLATE_DIR, exist_ok=True)


def extract_number(filename):
    match = re.search(r"\d+", filename)
    return int(match.group()) if match else 0


templates = sorted(
    [
        f
        for f in os.listdir(TEMPLATE_DIR)
        if f.endswith(".pdf") and 1 <= extract_number(f) <= 5
    ],
    key=extract_number,
)

if "exp_count" not in st.session_state:
    st.session_state.exp_count = 1
if "edu_count" not in st.session_state:
    st.session_state.edu_count = 1
if "preview_page_count" not in st.session_state:
    st.session_state.preview_page_count = 1


# Load template schema
with open("data/template_schema.json") as f:
    TEMPLATE_SCHEMA = json.load(f)

# Load sample data
with open("data/sample_data.json") as f:
    SAMPLE_DATA = json.load(f)


st.markdown(
    "<h1>Resume Builder</h1><p style='color:#64748b;'>Craft a polished, ATS-ready resume.</p>",
    unsafe_allow_html=True,
)
col1, col2 = st.columns([9, 10], gap="large")

with col1:
    st.markdown("### Template")
    selected_template = st.selectbox(
        "template_select",
        templates if templates else ["Default"],
        label_visibility="collapsed",
    )

    if (
        "prev_template" not in st.session_state
        or st.session_state.prev_template != selected_template
    ):
        st.session_state.prev_template = selected_template
        s_data = SAMPLE_DATA.get(
            selected_template, SAMPLE_DATA.get("default", {})
        )

        # Pre-fill contact
        contact = s_data.get("Contact", {})
        st.session_state.contact_name = contact.get("Name", "")
        st.session_state.contact_phone = contact.get("Phone", "")
        st.session_state.contact_email = contact.get("Email", "")
        st.session_state.contact_location = contact.get("Location", "")
        st.session_state.contact_links = contact.get("Links", "")

        # Pre-fill text areas
        st.session_state.summary_input = s_data.get("Summary", "")
        st.session_state.obj_input = s_data.get("Objective", "")
        st.session_state.skills_input = s_data.get("Skills", "")
        st.session_state.cert_input = s_data.get("Certifications", "")
        st.session_state.int_input = s_data.get("Interests", "")

        # Pre-fill experience
        exps = s_data.get("Experience", [])
        st.session_state.exp_count = max(1, len(exps))
        for i, exp in enumerate(exps):
            st.session_state[f"exp_org_{i}"] = exp.get("company", "")
            st.session_state[f"exp_loc_{i}"] = exp.get("location", "")
            st.session_state[f"exp_title_{i}"] = exp.get("title", "")
            st.session_state[f"exp_dates_{i}"] = exp.get("dates", "")
            st.session_state[f"exp_bull_{i}"] = exp.get("bullets", "")

        # Pre-fill education
        edus = s_data.get("Education", [])
        st.session_state.edu_count = max(1, len(edus))
        for i, edu in enumerate(edus):
            st.session_state[f"edu_school_{i}"] = edu.get("school", "")
            st.session_state[f"edu_loc_{i}"] = edu.get("location", "")
            st.session_state[f"edu_deg_{i}"] = edu.get("degree", "")
            st.session_state[f"edu_dates_{i}"] = edu.get("dates", "")
            st.session_state[f"edu_gpa_{i}"] = edu.get("gpa", "")
            st.session_state[f"edu_bull_{i}"] = edu.get("bullets", "")

        # Pre-fill projects
        projs = s_data.get("Projects", [])
        st.session_state.proj_count = max(1, len(projs))
        for i, proj in enumerate(projs):
            st.session_state[f"proj_title_{i}"] = proj.get("title", "")
            st.session_state[f"proj_dates_{i}"] = proj.get("dates", "")
            st.session_state[f"proj_desc_{i}"] = proj.get("bullets", "")

        # Get page count of the selected template to pre-fill height
        if selected_template and selected_template != "Default":
            tpath = os.path.join(TEMPLATE_DIR, selected_template)
            if os.path.exists(tpath):
                try:
                    import fitz

                    pdoc = fitz.open(tpath)
                    st.session_state.preview_page_count = len(pdoc)
                    pdoc.close()
                except BaseException:
                    st.session_state.preview_page_count = 1
            else:
                st.session_state.preview_page_count = 1
        else:
            st.session_state.preview_page_count = 1

        st.rerun()

    # Get schema for selected template
    schema = TEMPLATE_SCHEMA.get(selected_template, TEMPLATE_SCHEMA["default"])
    fields = schema.get(
        "fields", ["contact", "summary", "experience", "education", "skills"]
    )

    # Make the form scrollable and match the length of the rendered resume
    num_pages = st.session_state.get("preview_page_count", 1)
    form_height = 840 * num_pages + 60

    form_container = st.container(height=form_height)
    with form_container:
        name, phone, email, location, links = render_contact_info()
        st.markdown("<hr/>", unsafe_allow_html=True)

        summary = ""
        if "summary" in fields:
            summary = render_summary()
            st.markdown("<hr/>", unsafe_allow_html=True)

        objective = ""
        if "objective" in fields:
            # Import dynamically or assure it's imported at top
            from ui_components import render_objective

            objective = render_objective()
            st.markdown("<hr/>", unsafe_allow_html=True)

        experiences = []
        if "experience" in fields:
            experiences = render_experience_section()
            st.markdown("<hr/>", unsafe_allow_html=True)

        projects = []
        if "projects" in fields:
            from ui_components import render_projects

            projects = render_projects()
            st.markdown("<hr/>", unsafe_allow_html=True)

        educations = []
        if "education" in fields:
            educations = render_education_section()
            st.markdown("<hr/>", unsafe_allow_html=True)

        skills = ""
        if "skills" in fields:
            skills = render_skills_section()
            st.markdown("<hr/>", unsafe_allow_html=True)

        certifications = ""
        if "certifications" in fields:
            from ui_components import render_certifications

            certifications = render_certifications()
            st.markdown("<hr/>", unsafe_allow_html=True)

        interests = ""
        if "interests" in fields:
            from ui_components import render_interests

            interests = render_interests()
            st.markdown("<hr/>", unsafe_allow_html=True)

with col2:
    render_preview_pane(
        name=name,
        phone=phone,
        email=email,
        location=location,
        links=links,
        summary=summary,
        objective=objective,
        experiences=experiences,
        projects=projects,
        educations=educations,
        skills=skills,
        certifications=certifications,
        interests=interests,
        selected_template=selected_template,
        templates_dir=TEMPLATE_DIR,
    )
