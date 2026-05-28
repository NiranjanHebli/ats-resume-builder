import streamlit as st
import os
import fitz
from generate_resume import generate_pdf


def render_contact_info():
    with st.expander("CONTACT INFORMATION", expanded=True):
        r1c1, r1c2 = st.columns(2)
        first_name = r1c1.text_input(
            "First Name", placeholder="Jane", key="contact_first_name"
        )
        last_name = r1c2.text_input(
            "Last Name", placeholder="Doe", key="contact_last_name"
        )
        email = r1c1.text_input(
            "Email", placeholder="jane@example.com", key="contact_email"
        )
        phone = r1c2.text_input(
            "Phone", placeholder="+1 555-555-5555", key="contact_phone"
        )
        r2c1, _ = st.columns(2)
        location = r2c1.text_input(
            "Location", placeholder="City, State", key="contact_location"
        )
        name = f"{first_name} {last_name}".strip()
        return name, phone, email, location


def render_profiles():
    with st.expander("PROFILES (e.g. LinkedIn, GitHub)", expanded=True):
        profiles = []
        if "prof_count" not in st.session_state:
            st.session_state.prof_count = 1

        for i in range(st.session_state.prof_count):
            st.markdown(f"**Profile {i + 1}**")
            c1, c2 = st.columns(2)
            name = c1.text_input("Profile Name (e.g. LinkedIn)", key=f"prof_name_{i}")
            link = c2.text_input("URL (e.g. https://linkedin.com/...)", key=f"prof_link_{i}")
            profiles.append({"name": name, "link": link})

        pb1, pb2 = st.columns(2)
        pb1.button(
            "Add Another Profile",
            on_click=lambda: st.session_state.update(
                prof_count=st.session_state.prof_count + 1
            ),
            key="btn_add_prof",
        )
        if st.session_state.prof_count > 1:
            pb2.button(
                "Remove Last Profile",
                on_click=lambda: st.session_state.update(
                    prof_count=st.session_state.prof_count - 1
                ),
                key="btn_rem_prof",
            )

    return profiles


def render_summary():
    with st.expander("PROFESSIONAL SUMMARY", expanded=True):
        summary = st.text_area(
            "Summary",
            height=80,
            label_visibility="collapsed",
            key="summary_input",
        )
        return summary


def render_experience_section():
    with st.expander("EXPERIENCE", expanded=True):
        experiences = []

        for i in range(st.session_state.exp_count):
            st.markdown(f"**Role {i + 1}**")
            c1, c2 = st.columns(2)
            company = c1.text_input("Organization Name", key=f"exp_org_{i}")
            loc = c2.text_input("City, State", key=f"exp_loc_{i}")
            c3, c4 = st.columns(2)
            title = c3.text_input("Job Title", key=f"exp_title_{i}")
            dates = c4.text_input(
                "Dates", placeholder="e.g. Month Year - Month Year", key=f"exp_dates_{i}"
            )
            bullets = st.text_area(
                "Bullet Points (one per line)", height=100, key=f"exp_bull_{i}"
            )
            experiences.append(
                {
                    "company": company,
                    "location": loc,
                    "title": title,
                    "dates": dates,
                    "bullets": bullets,
                }
            )

        eb1, eb2 = st.columns(2)
        eb1.button(
            "Add Another Role",
            on_click=lambda: st.session_state.update(
                exp_count=st.session_state.exp_count + 1
            ),
            key="btn_add_exp",
        )
        if st.session_state.exp_count > 1:
            eb2.button(
                "Remove Last Role",
                on_click=lambda: st.session_state.update(
                    exp_count=st.session_state.exp_count - 1
                ),
                key="btn_rem_exp",
            )

    return experiences


def render_education_section():
    with st.expander("EDUCATION", expanded=True):
        educations = []

        for i in range(st.session_state.edu_count):
            st.markdown(f"**Degree {i + 1}**")
            c1, c2 = st.columns(2)
            school = c1.text_input("School Name", key=f"edu_school_{i}")
            loc = c2.text_input("City, State", key=f"edu_loc_{i}")
            c3, c4 = st.columns(2)
            degree = c3.text_input("Degree", key=f"edu_deg_{i}")
            dates = c4.text_input("Graduation Date", key=f"edu_dates_{i}")
            gpa = st.text_input("GPA (Optional)", key=f"edu_gpa_{i}")
            bullets = st.text_area(
                "Bullet Points (one per line, Optional)",
                height=80,
                key=f"edu_bull_{i}",
            )

            educations.append(
                {
                    "school": school,
                    "location": loc,
                    "degree": degree,
                    "dates": dates,
                    "gpa": gpa,
                    "bullets": bullets,
                }
            )

        db1, db2 = st.columns(2)
        db1.button(
            "Add Another Degree",
            on_click=lambda: st.session_state.update(
                edu_count=st.session_state.edu_count + 1
            ),
            key="btn_add_edu",
        )
        if st.session_state.edu_count > 1:
            db2.button(
                "Remove Last Degree",
                on_click=lambda: st.session_state.update(
                    edu_count=st.session_state.edu_count - 1
                ),
                key="btn_rem_edu",
            )

    return educations


