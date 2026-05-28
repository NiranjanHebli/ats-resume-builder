import streamlit as st
import fitz  # PyMuPDF
import docx
import os
import json
from langchain_groq import ChatGroq

def extract_text_from_pdf(file_bytes):
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_docx(file_bytes):
    try:
        import io
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"

def analyze_resume_with_groq(api_key, resume_text, job_title, job_description=""):
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.1
    )
    llm_with_json = llm.bind(response_format={"type": "json_object"})
    
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) analyzer. 
    Analyze the following resume against the target job title: "{job_title}".
    CRITICAL: You MUST use the following job description to identify necessary keywords. ONLY extract keywords that are explicitly mentioned in this job description! Do not invent or guess keywords outside of this text.
    "{job_description}"
    
    Provide your analysis as a JSON object with the following structure:
    {{
        "score": 85, // An integer between 0 and 100 representing the overall match score
        "score_label": "Excellent", // A short label like "Excellent", "Good", "Fair", "Poor"
        "quick_wins": [
            {{
                "title": "Missing quantifiable metrics",
                "description": "Add numbers to your recent experience to boost impact.",
                "type": "error" // "error", "warning", or "success"
            }}
        ], // Provide exactly 3 quick wins based on gaps identified between the resume and the job description
        "found_keywords": ["React.js", "TypeScript", "CI/CD"], // List of important keywords found in the resume that are EXPLICITLY present in the job description
        "missing_keywords": ["Next.js", "Webpack", "Jest"], // List of important keywords missing from the resume but EXPLICITLY present in the job description
        "parsing_checks": [
            {{ "name": "Contact Info", "status": "Parsed", "ok": true }},
            {{ "name": "Standard Fonts", "status": "Verified", "ok": true }},
            {{ "name": "Tables/Columns", "status": "Unreadable", "ok": false }},
            {{ "name": "File Type", "status": "Supported", "ok": true }}
        ] // Provide 4 parsing checks
    }}
    
    Resume Text:
    {resume_text}
    """
    
    try:
        messages = [
            ("system", "You are an ATS analyzer that only outputs raw JSON. Do not include markdown formatting or explanation."),
            ("human", prompt)
        ]
        response = llm_with_json.invoke(messages)
        response_content = response.content
        return json.loads(response_content)
    except Exception as e:
        st.error(f"Error calling Groq API: {str(e)}")
        return None

def render_analysis():
    st.markdown('<div class="ats-dashboard">', unsafe_allow_html=True)
    st.markdown('<h1 class="ats-title">ATS Score Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="ats-subtitle">Upload your resume to see how it performs against industry Applicant Tracking Systems.</p>', unsafe_allow_html=True)
    
    col1, col_rest = st.columns([1.2, 2])
    
    with col1:
        st.markdown("### Analysis Settings")
        api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        job_title = st.text_input("Target Job Title", value="Senior Frontend Developer")
        job_description = st.text_area("Job Description", placeholder="Paste the job description here...", height=150)
        
        st.markdown("### Upload Resume")
        uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

    # Process file upload
    analysis_data = None
    if uploaded_file:
        if api_key:
            with st.spinner("Analyzing resume with Groq..."):
                file_bytes = uploaded_file.getvalue()
                if uploaded_file.name.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(file_bytes)
                else:
                    resume_text = extract_text_from_docx(file_bytes)
                
                if resume_text and not resume_text.startswith("Error"):
                    analysis_data = analyze_resume_with_groq(api_key, resume_text, job_title, job_description)
                else:
                    st.error("Failed to extract text from the file.")
        else:
            st.info("Showing Demo Analysis. To generate a real, dynamic analysis based on your PDF, please enter a valid Groq API Key in the sidebar.")
            analysis_data = {
                "score": 85,
                "score_label": "Excellent",
                "quick_wins": [
                    {
                        "title": "Missing quantifiable metrics",
                        "description": "Add numbers to your recent experience to boost impact.",
                        "type": "error"
                    },
                    {
                        "title": "Generic summary detected",
                        "description": "Tailor your summary to specific tech stack requirements.",
                        "type": "warning"
                    },
                    {
                        "title": "Strong active verbs",
                        "description": "Great job using action-oriented language throughout.",
                        "type": "success"
                    }
                ],
                "found_keywords": ["React.js", "TypeScript", "CI/CD", "Redux", "GraphQL"],
                "missing_keywords": ["Next.js", "Webpack", "Jest"],
                "parsing_checks": [
                    { "name": "Contact Info", "status": "Parsed", "ok": True },
                    { "name": "Standard Fonts", "status": "Verified", "ok": True },
                    { "name": "Tables/Columns", "status": "Unreadable", "ok": False },
                    { "name": "File Type", "status": "Supported", "ok": True }
                ]
            }

    with col_rest:
        if not analysis_data:
            # Show a beautiful placeholder card instructing the user to upload a file
            st.markdown("""
            <div class="dashboard-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; min-height: 400px; padding: 3rem;">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#60a5fa" style="width: 64px; height: 64px; margin-bottom: 1.5rem;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h2 style="color: #f8fafc; font-size: 1.8rem; font-weight: 700; margin-bottom: 0.75rem;">No Resume Analyzed Yet</h2>
                <p style="color: #94a3b8; font-size: 1rem; max-width: 400px; margin: 0 auto 1.5rem auto; line-height: 1.5;">
                    Please upload your resume (PDF or DOCX) in the upload box to perform a comprehensive ATS match score and keyword analysis.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # We have analysis data. We render the cards in the remaining space.
            # We can use nested columns inside col_rest!
            sub_col1, sub_col2 = st.columns(2)
            
            with sub_col1:
                score = analysis_data["score"]
                if score >= 80:
                    stroke_color = "#38bdf8"
                    label_color = "#4ade80"
                elif score >= 60:
                    stroke_color = "#facc15"
                    label_color = "#facc15"
                else:
                    stroke_color = "#f87171"
                    label_color = "#f87171"
                    
                circumference = 2 * 3.14159 * 90
                dashoffset = circumference - (score / 100) * circumference
                    
                score_html = '<div class="dashboard-card" style="display: flex; flex-direction: column; justify-content: center; height: 100%;">'
                score_html += '<div class="card-header" style="text-align: center;">Overall Match Score</div>'
                score_html += f"""
<div class="score-container">
    <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="90" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="12"></circle>
        <circle cx="100" cy="100" r="90" fill="none" stroke="{stroke_color}" stroke-width="12" 
                stroke-dasharray="{circumference}" stroke-dashoffset="{dashoffset}" 
                stroke-linecap="round" style="transform: rotate(-90deg); transform-origin: 50% 50%; transition: stroke-dashoffset 1s ease-in-out;"></circle>
    </svg>
    <div class="score-value">{score}</div>
    <div class="score-label" style="color: {label_color};">{analysis_data["score_label"]}</div>
</div>
"""
                score_html += '</div>'
                st.markdown(score_html, unsafe_allow_html=True)
                
            with sub_col2:
                qw_html = '<div class="dashboard-card" style="height: 100%;">'
                qw_html += '<div class="card-header"><span style="color: #60a5fa; margin-right: 5px;">⚡</span> Quick Wins</div>'
                
                for win in analysis_data["quick_wins"]:
                    if win["type"] == "error":
                        icon_html = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#f87171" style="width: 20px; height: 20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>'
                    elif win["type"] == "warning":
                        icon_html = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#94a3b8" style="width: 20px; height: 20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>'
                    else:
                        icon_html = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#4ade80" style="width: 20px; height: 20px;"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
                        
                    qw_html += f"""
<div class="quick-win-item">
    <div class="quick-win-icon">{icon_html}</div>
    <div class="quick-win-content">
        <h4>{win['title']}</h4>
        <p>{win['description']}</p>
    </div>
</div>
"""
                qw_html += '</div>'
                st.markdown(qw_html, unsafe_allow_html=True)
            
            # Bottom keyword analysis
            kw_html = '<div class="dashboard-card" style="margin-top: 1rem;">'
            kw_html += f'''
            <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div class="card-header" style="margin-bottom: 0;">Keyword Analysis</div>
                <div style="font-size: 0.85rem; color: #94a3b8;">Compared against: {job_title}</div>
            </div>
            '''
            
            kw_html += '<div style="font-size: 0.85rem; color: #f8fafc; margin-bottom: 8px;">Found Keywords</div><div>'
            for kw in analysis_data["found_keywords"]:
                kw_html += f'<span class="keyword-pill">{kw}</span>'
            kw_html += '</div>'
            
            kw_html += '<div style="font-size: 0.85rem; color: #f8fafc; margin-bottom: 8px; margin-top: 15px;">Missing Important Keywords</div><div>'
            for kw in analysis_data["missing_keywords"]:
                kw_html += f'<span class="keyword-pill missing">{kw}</span>'
            kw_html += '</div></div>'
            
            st.markdown(kw_html, unsafe_allow_html=True)
            
            # Bottom parsing check
            parsing_html = '<div class="dashboard-card">'
            parsing_html += '<div class="card-header">ATS Parsing Check</div>'
            parsing_html += '<div class="parsing-check-container">'
            
            for check in analysis_data["parsing_checks"]:
                if check["ok"]:
                    icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 28px; height: 28px; color: #4ade80;"><path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" /></svg>'
                    box_class = "parsing-box"
                    status_class = "parsing-status"
                else:
                    icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 28px; height: 28px; color: #f87171;"><path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-1.72 6.97a.75.75 0 10-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 101.06 1.06L12 13.06l1.72 1.72a.75.75 0 101.06-1.06L13.06 12l1.72-1.72a.75.75 0 10-1.06-1.06L12 10.94l-1.72-1.72z" clip-rule="evenodd" /></svg>'
                    box_class = "parsing-box error"
                    status_class = "parsing-status error-text"
                    
                parsing_html += f'<div class="{box_class}"><div class="parsing-icon">{icon}</div><div class="parsing-label">{check["name"]}</div><div class="{status_class}">{check["status"]}</div></div>'
            parsing_html += '</div></div>'
            
            st.markdown(parsing_html, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)
