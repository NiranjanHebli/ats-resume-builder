import base64
import os
import streamlit as st

def render_sidebar():
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

        active_page = st.query_params.get("page", "Editor")
        editor_active = "active" if active_page == "Editor" else ""
        templates_active = "active" if active_page == "Templates" else ""
        analysis_active = "active" if active_page == "Analysis" else ""
        job_insights_active = "active" if active_page == "JobInsights" else ""
        about_active = "active" if active_page == "About" else ""

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
.nav-item {{
    display: flex;
    align-items: center;
    padding: 12px 16px;
    margin-bottom: 8px;
    border-radius: 8px;
    color: #94a3b8;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    text-decoration: none;
    transition: background-color 0.2s, color 0.2s;
}}
.nav-item:hover {{
    background-color: rgba(255, 255, 255, 0.05);
    color: #f8fafc;
}}
.nav-item.active {{
    background-color: #1e293b;
    color: #f8fafc;
    cursor: default;
}}
.nav-icon {{
    margin-right: 14px;
    font-size: 1.1rem;
    opacity: 0.8;
}}
.nav-item.active .nav-icon {{
    opacity: 1;
    color: #60a5fa;
}}
</style>

<div class="sidebar-container">
    <div class="brand-container">
        {brand_html}
    </div>
    
    <a href="/?page=Editor" target="_self" class="nav-item {editor_active}">
        <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 18px; height: 18px;"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg></span> Editor
    </a>
    <a href="/?page=Templates" target="_self" class="nav-item {templates_active}">
        <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 18px; height: 18px;"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" /></svg></span> Templates
    </a>
    <a href="/?page=Analysis" target="_self" class="nav-item {analysis_active}">
        <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 18px; height: 18px;"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" /></svg></span> Analysis
    </a>
    <a href="/?page=JobInsights" target="_self" class="nav-item {job_insights_active}">
        <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 18px; height: 18px;"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 0 0 .75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 0 0-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0 1 12 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 0 1-.673-.38m0 0A2.18 2.18 0 0 1 3 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 0 1 3.413-.387m7.5 0V5.25A2.25 2.25 0 0 0 13.5 3h-3a2.25 2.25 0 0 0-2.25 2.25v.894m7.5 0a48.667 48.667 0 0 0-7.5 0M12 12.75h.008v.008H12v-.008Z" /></svg></span> Job Insights
    </a>
    <a href="/?page=About" target="_self" class="nav-item {about_active}">
        <span class="nav-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 18px; height: 18px;"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 1 1 .718 1.316l-.041.02a.75.75 0 0 1-.718-1.316zm.18 5.625l-.041-.02a.75.75 0 0 1-.718-1.316l.041.02a.75.75 0 1 1 .718 1.316zM21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" /></svg></span> About
    </a>
</div>
"""
        st.html(sidebar_html)
    return active_page, brand_html