def render_skills_section():
    with st.expander("SKILLS", expanded=True):
        skills = st.text_area(
            "Technical/Language Skills",
            placeholder="e.g. Technical: Python, Java\nLanguage: English",
            height=80,
            key="skills_input",
            label_visibility="collapsed",
        )
        return skills


def render_objective():
    with st.expander("OBJECTIVE", expanded=True):
        objective = st.text_area(
            "Career Objective",
            height=80,
            label_visibility="collapsed",
            key="obj_input",
        )
        return objective


def render_projects():
    with st.expander("PROJECTS", expanded=True):
        projects = []
        if "proj_count" not in st.session_state:
            st.session_state.proj_count = 1

        for i in range(st.session_state.proj_count):
            st.markdown(f"**Project {i + 1}**")
            title = st.text_input("Project Title", key=f"proj_title_{i}")
            c1, c2 = st.columns(2)
            dates = c1.text_input("Dates", key=f"proj_dates_{i}")
            link = c2.text_input("Project Link (Optional)", key=f"proj_link_{i}")
            bullets = st.text_area(
                "Description (one point per line)", height=80, key=f"proj_desc_{i}"
            )
            projects.append({"title": title, "dates": dates, "bullets": bullets, "link": link})

        pb1, pb2 = st.columns(2)
        pb1.button(
            "Add Another Project",
            on_click=lambda: st.session_state.update(
                proj_count=st.session_state.proj_count + 1
            ),
            key="btn_add_proj",
        )
        if st.session_state.proj_count > 1:
            pb2.button(
                "Remove Last Project",
                on_click=lambda: st.session_state.update(
                    proj_count=st.session_state.proj_count - 1
                ),
                key="btn_rem_proj",
            )

    return projects


def render_certifications():
    with st.expander("CERTIFICATIONS", expanded=True):
        certs = st.text_area(
            "Certifications (one per line)",
            placeholder="e.g. AWS Certified Solutions Architect",
            height=80,
            key="cert_input",
            label_visibility="collapsed",
        )
        return certs


def render_interests():
    with st.expander("INTERESTS", expanded=True):
        interests = st.text_area(
            "Hobbies & Interests",
            placeholder="e.g. Photography, Open Source Contributing",
            height=80,
            key="int_input",
            label_visibility="collapsed",
        )
        return interests


def render_preview_pane(
    name,
    phone,
    email,
    location,
    profiles,
    summary,
    objective,
    experiences,
    projects,
    educations,
    skills,
    certifications,
    interests,
    selected_template,
    templates_dir,
):
    st.markdown("### Preview")
    tab1, tab2 = st.tabs(["Live Preview", "Template Sample"])

    with tab1:
        user_details = {
            "Contact": {
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Location": location,
                "Profiles": profiles,
            },
            "Summary": summary,
            "Objective": objective,
            "Experience": [
                e for e in experiences if e["company"] or e["title"]
            ],
            "Projects": [p for p in projects if p["title"]],
            "Education": [e for e in educations if e["school"] or e["degree"]],
            "Skills": skills,
            "Certifications": certifications,
            "Interests": interests,
        }

        output_pdf = "generated_resume.pdf"
        generate_pdf(output_pdf, user_details, selected_template)

        if os.path.exists(output_pdf):
            doc = fitz.open(output_pdf)
            st.session_state.preview_page_count = len(doc)
            for page in doc:
                pix = page.get_pixmap(dpi=180)
                st.image(pix.tobytes("png"), width="stretch")
            doc.close()

            with open(output_pdf, "rb") as f:
                st.download_button(
                    "Download Resume (PDF)",
                    f,
                    "My_Resume.pdf",
                    "application/pdf",
                )

    with tab2:
        if selected_template and selected_template != "Default":
            tpath = os.path.join(templates_dir, selected_template)
            if os.path.exists(tpath):
                pdoc = fitz.open(tpath)
                for page in pdoc:
                    pix = page.get_pixmap(dpi=180)
                    st.image(pix.tobytes("png"), width="stretch")
                pdoc.close()
            else:
                st.info("ℹ No static sample preview file is available for this template. Please use the **Live Preview** tab to view your generated resume.")
        else:
            st.info("ℹ The **Default** template does not have a static sample template. Please switch to the **Live Preview** tab to view your dynamically generated resume.")
