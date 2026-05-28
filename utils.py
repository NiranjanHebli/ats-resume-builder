import os
import re
import streamlit as st

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def get_pdf_pages_as_images(pdf_url_or_path):
    path = pdf_url_or_path
    if pdf_url_or_path.startswith("http"):
        path = "assets/harvard_guidelines.pdf"
        if not os.path.exists(path):
            import urllib.request
            os.makedirs("assets", exist_ok=True)
            urllib.request.urlretrieve(pdf_url_or_path, path)
            
    import fitz
    doc = fitz.open(path)
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=120)
        images.append(pix.tobytes("png"))
    doc.close()
    return images

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

TEMPLATE_NAMES = {
    "sample_resume_1.pdf": "Harvard College/HES (Classic/Academic)",
    "sample_resume_2.pdf": "Modern Professional (Clean Sidebar)",
    "sample_resume_3.pdf": "Minimalist Creative (Centered Header)",
    "sample_resume_4.pdf": "Executive Corporate (Elegant Left-Align)",
    "sample_resume_5.pdf": "Tech Minimalist (Modern Borders)",
    "sample_resume_6.pdf": "Project-Focused Professional",
    "sample_resume_7.pdf": "Classic Academic / Medical CV",
    "sample_resume_8.pdf": "Centered Classic Serif",
    "sample_resume_9.pdf": "Objective-Oriented Simple Layout",
    "sample_resume_10.pdf": "Contemporary Tech Resume",
}
