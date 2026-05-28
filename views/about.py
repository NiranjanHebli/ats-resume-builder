import streamlit as st
import base64
from utils import get_pdf_pages_as_images

ABOUT_HTML = """<style>
.about-container {
    font-family: 'Inter', sans-serif;
    color: #f1f5f9;
    text-align: center;
    padding: 10px 0;
}
.about-logo-container {
    margin: 0 auto 16px auto;
    display: flex;
    justify-content: center;
}
.about-logo-container .brand-logo {
    width: 90px !important;
    height: 90px !important;
    border-radius: 50% !important;
    border: 3px solid rgba(255, 255, 255, 0.15) !important;
    object-fit: cover !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
}
.about-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}
.about-version {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 24px;
}
.about-card {
    background-color: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 24px;
    text-align: left;
}
.about-card-title-row {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
}
.about-card-icon {
    font-size: 1.25rem;
    margin-right: 10px;
}
.about-card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #10b981;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.about-card-text {
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.5;
}
.about-section-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-align: left;
    margin-bottom: 12px;
}
.methodology-row {
    display: flex;
    background-color: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    align-items: flex-start;
    text-align: left;
}
.methodology-icon-box {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
    color: #60a5fa;
    width: 44px;
    height: 44px;
    min-width: 44px;
}
.methodology-icon-box img {
    width: 24px;
    height: 24px;
    filter: invert(100%);
    opacity: 0.9;
}
.methodology-content {
    flex: 1;
}
.methodology-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 4px;
}
.methodology-desc {
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.4;
}
.widgets-row {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 24px;
}
.widget-card {
    flex: 1;
    background-color: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.widget-svg-container {
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}
.widget-svg-container img {
    width: 36px;
    height: 36px;
    filter: invert(100%);
    opacity: 0.9;
}
.widget-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 4px;
}
.widget-desc {
    font-size: 0.75rem;
    color: #94a3b8;
}
</style>

<div class="about-container">
    <div class="about-logo-container">
        __LOGO_HTML__
    </div>
    <div class="about-title">ATSCraft</div>
    <div class="about-version">Version 1.0.0</div>

    <div class="about-card">
        <div class="about-card-title-row">
            <span class="about-card-icon">🚀</span>
            <span class="about-card-title">OUR MISSION</span>
        </div>
        <div class="about-card-text">
            Empowering professionals to navigate the modern job market with precision-engineered tools. Our mission is to dismantle the barriers of Applicant Tracking Systems (ATS) through advanced AI analysis, ensuring your expertise is never overlooked by an algorithm.
        </div>
    </div>

    <div class="widgets-row">
        <div class="widget-card">
            <div class="widget-svg-container">
                <img src="https://cdn.jsdelivr.net/npm/lucide-static@0.344.0/icons/gauge.svg" />
            </div>
            <div class="widget-title">ATS Match Rate</div>
            <div class="widget-desc">Optimized structure for top parser scores</div>
        </div>
        
        <div class="widget-card">
            <div class="widget-svg-container">
                <img src="https://cdn.jsdelivr.net/npm/lucide-static@0.344.0/icons/zap.svg" />
            </div>
            <div class="widget-title">Instant Rendering</div>
            <div class="widget-desc">Fast, real-time PDF generation</div>
        </div>

        <div class="widget-card">
            <div class="widget-svg-container">
                <img src="https://cdn.jsdelivr.net/npm/lucide-static@0.344.0/icons/brain-circuit.svg" />
            </div>
            <div class="widget-title">AI Semantic Match</div>
            <div class="widget-desc">Neural parser scoring simulation</div>
        </div>
    </div>

    <div class="about-section-title">SOURCES & METHODOLOGY</div>

    <div class="methodology-row">
        <div class="methodology-icon-box">
            <img src="https://cdn.jsdelivr.net/npm/lucide-static@0.344.0/icons/graduation-cap.svg" />
        </div>
        <div class="methodology-content">
            <div class="methodology-title">Harvard-Style Templates</div>
            <div class="methodology-desc">Our core structural engine utilizes the gold standard in professional formatting based on Harvard Office of Career Services guidelines.</div>
        </div>
    </div>

    <div class="methodology-row">
        <div class="methodology-icon-box">
            <img src="https://cdn.jsdelivr.net/npm/lucide-static@0.344.0/icons/cpu.svg" />
        </div>
        <div class="methodology-content">
            <div class="methodology-title">Neural Semantic Parser</div>
            <div class="methodology-desc">Leveraging Large Language Models to simulate the scoring logic of leading ATS platforms including Workday and Taleo.</div>
        </div>
    </div>

    <div class="about-section-title" style="margin-top: 24px;">OFFICIAL STYLE REFERENCE</div>
    
    <div class="pdf-link-container" style="text-align: left; margin-bottom: 12px; font-size: 0.85rem; color: #94a3b8;">
        Official Harvard Extension School Resume & Letter Guidelines: 
        <a href="https://cdn-careerservices.fas.harvard.edu/wp-content/uploads/sites/161/2024/08/2024-HES_resume-and-letter.pdf" target="_blank" style="color: #60a5fa; text-decoration: underline; font-weight: 500;">Open reference document in new tab</a>
    </div>
</div>
"""

def render_about(brand_html):
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        formatted_about_html = ABOUT_HTML.replace("__LOGO_HTML__", brand_html)
        st.html(formatted_about_html)
        
        try:
            # Render only the first page of our local Harvard-style template
            pdf_images = get_pdf_pages_as_images("templates/sample_resume_1.pdf")
            if pdf_images:
                first_page_b64 = base64.b64encode(pdf_images[0]).decode()
                st.html(f'''
                <a href="https://cdn-careerservices.fas.harvard.edu/wp-content/uploads/sites/161/2024/08/2024-HES_resume-and-letter.pdf" target="_blank" style="text-decoration: none;">
                    <div style="text-align: center; margin-bottom: 24px; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.015)'" onmouseout="this.style.transform='scale(1)'">
                        <img src="data:image/png;base64,{first_page_b64}" style="width: 100%; border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);" />
                        <p style="color: #60a5fa; font-size: 0.85rem; margin-top: 8px; font-weight: 500; text-decoration: underline;">Click to open complete guidelines document (PDF)</p>
                    </div>
                </a>
                ''')
        except Exception as e:
            st.error(f"Error loading guidelines PDF: {e}")
