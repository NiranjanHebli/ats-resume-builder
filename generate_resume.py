import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SUPP = "/System/Library/Fonts/Supplemental"
_FONT_FILES = {
    "TimesNewRoman": f"{SUPP}/Times New Roman.ttf",
    "TimesNewRoman-Bold": f"{SUPP}/Times New Roman Bold.ttf",
    "TimesNewRoman-Italic": f"{SUPP}/Times New Roman Italic.ttf",
    "TimesNewRoman-BoldItalic": f"{SUPP}/Times New Roman Bold Italic.ttf",
    "Arial": f"{SUPP}/Arial.ttf",
    "Arial-Bold": f"{SUPP}/Arial Bold.ttf",
    "Arial-Italic": f"{SUPP}/Arial Italic.ttf",
    "Arial-BoldItalic": f"{SUPP}/Arial Bold Italic.ttf",
    "TrebuchetMS": f"{SUPP}/Trebuchet MS.ttf",
    "TrebuchetMS-Bold": f"{SUPP}/Trebuchet MS Bold.ttf",
    "TrebuchetMS-Italic": f"{SUPP}/Trebuchet MS Italic.ttf",
    "Georgia": f"{SUPP}/Georgia.ttf",
    "Georgia-Bold": f"{SUPP}/Georgia Bold.ttf",
    "Georgia-Italic": f"{SUPP}/Georgia Italic.ttf",
    "Georgia-BoldItalic": f"{SUPP}/Georgia Bold Italic.ttf",
}

_REGISTERED_FONTS = set()
for name, path in _FONT_FILES.items():
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont(name, path))
            _REGISTERED_FONTS.add(name)
        except Exception:
            pass

_FONT_MAP = {
    "timesnewroman": "Times-Roman",
    "timesnewroman-bold": "Times-Bold",
    "timesnewroman-italic": "Times-Italic",
    "timesnewroman-bolditalic": "Times-BoldItalic",
    "arial": "Helvetica",
    "arial-bold": "Helvetica-Bold",
    "arial-italic": "Helvetica-Oblique",
    "arial-bolditalic": "Helvetica-BoldOblique",
    "georgia": "Times-Roman",
    "georgia-bold": "Times-Bold",
    "georgia-italic": "Times-Italic",
    "georgia-bolditalic": "Times-BoldItalic",
    "trebuchetms": "Helvetica",
    "trebuchetms-bold": "Helvetica-Bold",
    "trebuchetms-italic": "Helvetica-Oblique",
    "trebuchetms-bolditalic": "Helvetica-BoldOblique",
}

def _resolve_font(font_name: str) -> str:
    if font_name in _REGISTERED_FONTS:
        return font_name
    return _FONT_MAP.get(font_name.lower(), "Helvetica")

_JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "template_fonts.json")
with open(_JSON_PATH) as f:
    TEMPLATE_FONT_SPEC = json.load(f)

_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "data", "template_schema.json")
if os.path.exists(_SCHEMA_PATH):
    with open(_SCHEMA_PATH) as f:
        TEMPLATE_SCHEMA = json.load(f)
else:
    TEMPLATE_SCHEMA = {}

_FALLBACK_SPEC = {
    "name": {"font": "TimesNewRoman-Bold", "size": 14.0, "align": "center"},
    "contact": {"font": "TimesNewRoman", "size": 11.0, "align": "center"},
    "section_heading": {
        "font": "TimesNewRoman-Bold",
        "size": 11.0,
        "align": "left",
    },
    "sub_heading": {
        "font": "TimesNewRoman-Bold",
        "size": 11.0,
        "align": "left",
    },
    "body": {"font": "TimesNewRoman", "size": 11.0, "align": "left"},
    "bullet": {"font": "TimesNewRoman", "size": 11.0, "align": "left"},
}

_ALIGN_MAP = {"center": TA_CENTER, "left": TA_LEFT, "right": TA_RIGHT}


def _style(role: str, spec: dict, **overrides) -> ParagraphStyle:
    info = spec.get(role, _FALLBACK_SPEC[role])
    align = _ALIGN_MAP.get(info.get("align", "left"), TA_LEFT)
    size = info["size"]
    font = info["font"]

    if overrides.pop("_italic", False) and not font.endswith("-Italic"):
        if font.endswith("-Bold"):
            font = font.replace("-Bold", "-BoldItalic")
        else:
            font = font + "-Italic"
        if font not in _FONT_FILES:
            font = info["font"]

    font = _resolve_font(font)

    kwargs = dict(
        fontName=font,
        fontSize=size,
        leading=size * 1.35,
        textColor=black,
        alignment=align,
    )
    kwargs.update(overrides)
    return ParagraphStyle(
        f"_style_{role}_{font}_{hash(str(overrides))}", **kwargs
    )


