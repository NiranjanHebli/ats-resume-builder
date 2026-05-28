import os
import streamlit as st
import json
from langchain_groq import ChatGroq


def analyze_job_description(api_key: str, job_title: str, job_description: str) -> dict | None:
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.1,
    )
    llm_with_json = llm.bind(response_format={"type": "json_object"})

    prompt = f"""
You are an expert career coach and ATS specialist.
Analyse the following job description for the role: "{job_title}".

Return a JSON object with EXACTLY this structure (no extra keys):
{{
  "overview": {{
    "seniority_level": "Mid-level",
    "employment_type": "Full-time",
    "industry": "Software / Technology",
    "experience_required": "3-5 years"
  }},
  "ats_keywords": {{
    "must_have": ["keyword1", "keyword2"],
    "nice_to_have": ["keyword3", "keyword4"],
    "soft_skills": ["Communication", "Teamwork"]
  }},
  "quick_wins": [
    {{
      "title": "Tailor your summary",
      "description": "Mirror the exact role title in your resume summary.",
      "type": "success"
    }}
  ],
  "key_responsibilities": ["Responsibility 1", "Responsibility 2", "Responsibility 3"],
  "required_skills": ["Skill 1", "Skill 2", "Skill 3"],
  "preferred_qualifications": ["Qual 1", "Qual 2"],
  "culture_signals": ["Signal 1", "Signal 2"],
  "red_flags": ["Flag 1"],
  "salary_insight": "Estimated $90k–$130k based on role and market.",
  "interview_tips": ["Tip 1", "Tip 2", "Tip 3"]
}}

Rules:
- Extract data ONLY from the job description below.
- Provide 3–5 items per list unless specified.
- Provide exactly 3 quick_wins with types: "success", "warning", or "error".
- If data is unavailable, use an empty list [] or "Not specified".

Job Description:
{job_description}
"""

    try:
        messages = [
            ("system", "You are a JSON-only ATS and career insights engine. Output raw JSON, no markdown."),
            ("human", prompt),
        ]
        response = llm_with_json.invoke(messages)
        return json.loads(response.content)
    except Exception as e:
        st.error(f"Groq API error: {e}")
        return None


def _win_icon(win_type: str) -> str:
    if win_type == "error":
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#f87171" style="width:18px;height:18px;flex-shrink:0;"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>'
    elif win_type == "warning":
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#facc15" style="width:18px;height:18px;flex-shrink:0;"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>'
    else:
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#4ade80" style="width:18px;height:18px;flex-shrink:0;"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'


