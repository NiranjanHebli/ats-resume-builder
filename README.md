# ATSCraft - ATS Resume Builder & Analysis Suite

![Python](https://img.shields.io/badge/Python-v3.13-gray?style=for-the-badge&logo=python&logoColor=ffdd54&labelColor=3670A0)
![Streamlit](https://img.shields.io/badge/Streamlit-v1.57.0-gray?style=for-the-badge&logo=Streamlit&logoColor=white&labelColor=FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-v1.4.0-gray?style=for-the-badge&logo=chainlink&logoColor=white&labelColor=1C3C3C)
![Groq](https://img.shields.io/badge/Groq-v0.37.1-gray?style=for-the-badge&labelColor=f55a14)


ATSCraft is a comprehensive, ATS-optimized resume builder and job description analyzer designed to bridge the gap between job seekers and Applicant Tracking Systems (ATS).


---

## Problem Statement

Most modern companies use Applicant Tracking Systems (ATS) to filter out resumes before they ever reach a human recruiter. Up to 75% of resumes are rejected due to formatting issues, missing keywords, or misalignment with the job description. Job seekers struggle to identify these gaps and optimize their profiles for specific roles without manual, tedious tailoring.

---

## Key Features

### 1. Interactive Resume Editor
Build structured, professional, and ATS-compliant resumes with real-time feedback.
- **Live PDF Previews**: Instant visual updates of your resume content during editing.
- **ATS-Optimized Templates**: Select from multiple high-parsing clean layouts.
- **Customizable Sections**: Seamlessly manage contact profiles (hyperlinked), experience, education, skills, and optional projects.

### 2. ATS Score Analyzer
Audit and evaluate your existing resume against targeted job definitions.
- **Match Scoring**: Get a percentage score reflecting job description compatibility.
- **Parsing Check**: Instant feedback on formatting risks, warnings, and missing components.
- **Keyword Auditing**: Track critical keyword presence and density directly.

### 3. Job Insights Portal
Extract actionable intelligence directly from job descriptions to prepare before applying.
- **ATS-Friendly Keywords**: Curates lists of must-have skills, nice-to-have capabilities, and soft skills.
- **Quick Wins**: Immediate, actionable advice on styling, resume positioning, and structure.
- **Deep Role Insights**: Inferred seniority levels, experience requirements, culture signals, organizational red flags, and custom interview prep questions.

---

## Use Cases

1. **Job Application Optimization**: Tailor your existing resume for a specific role by identifying missing keywords and structural parsing risks.
2. **Pre-Application Research**: Extract deep insights and interview preparation strategies directly from job descriptions to prepare for applications and discussions.
3. **ATS-Compliant Resume Creation**: Build a resume from scratch using layouts guaranteed to be easily read by automated scanners.

---

## Configuration & Setup

### Prerequisites
- Python 3.10+
- A Groq API Key (Create one at [console.groq.com](https://console.groq.com/))

### 1. Environment Configuration
Create a `.env` file in the root directory by copying the example template:
```bash
cp .env.example .env
```
Open `.env` and enter your Groq API Key:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 2. Install Dependencies
Install all required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Streamlit development server:
```bash
streamlit run app.py
```

---

## Future Improvements

- **AI-Powered Resume Tailoring**: Automatic phrasing suggestions to integrate missing keywords directly into descriptions.
- **Multiple Template Export Options**: Render and download resumes as clean HTML or customizable DOCX in addition to PDF.
- **LinkedIn Profile Optimization**: Scanner for LinkedIn profile PDFs to provide matching insights.
- **Multi-Model Support**: Dropdown to select different LLMs (e.g., Llama 3, Claude, GPT) depending on configuration preference.