def sanitize(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.encode("ascii", "ignore").decode("ascii")

def format_profiles(profiles):
    parts = []
    for p in profiles:
        name = sanitize(p.get("name", "").strip())
        url = p.get("link", "").strip()
        if name and url:
            parts.append(f'<link href="{sanitize(url)}"><font color="blue">{name}</font></link>')
        elif name:
            parts.append(name)
        elif url:
            parts.append(f'<link href="{sanitize(url)}"><font color="blue">{sanitize(url)}</font></link>')
    return parts

def format_project_title(title, link):
    safe_title = sanitize(title.strip())
    safe_link = link.strip()
    if safe_title and safe_link:
        return f'<link href="{sanitize(safe_link)}"><font color="blue">{safe_title}</font></link>'
    return safe_title


def create_row_table(left_para, right_para, doc_width):
    t = Table(
        [[left_para, right_para]], colWidths=[doc_width * 0.7, doc_width * 0.3]
    )
    t.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return t


def generate_pdf(
    output_path: str,
    user_details: dict,
    template_choice: str = "sample_resume_1.pdf",
):
    # Check if user details are empty to provide a beautiful template preview
    has_content = False
    contact = user_details.get("Contact", {})
    if (
        contact.get("Name")
        or contact.get("Email")
        or contact.get("Phone")
        or contact.get("Location")
        or contact.get("Profiles")
    ):
        has_content = True
    if user_details.get("Summary"):
        has_content = True
    if any(
        e.get("company") or e.get("title")
        for e in user_details.get("Experience", [])
    ):
        has_content = True
    if any(
        e.get("school") or e.get("degree")
        for e in user_details.get("Education", [])
    ):
        has_content = True
    if user_details.get("Skills"):
        has_content = True

    if not has_content:
        user_details = {
            "Contact": {
                "Name": "Jane Doe",
                "Email": "jane.doe@example.com",
                "Phone": "+1 (555) 555-5555",
                "Location": "San Francisco, CA",
                "Profiles": [{"name": "LinkedIn", "link": "https://linkedin.com/in/janedoe"}],
            },
            "Summary": "Highly motivated Software Engineer with 5+ years of experience building scalable web applications. Proficient in Python, database optimization, and cloud architecture, with a passion for writing clean, maintainable code.",
            "Experience": [
                {
                    "company": "Tech Innovations Inc.",
                    "location": "San Francisco, CA",
                    "title": "Senior Software Engineer",
                    "dates": "Jan 2022 - Present",
                    "bullets": "Led the backend team in migrating legacy monolith architectures to Python-based microservices, reducing latencies by 35%.\nDesigned and developed robust RESTful APIs using FastAPI and integrated them with AWS infrastructure.",
                },
                {
                    "company": "Dynamic Solutions Group",
                    "location": "Boston, MA",
                    "title": "Software Developer",
                    "dates": "Jun 2019 - Dec 2021",
                    "bullets": "Collaborated with design and product teams to implement interactive user dashboards.\nOptimized database indexing and queries, cutting query execution times by 20%.",
                },
            ],
            "Education": [
                {
                    "school": "University of California, Berkeley",
                    "location": "Berkeley, CA",
                    "degree": "B.S. in Computer Science",
                    "dates": "Sep 2015 - May 2019",
                }
            ],
            "Skills": "Languages: Python, SQL, JavaScript, HTML/CSS\nFrameworks & Tools: FastAPI, Streamlit, Docker, PostgreSQL, Git",
        }

    spec = TEMPLATE_FONT_SPEC.get(template_choice, _FALLBACK_SPEC)

    margin = 54
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=margin,
        leftMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
    )
    doc_width = letter[0] - (2 * margin)

    _style("name", spec, spaceAfter=4)
    _style("contact", spec, spaceAfter=14)
    _style("section_heading", spec, spaceBefore=14, spaceAfter=2)
    _style("sub_heading", spec, spaceAfter=0)
    _style("body", spec, spaceAfter=0, alignment=TA_RIGHT)
    _style("sub_heading", spec, spaceAfter=2, _italic=True)
    _style("body", spec, spaceAfter=2, alignment=TA_RIGHT)
    _style("body", spec, spaceAfter=2)
    _style("bullet", spec, spaceAfter=2, leftIndent=14)

    story = []

    # --- ROUTER ---
    if template_choice == "sample_resume_1.pdf":
        render_template_1(doc, story, user_details, spec, doc_width)
    elif template_choice == "sample_resume_2.pdf":
        render_template_2(doc, story, user_details, spec, doc_width)
    elif template_choice == "sample_resume_3.pdf":
        render_template_3(doc, story, user_details, spec, doc_width)
    elif template_choice == "sample_resume_4.pdf":
        render_template_4(doc, story, user_details, spec, doc_width)
    elif template_choice == "sample_resume_5.pdf":
        render_template_5(doc, story, user_details, spec, doc_width)
    else:
        render_template_generic(
            doc, story, user_details, spec, template_choice, doc_width
        )