def render_job_insights():
    st.markdown("""
<style>
.ji-hero-title { font-size:2.4rem; font-weight:700; color:#f8fafc; margin-bottom:.4rem; }
.ji-hero-sub   { color:#94a3b8; font-size:1rem; margin-bottom:2rem; }
.ji-card {
    background: rgba(30,41,59,0.45);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
}
.ji-card-title {
    font-size:.78rem; font-weight:700; text-transform:uppercase;
    letter-spacing:.8px; color:#60a5fa; margin-bottom:1.1rem;
}
.ji-pill {
    display:inline-block; padding:4px 13px; border-radius:20px;
    font-size:.82rem; font-weight:500; margin:3px 4px 3px 0;
    border:1px solid rgba(255,255,255,0.12); color:#e2e8f0;
    background:rgba(255,255,255,0.05);
}
.ji-pill.must   { border-color:rgba(96,165,250,.4); color:#93c5fd; background:rgba(96,165,250,.08); }
.ji-pill.nice   { border-color:rgba(167,139,250,.4); color:#c4b5fd; background:rgba(167,139,250,.08); }
.ji-pill.soft   { border-color:rgba(74,222,128,.35); color:#86efac; background:rgba(74,222,128,.07); }
.ji-meta-item {
    display:flex; align-items:center; gap:10px;
    padding:.55rem 0; border-bottom:1px solid rgba(255,255,255,0.05);
    font-size:.88rem; color:#cbd5e1;
}
.ji-meta-item:last-child { border-bottom:none; }
.ji-meta-label { color:#64748b; font-size:.78rem; font-weight:600; min-width:130px; }
.ji-bullet { display:flex; align-items:flex-start; gap:10px; margin-bottom:.75rem; color:#cbd5e1; font-size:.88rem; line-height:1.5; }
.ji-bullet-dot { width:6px; height:6px; background:#60a5fa; border-radius:50%; margin-top:7px; flex-shrink:0; }
.ji-win-item { display:flex; align-items:flex-start; gap:12px; margin-bottom:1rem; }
.ji-win-item svg { margin-top: 3px; }
.ji-win-body h4 { margin:0 0 3px 0; font-size:.92rem; font-weight:600; color:#f8fafc; }
.ji-win-body p  { margin:0; font-size:.82rem; color:#94a3b8; }
.ji-tip-num { background:rgba(96,165,250,.15); color:#60a5fa; border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:.78rem; font-weight:700; flex-shrink:0; margin-top:1px; }
.ji-divider { border:none; border-top:1px solid rgba(255,255,255,0.07); margin:1.5rem 0; }
.ji-salary-box {
    background:linear-gradient(135deg, rgba(99,102,241,.18), rgba(14,165,233,.14));
    border:1px solid rgba(99,102,241,.3); border-radius:12px;
    padding:1.2rem 1.5rem; text-align:center;
}
.ji-salary-text { font-size:1.5rem; font-weight:700; color:#f8fafc; }
.ji-salary-sub  { font-size:.82rem; color:#94a3b8; margin-top:4px; }
.ji-flag-item { display:flex; align-items:flex-start; gap:10px; margin-bottom:.7rem; font-size:.88rem; color:#fca5a5; }
.ji-culture-badge {
    display:inline-block; padding:5px 14px; border-radius:8px; font-size:.82rem; font-weight:500;
    margin:4px; background:rgba(251,191,36,.08); border:1px solid rgba(251,191,36,.25); color:#fcd34d;
}
/* Flex row layout — ensures equal-height cards with no Streamlit column hacks */
.ji-row {
    display: flex;
    gap: 1.2rem;
    align-items: stretch;
    margin-bottom: 1.2rem;
}
.ji-col-1 { flex: 1; }
.ji-col-2 { flex: 2; }
.ji-row .ji-card {
    margin-bottom: 0;
    display: flex;
    flex-direction: column;
    height: auto !important;
}

</style>
""", unsafe_allow_html=True)

    st.markdown('<div class="ji-dashboard">', unsafe_allow_html=True)
    st.markdown('<h1 class="ji-hero-title">Job Insights Portal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="ji-hero-sub">Paste any job description and get instant ATS keywords, quick wins, and deep role intelligence.</p>', unsafe_allow_html=True)

    api_key = os.getenv("GROQ_API_KEY", "")

    # ── Input section ──────────────────────────────────────────────────────────
    with st.container():
        if not api_key:
            st.error("🔑 **Missing Groq API Key:** Please set `GROQ_API_KEY` in your `.env` file to enable job analysis.")
        
        job_title = st.text_input("Target Job Title", placeholder="e.g. Senior Backend Engineer", key="ji_job_title")

        job_description = st.text_area(
            "Job Description",
            placeholder="Paste the full job description here…",
            height=220,
            key="ji_job_description",
        )

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            analyse_clicked = st.button("Analyse Job", use_container_width=True, disabled=not api_key)

    st.markdown('<hr class="ji-divider">', unsafe_allow_html=True)

    # ── Run analysis ───────────────────────────────────────────────────────────
    if analyse_clicked:
        if not api_key:
            st.error("Please configure the GROQ_API_KEY in your .env file.")
            return
        if not job_title:
            st.warning("Please enter the target job title.")
            return
        if not job_description or len(job_description.strip()) < 50:
            st.warning("Please paste a meaningful job description (at least 50 characters).")
            return

        with st.spinner("Analysing job description with Groq LLM…"):
            data = analyze_job_description(api_key, job_title, job_description)

        if not data:
            return

        st.session_state["ji_result"] = data
        st.session_state["ji_job_title_result"] = job_title

    # ── Render results ─────────────────────────────────────────────────────────
    if "ji_result" not in st.session_state:
        st.markdown("""
<div class="ji-card" style="text-align:center; padding:3.5rem 2rem; min-height:280px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.2" stroke="#60a5fa" style="width:56px;height:56px;margin-bottom:1.2rem;">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z"/>
    </svg>
    <h2 style="color:#f8fafc; font-size:1.6rem; margin-bottom:.6rem;">No Analysis Yet</h2>
    <p style="color:#94a3b8; max-width:380px; line-height:1.6;">Fill in your Groq API key, job title, and job description above, then click <strong style="color:#60a5fa;">Analyse Job</strong>.</p>
</div>
</div>
""", unsafe_allow_html=True)
        return

    data = st.session_state["ji_result"]
    result_job_title = st.session_state.get("ji_job_title_result", "the role")

    # ── Row 1: Overview + Salary ───────────────────────────────────────────────
    overview = data.get("overview", {})
    salary = data.get("salary_insight", "")

    overview_html = '<div class="ji-card-title">Role Overview</div>'
    for label, val in [
        ("Job Title",           result_job_title),
        ("Seniority Level",     overview.get("seniority_level", "—")),
        ("Employment Type",     overview.get("employment_type", "—")),
        ("Industry",            overview.get("industry", "—")),
        ("Experience Required", overview.get("experience_required", "—")),
    ]:
        overview_html += f'<div class="ji-meta-item"><span class="ji-meta-label">{label}</span><span>{val}</span></div>'

    salary_html = (
        f'<div class="ji-card-title">Salary Insight</div>'
        f'<div style="flex:1;display:flex;align-items:center;justify-content:center;">'
        f'<div class="ji-salary-box" style="width:100%;">'
        f'<div class="ji-salary-sub" style="font-size:.95rem; color:#e2e8f0;">{salary if salary else "Not specified"}</div>'
        f'</div></div>'
    )

    row1 = (
        '<div class="ji-row">'
        f'<div class="ji-card ji-col-2">{overview_html}</div>'
        f'<div class="ji-card ji-col-1">{salary_html}</div>'
        '</div>'
    )
    st.markdown(row1, unsafe_allow_html=True)

    # ── Row 2: ATS Keywords (full width) ──────────────────────────────────────
    kw = data.get("ats_keywords", {})
    kw_html = '<div class="ji-card"><div class="ji-card-title">ATS-Friendly Keywords</div>'

    kw_html += '<div style="margin-bottom:1rem;">'
    kw_html += '<div style="font-size:.78rem;font-weight:600;color:#94a3b8;margin-bottom:.5rem;text-transform:uppercase;letter-spacing:.5px;">Must-Have</div>'
    must_have = kw.get("must_have", [])
    if must_have:
        for item in must_have:
            kw_html += f'<span class="ji-pill must">{item}</span>'
    else:
        kw_html += '<p style="color:#64748b; font-size:.88rem; margin:0; font-style:italic;">None identified</p>'
    kw_html += '</div>'

    kw_html += '<div style="margin-bottom:1rem;">'
    kw_html += '<div style="font-size:.78rem;font-weight:600;color:#94a3b8;margin-bottom:.5rem;text-transform:uppercase;letter-spacing:.5px;">Nice-to-Have</div>'
    nice_to_have = kw.get("nice_to_have", [])
    if nice_to_have:
        for item in nice_to_have:
            kw_html += f'<span class="ji-pill nice">{item}</span>'
    else:
        kw_html += '<p style="color:#64748b; font-size:.88rem; margin:0; font-style:italic;">None identified</p>'
    kw_html += '</div>'

    kw_html += '<div>'
    kw_html += '<div style="font-size:.78rem;font-weight:600;color:#94a3b8;margin-bottom:.5rem;text-transform:uppercase;letter-spacing:.5px;">Soft Skills</div>'
    soft_skills = kw.get("soft_skills", [])
    if soft_skills:
        for item in soft_skills:
            kw_html += f'<span class="ji-pill soft">{item}</span>'
    else:
        kw_html += '<p style="color:#64748b; font-size:.88rem; margin:0; font-style:italic;">None identified</p>'
    kw_html += '</div></div>'
    st.markdown(kw_html, unsafe_allow_html=True)

    # ── Row 3: Quick Wins + Key Responsibilities ───────────────────────────────
    wins = data.get("quick_wins", [])
    wins_html = '<div class="ji-card-title">Quick Wins</div>'
    if wins:
        for win in wins:
            icon = _win_icon(win.get("type", "success"))
            wins_html += f'<div class="ji-win-item">{icon}<div class="ji-win-body"><h4>{win["title"]}</h4><p>{win["description"]}</p></div></div>'
    else:
        wins_html += '<p style="color:#94a3b8; font-size:.88rem;">No quick wins detected.</p>'

    resps = data.get("key_responsibilities", [])
    resp_html = '<div class="ji-card-title">Key Responsibilities</div>'
    if resps:
        for item in resps:
            resp_html += f'<div class="ji-bullet"><div class="ji-bullet-dot"></div><span>{item}</span></div>'
    else:
        resp_html += '<p style="color:#94a3b8; font-size:.88rem;">No key responsibilities specified.</p>'

    row3 = (
        '<div class="ji-row">'
        f'<div class="ji-card ji-col-1">{wins_html}</div>'
        f'<div class="ji-card ji-col-1">{resp_html}</div>'
        '</div>'
    )
    st.markdown(row3, unsafe_allow_html=True)

    # ── Row 4: Required Skills + Preferred Qualifications ─────────────────────
    skills = data.get("required_skills", [])
    skills_html = '<div class="ji-card-title">Required Skills</div>'
    if skills:
        skills_html += '<div style="display:flex; flex-wrap:wrap; gap:8px;">'
        for item in skills:
            skills_html += f'<span class="ji-pill" style="margin:0;">{item}</span>'
        skills_html += '</div>'
    else:
        skills_html += '<p style="color:#94a3b8; font-size:.88rem;">No required skills specified.</p>'

    quals = data.get("preferred_qualifications", [])
    quals_html = '<div class="ji-card-title">Preferred Qualifications</div>'
    if quals:
        for item in quals:
            quals_html += f'<div class="ji-bullet"><div class="ji-bullet-dot" style="background:#a78bfa;"></div><span>{item}</span></div>'
    else:
        quals_html += '<p style="color:#94a3b8; font-size:.88rem;">No preferred qualifications specified.</p>'

    row4 = (
        '<div class="ji-row">'
        f'<div class="ji-card ji-col-1">{skills_html}</div>'
        f'<div class="ji-card ji-col-1">{quals_html}</div>'
        '</div>'
    )
    st.markdown(row4, unsafe_allow_html=True)

    # ── Row 5: Culture Signals + Red Flags ────────────────────────────────────
    culture = data.get("culture_signals", [])
    culture_html = '<div class="ji-card-title">Culture Signals</div>'
    if culture:
        culture_html += '<div style="display:flex; flex-wrap:wrap; gap:8px;">'
        for item in culture:
            culture_html += f'<span class="ji-culture-badge" style="margin:0;">{item}</span>'
        culture_html += '</div>'
    else:
        culture_html += '<p style="color:#94a3b8; font-size:.88rem;">No culture signals detected.</p>'

    flags = data.get("red_flags", [])
    flags_html = '<div class="ji-card-title">Red Flags to Watch</div>'
    if flags:
        for item in flags:
            flags_html += f'<div class="ji-flag-item"><span>{item}</span></div>'
    else:
        flags_html += '<p style="color:#4ade80; font-size:.88rem;">No significant red flags detected.</p>'

    row5 = (
        '<div class="ji-row">'
        f'<div class="ji-card ji-col-1">{culture_html}</div>'
        f'<div class="ji-card ji-col-1">{flags_html}</div>'
        '</div>'
    )
    st.markdown(row5, unsafe_allow_html=True)

    # ── Row 6: Interview Tips (full width) ────────────────────────────────────
    tips = data.get("interview_tips", [])
    if tips:
        tips_html = '<div class="ji-card"><div class="ji-card-title">Interview Preparation Tips</div><div style="display:flex;flex-direction:column;gap:.8rem;">'
        for i, tip in enumerate(tips, 1):
            tips_html += f'<div class="ji-win-item"><div class="ji-tip-num">{i}</div><div class="ji-win-body"><p style="margin:0;font-size:.88rem;color:#cbd5e1;">{tip}</p></div></div>'
        tips_html += '</div></div>'
        st.markdown(tips_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