def render_template_1(doc, story, user_details, spec, doc_width):
    name_st = _style("name", spec, spaceAfter=4)
    contact_st = _style("contact", spec, spaceAfter=14)
    heading_st = _style(
        "section_heading",
        spec,
        spaceBefore=14,
        spaceAfter=2,
        alignment=TA_CENTER,
    )
    org_st = _style("sub_heading", spec, spaceAfter=0)
    org_right_st = _style("body", spec, spaceAfter=0, alignment=TA_RIGHT)
    # Note: not italic/bold for temp 1 education degree, but we use bold for
    # job title
    title_st = _style("body", spec, spaceAfter=2)
    job_title_st = _style("sub_heading", spec, spaceAfter=2)
    title_right_st = _style("body", spec, spaceAfter=2, alignment=TA_RIGHT)
    bullet_st = _style("bullet", spec, spaceAfter=2, leftIndent=14)

    contact = user_details.get("Contact", {})
    name = contact.get("Name", "Your Name")
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    location = contact.get("Location", "")
    profiles = contact.get("Profiles", [])
    story.append(Paragraph(sanitize(name), name_st))
    
    c_parts = [sanitize(p.strip()) for p in [location, phone, email] if p.strip()]
    c_parts.extend(format_profiles(profiles))
    if c_parts:
        story.append(Paragraph(" | ".join(c_parts), contact_st))

    education = user_details.get("Education", [])
    if education:
        story.append(Paragraph("Education", heading_st))
        for edu in education:
            org_p = Paragraph(sanitize(edu.get("school", "")), org_st)
            loc_p = Paragraph(sanitize(edu.get("location", "")), org_right_st)
            story.append(create_row_table(org_p, loc_p, doc_width))

            deg_p = Paragraph(sanitize(edu.get("degree", "")), title_st)
            date_p = Paragraph(sanitize(edu.get("dates", "")), title_right_st)
            story.append(create_row_table(deg_p, date_p, doc_width))
            story.append(Spacer(1, 4))

    experience = user_details.get("Experience", [])
    if experience:
        story.append(Paragraph("Experience", heading_st))
        for exp in experience:
            org_p = Paragraph(sanitize(exp.get("company", "")), org_st)
            loc_p = Paragraph(sanitize(exp.get("location", "")), org_right_st)
            story.append(create_row_table(org_p, loc_p, doc_width))

            tit_p = Paragraph(sanitize(exp.get("title", "")), job_title_st)
            dat_p = Paragraph(sanitize(exp.get("dates", "")), title_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = exp.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    projects = user_details.get("Projects", [])
    if projects:
        story.append(Paragraph("Projects", heading_st))
        for proj in projects:
            title_text = format_project_title(proj.get("title", ""), proj.get("link", ""))
            tit_p = Paragraph(title_text, job_title_st)
            dat_p = Paragraph(sanitize(proj.get("dates", "")), title_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = proj.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    skills = user_details.get("Skills", "").strip()
    if skills:
        story.append(Paragraph("Skills", heading_st))
        for line in skills.split("\n"):
            if line.strip():
                story.append(Paragraph(sanitize(line.strip()), title_st))
        story.append(Spacer(1, 4))

    doc.build(story)


def create_multi_col_table(items, cols, doc_width, style):
    rows = [items[i : i + cols] for i in range(0, len(items), cols)]
    if rows and len(rows[-1]) < cols:
        rows[-1].extend([""] * (cols - len(rows[-1])))

    table_data = []
    for row in rows:
        table_row = []
        for item in row:
            if item.strip():
                table_row.append(
                    Paragraph(f"\u2022\u00a0{sanitize(item.strip())}", style)
                )
            else:
                table_row.append(Paragraph("", style))
        table_data.append(table_row)

    col_width = doc_width / cols
    return Table(
        table_data,
        colWidths=[col_width] * cols,
        style=[
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
        ],
    )


def render_template_2(doc, story, user_details, spec, doc_width):
    name_st = _style("name", spec, spaceAfter=4)
    contact_st = _style("contact", spec, spaceAfter=14)
    heading_st = _style(
        "section_heading",
        spec,
        spaceBefore=14,
        spaceAfter=2,
        alignment=TA_CENTER,
    )
    org_st = _style("sub_heading", spec, spaceAfter=0)
    org_right_st = _style("body", spec, spaceAfter=0, alignment=TA_RIGHT)
    title_st = _style("sub_heading", spec, spaceAfter=2, _italic=True)
    body_st = _style("body", spec, spaceAfter=2)
    bullet_st = _style("bullet", spec, spaceAfter=2, leftIndent=14)

    def append_heading(title):
        story.append(Paragraph(title, heading_st))
        story.append(
            HRFlowable(
                width="100%",
                thickness=0.6,
                color=black,
                spaceAfter=4,
                spaceBefore=2,
            )
        )

    contact = user_details.get("Contact", {})
    name = contact.get("Name", "Your Name")
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    profiles = contact.get("Profiles", [])

    story.append(Paragraph(sanitize(name), name_st))
    c_parts = [sanitize(p.strip()) for p in [email, phone] if p.strip()]
    c_parts.extend(format_profiles(profiles))
    if c_parts:
        story.append(Paragraph(" \u2022 ".join(c_parts), contact_st))

    education = user_details.get("Education", [])
    if education:
        append_heading("Education")
        for edu in education:
            org_p = Paragraph(sanitize(edu.get("school", "")), org_st)
            story.append(org_p)

            deg = sanitize(edu.get("degree", ""))
            dates = sanitize(edu.get("dates", ""))
            story.append(
                create_row_table(
                    Paragraph(deg, body_st),
                    Paragraph(dates, org_right_st),
                    doc_width,
                )
            )

            gpa = sanitize(edu.get("gpa", ""))
            if gpa:
                story.append(Paragraph(gpa, body_st))

            bullets = edu.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 4))

    skills = user_details.get("Skills", "").strip()
    if skills:
        append_heading("Technical Skills")
        items = [line.strip() for line in skills.split("\n") if line.strip()]
        if items:
            story.append(create_multi_col_table(items, 4, doc_width, body_st))
            story.append(Spacer(1, 4))

    experience = user_details.get("Experience", [])
    if experience:
        append_heading("Professional Experience")
        for exp in experience:
            org_p = Paragraph(sanitize(exp.get("company", "")), org_st)
            loc_p = Paragraph(sanitize(exp.get("location", "")), org_right_st)
            story.append(create_row_table(org_p, loc_p, doc_width))

            tit_p = Paragraph(sanitize(exp.get("title", "")), title_st)
            dat_p = Paragraph(sanitize(exp.get("dates", "")), org_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = exp.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))
            
    projects = user_details.get("Projects", [])
    if projects:
        append_heading("Projects")
        for proj in projects:
            title_text = format_project_title(proj.get("title", ""), proj.get("link", ""))
            tit_p = Paragraph(title_text, title_st)
            dat_p = Paragraph(sanitize(proj.get("dates", "")), org_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = proj.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    certifications = user_details.get("Certifications", "").strip()
    if certifications:
        append_heading("Certifications")
        for line in certifications.split("\n"):
            line = line.strip()
            if not line:
                continue

            # split by '-' or ' - ' to separate name and date. The image shows:
            # "Name - Date"
            parts = line.rsplit(" - ", 1)
            if len(parts) == 2:
                left = Paragraph(
                    f"\u2022\u00a0{sanitize(parts[0].strip())}", body_st
                )
                right = Paragraph(sanitize(parts[1].strip()), org_right_st)
                story.append(create_row_table(left, right, doc_width))
            else:
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", body_st)
                )
        story.append(Spacer(1, 4))

    doc.build(story)


def render_template_3(doc, story, user_details, spec, doc_width):
    import re

    name_st = _style("name", spec, spaceAfter=2, alignment=TA_CENTER)
    contact_st = _style("contact", spec, spaceAfter=2, alignment=TA_CENTER)
    heading_st = _style(
        "section_heading",
        spec,
        spaceBefore=14,
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    org_st = _style("sub_heading", spec, spaceAfter=0)
    org_right_st = _style("body", spec, spaceAfter=0, alignment=TA_RIGHT)
    title_st = _style("body", spec, spaceAfter=2)
    _style("body", spec, spaceAfter=2)
    bullet_st = _style("bullet", spec, spaceAfter=2, leftIndent=14)

    def append_heading(title):
        story.append(Paragraph(title, heading_st))

    contact = user_details.get("Contact", {})
    name = contact.get("Name", "Your Name")
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    profiles = contact.get("Profiles", [])

    story.append(Paragraph(sanitize(name), name_st))
    c_parts = [sanitize(p.strip()) for p in [email, phone] if p.strip()]
    if c_parts:
        story.append(Paragraph(" | ".join(c_parts), contact_st))
        
    p_parts = format_profiles(profiles)
    if p_parts:
        story.append(Paragraph(" | ".join(p_parts), contact_st))

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.6,
            color=black,
            spaceAfter=10,
            spaceBefore=6,
        )
    )

    education = user_details.get("Education", [])
    if education:
        append_heading("EDUCATION")
        for edu in education:
            org_p = Paragraph(sanitize(edu.get("school", "")), org_st)
            loc_p = Paragraph(sanitize(edu.get("dates", "")), org_right_st)
            story.append(create_row_table(org_p, loc_p, doc_width))

            deg = sanitize(edu.get("degree", ""))
            story.append(Paragraph(deg, title_st))

            bullets = edu.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    experience = user_details.get("Experience", [])
    if experience:
        append_heading("PROFESSIONAL EXPERIENCE")
        for exp in experience:
            org_p = Paragraph(sanitize(exp.get("company", "")), org_st)
            dat_p = Paragraph(sanitize(exp.get("dates", "")), org_right_st)
            story.append(create_row_table(org_p, dat_p, doc_width))

            tit_p = Paragraph(sanitize(exp.get("title", "")), title_st)
            story.append(tit_p)

            bullets = exp.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    projects = user_details.get("Projects", [])
    if projects:
        append_heading("PROJECTS")
        for proj in projects:
            title_text = format_project_title(proj.get("title", ""), proj.get("link", ""))
            tit_p = Paragraph(title_text, title_st)
            dat_p = Paragraph(sanitize(proj.get("dates", "")), org_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = proj.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    interests = user_details.get("Interests", "").strip()
    if interests:
        append_heading("VOLUNTEER EXPERIENCE")
        for line in interests.split("\n"):
            line = line.strip()
            if not line:
                continue

            safe_line = sanitize(line)
            # Make **text** bold
            safe_line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", safe_line)

            story.append(Paragraph(f"\u2022\u00a0{safe_line}", bullet_st))
        story.append(Spacer(1, 6))

    doc.build(story)


def render_template_4(doc, story, user_details, spec, doc_width):
    import re

    name_st = _style("name", spec, spaceAfter=2, alignment=TA_CENTER)
    contact_st = _style("contact", spec, spaceAfter=2, alignment=TA_CENTER)
    heading_st = _style(
        "section_heading",
        spec,
        spaceBefore=10,
        spaceAfter=2,
        alignment=TA_LEFT,
    )
    org_st = _style("sub_heading", spec, spaceAfter=0)
    org_right_st = _style("body", spec, spaceAfter=0, alignment=TA_RIGHT)
    title_st = _style("sub_heading", spec, spaceAfter=2, _italic=True)
    title_right_st = _style("body", spec, spaceAfter=2, alignment=TA_RIGHT)
    _style("body", spec, spaceAfter=2)
    summary_st = _style("body", spec, spaceAfter=2, leftIndent=30)
    bullet_st = _style("bullet", spec, spaceAfter=2, leftIndent=14)

    def append_heading(title):
        story.append(Paragraph(title, heading_st))

    contact = user_details.get("Contact", {})
    name = contact.get("Name", "Your Name")
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    profiles = contact.get("Profiles", [])

    story.append(Paragraph(sanitize(name), name_st))
    c_parts = [sanitize(p.strip()) for p in [phone, email] if p.strip()]
    c_parts.extend(format_profiles(profiles))
    if c_parts:
        story.append(Paragraph(" / ".join(c_parts), contact_st))

    story.append(
        HRFlowable(
            width="100%",
            thickness=0.6,
            color=black,
            spaceAfter=10,
            spaceBefore=4,
        )
    )

    summary = user_details.get("Summary", "").strip()
    if summary:
        append_heading("Summary")
        for line in summary.split("\n"):
            line = line.strip()
            if line:
                story.append(Paragraph(sanitize(line), summary_st))
        story.append(Spacer(1, 4))

    skills = user_details.get("Skills", "").strip()
    if skills:
        append_heading("Core Competencies")
        items = [line.strip() for line in skills.split("\n") if line.strip()]
        if items:
            story.append(
                create_multi_col_table(items, 4, doc_width, bullet_st)
            )
            story.append(Spacer(1, 4))

    experience = user_details.get("Experience", [])
    if experience:
        append_heading("Experience")
        for exp in experience:
            org = exp.get("company", "").strip()
            if org:
                story.append(Paragraph(sanitize(org), org_st))

            tit_p = Paragraph(sanitize(exp.get("title", "")), title_st)
            dat_p = Paragraph(sanitize(exp.get("dates", "")), title_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = exp.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 4))
            
    projects = user_details.get("Projects", [])
    if projects:
        append_heading("Projects")
        for proj in projects:
            title_text = format_project_title(proj.get("title", ""), proj.get("link", ""))
            tit_p = Paragraph(title_text, title_st)
            dat_p = Paragraph(sanitize(proj.get("dates", "")), title_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = proj.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 4))

    education = user_details.get("Education", [])
    if education:
        append_heading("Education")
        for edu in education:
            org = edu.get("school", "").strip()
            if org:
                org_p = Paragraph(sanitize(org), org_st)
                dat_p = Paragraph(sanitize(edu.get("dates", "")), org_right_st)
                story.append(create_row_table(org_p, dat_p, doc_width))

                deg = sanitize(edu.get("degree", ""))
                story.append(Paragraph(deg, title_st))
            else:
                deg_p = Paragraph(sanitize(edu.get("degree", "")), title_st)
                dat_p = Paragraph(
                    sanitize(edu.get("dates", "")), title_right_st
                )
                story.append(create_row_table(deg_p, dat_p, doc_width))

            bullets = edu.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u2022\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 4))

    interests = user_details.get("Interests", "").strip()
    if interests:
        append_heading("Additional Information")
        for line in interests.split("\n"):
            line = line.strip()
            if not line:
                continue

            safe_line = sanitize(line)
            safe_line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", safe_line)

            story.append(Paragraph(f"\u2022\u00a0{safe_line}", bullet_st))
        story.append(Spacer(1, 4))

    doc.build(story)


def render_template_5(doc, story, user_details, spec, doc_width):
    name_st = _style("name", spec, spaceAfter=2, alignment=TA_CENTER)
    contact_st = _style("contact", spec, spaceAfter=2, alignment=TA_CENTER)
    heading_st = _style(
        "section_heading",
        spec,
        spaceBefore=12,
        spaceAfter=2,
        alignment=TA_CENTER,
    )
    org_st = _style("sub_heading", spec, spaceAfter=0)
    org_right_st = _style("body", spec, spaceAfter=0, alignment=TA_RIGHT)
    title_st = _style("body", spec, spaceAfter=2)
    title_right_st = _style("body", spec, spaceAfter=2, alignment=TA_RIGHT)
    body_st = _style("body", spec, spaceAfter=2)
    bullet_st = _style(
        "bullet", spec, spaceAfter=2, leftIndent=18, bulletIndent=10
    )

    def append_heading(title):
        story.append(Paragraph(title, heading_st))
        story.append(
            HRFlowable(
                width="100%",
                thickness=0.6,
                color=black,
                spaceAfter=8,
                spaceBefore=2,
            )
        )

    contact = user_details.get("Contact", {})
    name = contact.get("Name", "Your Name")
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    location = contact.get("Location", "")
    profiles = contact.get("Profiles", [])

    story.append(Paragraph(sanitize(name), name_st))
    if location:
        story.append(Paragraph(sanitize(location), contact_st))
    c_parts = [sanitize(p.strip()) for p in [email, phone] if p.strip()]
    c_parts.extend(format_profiles(profiles))
    if c_parts:
        story.append(Paragraph(" \u2022 ".join(c_parts), contact_st))

    story.append(Spacer(1, 4))

    education = user_details.get("Education", [])
    if education:
        append_heading("Education")
        for edu in education:
            org = edu.get("school", "").strip()
            if org:
                story.append(Paragraph(sanitize(org), org_st))

            deg_p = Paragraph(sanitize(edu.get("degree", "")), title_st)
            dat_p = Paragraph(sanitize(edu.get("dates", "")), title_right_st)
            story.append(create_row_table(deg_p, dat_p, doc_width))

            bullets = edu.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•", "▪", "■"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                # Using a small square bullet
                story.append(
                    Paragraph(f"\u25aa\u00a0\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    experience = user_details.get("Experience", [])
    if experience:
        append_heading("Professional Experience")
        for exp in experience:
            org_p = Paragraph(sanitize(exp.get("company", "")), org_st)
            loc_p = Paragraph(sanitize(exp.get("location", "")), org_right_st)
            story.append(create_row_table(org_p, loc_p, doc_width))

            tit_p = Paragraph(sanitize(exp.get("title", "")), title_st)
            dat_p = Paragraph(sanitize(exp.get("dates", "")), title_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = exp.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•", "▪", "■"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u25aa\u00a0\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    projects = user_details.get("Projects", [])
    if projects:
        append_heading("Projects")
        for proj in projects:
            title_text = format_project_title(proj.get("title", ""), proj.get("link", ""))
            tit_p = Paragraph(title_text, title_st)
            dat_p = Paragraph(sanitize(proj.get("dates", "")), title_right_st)
            story.append(create_row_table(tit_p, dat_p, doc_width))

            bullets = proj.get("bullets", "")
            for line in bullets.split("\n"):
                line = line.strip()
                if not line:
                    continue
                for prefix in ("- ", "* ", "• ", "-", "*", "•", "▪", "■"):
                    if line.startswith(prefix):
                        line = line[len(prefix) :].strip()
                        break
                story.append(
                    Paragraph(f"\u25aa\u00a0\u00a0{sanitize(line)}", bullet_st)
                )
            story.append(Spacer(1, 6))

    skills = user_details.get("Skills", "").strip()
    if skills:
        append_heading("Technical Expertise")
        for line in skills.split("\n"):
            line = line.strip()
            if line:
                story.append(Paragraph(sanitize(line), body_st))
        story.append(Spacer(1, 6))

    interests = user_details.get("Interests", "").strip()
    if interests:
        append_heading("Additional")
        for line in interests.split("\n"):
            line = line.strip()
            if line:
                story.append(Paragraph(sanitize(line), body_st))
        story.append(Spacer(1, 6))

    doc.build(story)


def render_template_generic(
    doc, story, user_details, spec, template_choice, doc_width
):
    name_st = _style("name", spec, spaceAfter=4)
    contact_st = _style("contact", spec, spaceAfter=14)
    heading_st = _style("section_heading", spec, spaceBefore=14, spaceAfter=2)
    org_st = _style("sub_heading", spec, spaceAfter=0)
    org_right_st = _style("body", spec, spaceAfter=0, alignment=TA_RIGHT)
    title_st = _style("sub_heading", spec, spaceAfter=2, _italic=True)
    title_right_st = _style("body", spec, spaceAfter=2, alignment=TA_RIGHT)
    body_st = _style("body", spec, spaceAfter=2)
    bullet_st = _style("bullet", spec, spaceAfter=2, leftIndent=14)

    contact = user_details.get("Contact", {})
    name = contact.get("Name", "Your Name")
    email = contact.get("Email", "")
    phone = contact.get("Phone", "")
    location = contact.get("Location", "")
    profiles = contact.get("Profiles", [])
    
    story.append(Paragraph(sanitize(name), name_st))
    c_parts = [sanitize(p.strip()) for p in [location, phone, email] if p.strip()]
    c_parts.extend(format_profiles(profiles))
    if c_parts:
        story.append(Paragraph("  |  ".join(c_parts), contact_st))

    schema = TEMPLATE_SCHEMA.get(
        template_choice, TEMPLATE_SCHEMA.get("default", {})
    )
    header_align = schema.get("header_align", "left")
    has_line = schema.get("has_line", True)
    fields = schema.get(
        "fields", ["contact", "summary", "experience", "education", "skills"]
    )

    if header_align == "center":
        heading_st.alignment = TA_CENTER
    else:
        heading_st.alignment = TA_LEFT

    def append_heading(title):
        story.append(Paragraph(title, heading_st))
        if has_line:
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.6,
                    color=black,
                    spaceAfter=4,
                    spaceBefore=2,
                )
            )

    for field in fields:
        if field == "contact":
            pass
        elif field == "summary":
            summary = user_details.get("Summary", "").strip()
            if summary:
                append_heading("SUMMARY")
                for line in summary.split("\n"):
                    if line.strip():
                        story.append(
                            Paragraph(sanitize(line.strip()), body_st)
                        )
                story.append(Spacer(1, 4))
        elif field == "objective":
            objective = user_details.get("Objective", "").strip()
            if objective:
                append_heading("OBJECTIVE")
                for line in objective.split("\n"):
                    if line.strip():
                        story.append(
                            Paragraph(sanitize(line.strip()), body_st)
                        )
                story.append(Spacer(1, 4))
        elif field == "experience":
            experience = user_details.get("Experience", [])
            if experience:
                append_heading("EXPERIENCE")
                for exp in experience:
                    org_p = Paragraph(sanitize(exp.get("company", "")), org_st)
                    loc_p = Paragraph(
                        sanitize(exp.get("location", "")), org_right_st
                    )
                    story.append(create_row_table(org_p, loc_p, doc_width))
                    tit_p = Paragraph(sanitize(exp.get("title", "")), title_st)
                    dat_p = Paragraph(
                        sanitize(exp.get("dates", "")), title_right_st
                    )
                    story.append(create_row_table(tit_p, dat_p, doc_width))
                    bullets = exp.get("bullets", "")
                    for line in bullets.split("\n"):
                        line = line.strip()
                        if not line:
                            continue
                        for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                            if line.startswith(prefix):
                                line = line[len(prefix) :].strip()
                                break
                        story.append(
                            Paragraph(
                                f"\u2022\u00a0{sanitize(line)}", bullet_st
                            )
                        )
                    story.append(Spacer(1, 6))
        elif field == "projects":
            projects = user_details.get("Projects", [])
            if projects:
                append_heading("PROJECTS")
                for proj in projects:
                    title_text = format_project_title(proj.get("title", ""), proj.get("link", ""))
                    tit_p = Paragraph(title_text, title_st)
                    dat_p = Paragraph(
                        sanitize(proj.get("dates", "")), title_right_st
                    )
                    story.append(create_row_table(tit_p, dat_p, doc_width))
                    bullets = proj.get("bullets", "")
                    for line in bullets.split("\n"):
                        line = line.strip()
                        if not line:
                            continue
                        for prefix in ("- ", "* ", "• ", "-", "*", "•"):
                            if line.startswith(prefix):
                                line = line[len(prefix) :].strip()
                                break
                        story.append(
                            Paragraph(
                                f"\u2022\u00a0{sanitize(line)}", bullet_st
                            )
                        )
                    story.append(Spacer(1, 6))
        elif field == "education":
            education = user_details.get("Education", [])
            if education:
                append_heading("EDUCATION")
                for edu in education:
                    org_p = Paragraph(sanitize(edu.get("school", "")), org_st)
                    loc_p = Paragraph(
                        sanitize(edu.get("location", "")), org_right_st
                    )
                    story.append(create_row_table(org_p, loc_p, doc_width))
                    deg_p = Paragraph(
                        sanitize(edu.get("degree", "")), title_st
                    )
                    date_p = Paragraph(
                        sanitize(edu.get("dates", "")), title_right_st
                    )
                    story.append(create_row_table(deg_p, date_p, doc_width))
                    story.append(Spacer(1, 4))
        elif field == "skills":
            skills = user_details.get("Skills", "").strip()
            if skills:
                append_heading("SKILLS")
                for line in skills.split("\n"):
                    if line.strip():
                        story.append(
                            Paragraph(sanitize(line.strip()), body_st)
                        )
                story.append(Spacer(1, 4))
        elif field == "certifications":
            certifications = user_details.get("Certifications", "").strip()
            if certifications:
                append_heading("CERTIFICATIONS")
                for line in certifications.split("\n"):
                    if line.strip():
                        story.append(
                            Paragraph(sanitize(line.strip()), body_st)
                        )
                story.append(Spacer(1, 4))
        elif field == "interests":
            interests = user_details.get("Interests", "").strip()
            if interests:
                append_heading("INTERESTS")
                for line in interests.split("\n"):
                    if line.strip():
                        story.append(
                            Paragraph(sanitize(line.strip()), body_st)
                        )
                story.append(Spacer(1, 4))

    doc.build(story)
