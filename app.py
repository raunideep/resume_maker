import streamlit as st
import io
import streamlit.components.v1 as components
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="AI Multi-Style Resume Generator", page_icon="🎨", layout="wide")

# Custom styling to remove form border and clean up inputs
st.markdown("""
<style>
/* Remove the outer st.form border box */
[data-testid="stForm"] {
    border: none !important;
    padding: 0px !important;
    background: transparent !important;
}

/* Style input fields */
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div {
    background-color: #1A202C !important;
    border: 1px solid #4A5568 !important;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Professional Resume & Cover Letter Generator")
st.markdown("Build a full-page, stylish resume with instant visual layout switching for **Sahitool**.")

col_form, col_preview = st.columns([1, 1.2])

with col_form:
    st.subheader("📝 Enter Your Details")
    with st.form("resume_form"):
        full_name = st.text_input("Full Name", value="Rahul Sharma", placeholder="e.g. Rahul Sharma")
        job_title = st.text_input("Target Job Title", value="Solar Design Engineer", placeholder="e.g. Solar Design Engineer")
        
        c1, c2 = st.columns(2)
        with c1:
            email = st.text_input("Email", value="rahul@sahitool.com")
        with c2:
            phone = st.text_input("Phone", value="##########")
            
        photo_url = st.text_input("Optional Photo Image URL", value="", placeholder="https://example.com/photo.jpg")
        
        education = st.text_input("Education / Degree", value="B.Tech in Electrical & Automation Engineering")
        skills = st.text_input("Key Skills (Comma separated)", value="Python, CAD, Solar Systems, Automation, UI/UX")
        experience = st.text_area("Work Experience / Projects", value="• Designed high-efficiency solar pump systems reducing power loss by 18%.\n• Developed automated Python workflows for system tracking and real-time data logging.")
        
        template_style = st.selectbox(
            "Choose Resume Style Design",
            [
                "1. Sunshine (Bright Accent)", 
                "2. Elegant Executive (Left Sidebar)", 
                "3. Modern Corporate (Clean Blue)", 
                "4. Minimalist Classic (Simple)",
                "5. Creative Bold (Dark Contrast)",
                "6. Startup Fresh (Green Accent)",
                "7. Compact Grid (Two-Column Skills)",
                "8. Professional Timeline",
                "9. Executive Split",
                "10. Simple ATS-Friendly"
            ]
        )
        
        submitted = st.form_submit_button("Update & Preview Resume Sheet")

def generate_pdf(name, title, mail, ph, edu, sk, exp, style_name):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    if "Sunshine" in style_name:
        accent_color = colors.HexColor("#D69E2E")
    elif "Startup Fresh" in style_name:
        accent_color = colors.HexColor("#2F855A")
    elif "Creative Bold" in style_name:
        accent_color = colors.HexColor("#1A202C")
    elif "Elegant Executive" in style_name or "Executive Split" in style_name:
        accent_color = colors.HexColor("#2B6CB0")
    elif "Minimalist Classic" in style_name:
        accent_color = colors.HexColor("#4A5568")
    else:
        accent_color = colors.HexColor("#1A365D")

    name_style = ParagraphStyle('DocName', fontName='Helvetica-Bold', fontSize=22, textColor=accent_color, spaceAfter=2, leading=26)
    title_style = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#4A5568"), spaceAfter=4, leading=15)
    contact_style = ParagraphStyle('DocContact', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#718096"), spaceAfter=0, leading=13)
    
    heading_style = ParagraphStyle('SectionHeading', fontName='Helvetica-Bold', fontSize=12, textColor=accent_color, spaceBefore=14, spaceAfter=3, leading=15)
    body_style = ParagraphStyle('BodyDark', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#2D3748"), spaceAfter=4, leading=14)
    
    sidebar_heading = ParagraphStyle('SideHeading', fontName='Helvetica-Bold', fontSize=11, textColor=accent_color, spaceBefore=8, spaceAfter=4, leading=13)
    sidebar_body = ParagraphStyle('SideBody', fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#4A5568"), spaceAfter=4, leading=12)

    is_sidebar_layout = "Elegant Executive" in style_name or "Executive Split" in style_name

    if is_sidebar_layout:
        sidebar_story = [
            Paragraph("CONTACT", sidebar_heading),
            HRFlowable(width="100%", thickness=1, color=accent_color, spaceBefore=1, spaceAfter=4),
            Paragraph(f"<b>Email:</b><br/>{mail}", sidebar_body),
            Paragraph(f"<b>Phone:</b><br/>{ph}", sidebar_body),
            Spacer(1, 10),
            Paragraph("CORE SKILLS", sidebar_heading),
            HRFlowable(width="100%", thickness=1, color=accent_color, spaceBefore=1, spaceAfter=4),
        ]
        for skill in [s.strip() for s in sk.split(",")]:
            if skill:
                sidebar_story.append(Paragraph(f"• {skill}", sidebar_body))

        main_story = [
            Paragraph(name.upper(), name_style),
            Paragraph(title, title_style),
            Spacer(1, 6),
            Paragraph("SUMMARY", heading_style),
            HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=1, spaceAfter=6),
            Paragraph(f"Dedicated {title} with solid technical expertise and project execution capability.", body_style),
            
            Paragraph("EDUCATION", heading_style),
            HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=1, spaceAfter=6),
            Paragraph(f"• {edu}", body_style),
            
            Paragraph("EXPERIENCE", heading_style),
            HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=1, spaceAfter=6)
        ]
        for line in exp.split("\n"):
            if line.strip():
                main_story.append(Paragraph(line.strip(), body_style))

        layout_table = Table([[sidebar_story, main_story]], colWidths=[180, 350])
        layout_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (0,0), 0),
            ('RIGHTPADDING', (0,0), (0,0), 10),
            ('LEFTPADDING', (1,0), (1,0), 15),
            ('RIGHTPADDING', (1,0), (1,0), 0),
        ]))
        story.append(layout_table)

    else:
        story.append(Paragraph(name.upper(), name_style))
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(f"{mail}  &nbsp;|&nbsp;  {ph}", contact_style))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=2, color=accent_color, spaceBefore=2, spaceAfter=10))

        def add_section(title_text):
            story.append(Paragraph(title_text, heading_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=1, spaceAfter=6))

        add_section("PROFESSIONAL SUMMARY")
        story.append(Paragraph(f"Dedicated and result-oriented {title} with proven expertise in project execution, system optimization, and cutting-edge technical implementations.", body_style))

        add_section("EDUCATION")
        story.append(Paragraph(f"• {edu}", body_style))

        add_section("CORE COMPETENCIES")
        
        skill_list = [s.strip() for s in sk.split(",") if s.strip()]
        skill_rows = []
        for i in range(0, len(skill_list), 2):
            col1 = Paragraph(f"• {skill_list[i]}", body_style)
            col2 = Paragraph(f"• {skill_list[i+1]}", body_style) if i+1 < len(skill_list) else Paragraph("", body_style)
            skill_rows.append([col1, col2])
            
        if skill_rows:
            skills_table = Table(skill_rows, colWidths=[270, 270])
            skills_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ]))
            story.append(skills_table)
            story.append(Spacer(1, 4))

        add_section("EXPERIENCE & PROJECTS")
        for line in exp.split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

with col_preview:
    st.subheader("👁️ Live Full-Page Sheet Preview")
    
    accent_color = "#1A365D"
    layout_type = "standard"
    
    if "Sunshine" in template_style:
        accent_color = "#D69E2E"
    elif "Elegant Executive" in template_style or "Executive Split" in template_style:
        layout_type = "sidebar"
        accent_color = "#2B6CB0"
    elif "Creative Bold" in template_style:
        accent_color = "#1A202C"
    elif "Startup Fresh" in template_style:
        accent_color = "#2F855A"
    elif "Minimalist Classic" in template_style:
        accent_color = "#4A5568"

    skills_html = "".join([f"<li style='margin-bottom: 4px;'>{s.strip()}</li>" for s in skills.split(",") if s.strip()])
    skills_grid_html = "".join([f"<div style='margin-bottom: 4px;'>• {s.strip()}</div>" for s in skills.split(",") if s.strip()])
    exp_html = "".join([f"<p style='margin: 4px 0; font-size: 13px; color: #2D3748;'>{line.strip()}</p>" for line in experience.split("\n") if line.strip()])

    photo_html = ""
    if photo_url.strip():
        photo_html = f"""<img src="{photo_url}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid {accent_color}; float: right;" />"""

    if layout_type == "sidebar":
        resume_sheet_html = f"""
        <div style="background: white; color: #333; padding: 30px; border-radius: 4px; border: 1px solid #E2E8F0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.05); min-height: 750px; box-sizing: border-box; display: flex; gap: 25px;">
            <div style="width: 35%; padding-right: 15px; border-right: 2px solid #EDF2F7; height: fit-content;">
                {f'<div style="text-align: center; margin-bottom: 15px;"><img src="{photo_url}" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border: 2px solid {accent_color};" /></div>' if photo_url.strip() else ''}
                <h3 style="color: {accent_color}; font-size: 13px; border-bottom: 2px solid {accent_color}; padding-bottom: 3px; margin-bottom: 8px;">CONTACT</h3>
                <p style="font-size: 11px; color: #4A5568; word-break: break-all; margin: 0 0 10px 0;"><b>Email:</b><br>{email}</p>
                <p style="font-size: 11px; color: #4A5568; margin: 0 0 15px 0;"><b>Phone:</b><br>{phone}</p>
                
                <h3 style="color: {accent_color}; font-size: 13px; border-bottom: 2px solid {accent_color}; padding-bottom: 3px; margin-bottom: 8px;">CORE SKILLS</h3>
                <ul style="margin: 0; padding-left: 15px; font-size: 11px; color: #2D3748;">
                    {skills_html}
                </ul>
            </div>
            <div style="width: 65%;">
                <h1 style="color: {accent_color}; margin: 0 0 4px 0; font-size: 22px;">{full_name.upper()}</h1>
                <p style="color: #4A5568; font-weight: bold; margin: 0 0 15px 0; font-size: 12px;">{job_title}</p>
                <div style="margin-bottom: 14px;">
                    <h3 style="color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 3px; font-size: 13px; margin-bottom: 6px;">SUMMARY</h3>
                    <p style="font-size: 12px; color: #2D3748; line-height: 1.4; margin: 0;">Dedicated {job_title} with solid technical expertise and project execution capability.</p>
                </div>
                <div style="margin-bottom: 14px;">
                    <h3 style="color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 3px; font-size: 13px; margin-bottom: 6px;">EDUCATION</h3>
                    <p style="font-size: 12px; color: #2D3748; margin: 0;">{education}</p>
                </div>
                <div>
                    <h3 style="color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 3px; font-size: 13px; margin-bottom: 6px;">EXPERIENCE</h3>
                    {exp_html}
                </div>
            </div>
        </div>
        """
    else:
        resume_sheet_html = f"""
        <div style="background: white; color: #333; padding: 40px; border-radius: 4px; border: 1px solid #E2E8F0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; box-shadow: 0 4px 12px rgba(0,0,0,0.05); min-height: 750px; box-sizing: border-box;">
            <div style="margin-bottom: 20px; border-bottom: 2px solid {accent_color}; padding-bottom: 15px; overflow: hidden;">
                {photo_html}
                <h1 style="color: {accent_color}; margin: 0 0 4px 0; font-size: 24px; letter-spacing: 0.5px;">{full_name.upper()}</h1>
                <p style="color: #4A5568; font-weight: bold; margin: 0; font-size: 13px;">{job_title}</p>
                <p style="color: #718096; margin: 5px 0 0 0; font-size: 12px;">{email} &nbsp;|&nbsp; {phone}</p>
            </div>
            <div style="margin-bottom: 20px;">
                <h3 style="color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 4px; font-size: 14px; margin-bottom: 8px;">PROFESSIONAL SUMMARY</h3>
                <p style="font-size: 13px; color: #2D3748; line-height: 1.5; margin: 0;">
                    Dedicated and result-oriented {job_title} with proven expertise in project execution, system optimization, and cutting-edge technical implementations.
                </p>
            </div>
            <div style="margin-bottom: 20px;">
                <h3 style="color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 4px; font-size: 14px; margin-bottom: 8px;">EDUCATION</h3>
                <p style="font-size: 13px; color: #2D3748; margin: 0; font-weight: 500;">{education}</p>
            </div>
            <div style="margin-bottom: 20px;">
                <h3 style="color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 4px; font-size: 14px; margin-bottom: 8px;">CORE COMPETENCIES</h3>
                <div style="font-size: 13px; color: #2D3748; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 20px;">
                    {skills_grid_html}
                </div>
            </div>
            <div style="margin-bottom: 10px;">
                <h3 style="color: {accent_color}; border-bottom: 2px solid {accent_color}; padding-bottom: 4px; font-size: 14px; margin-bottom: 8px;">EXPERIENCE & PROJECTS</h3>
                {exp_html}
            </div>
        </div>
        """
    
    components.html(resume_sheet_html, height=780, scrolling=True)
    st.write("")

    pdf_buffer = generate_pdf(full_name, job_title, email, phone, education, skills, experience, template_style)
    
    st.download_button(
        label="📥 Download Full-Page Styled PDF Resume",
        data=pdf_buffer,
        file_name=f"{full_name.replace(' ', '_')}_Resume.pdf",
        mime="application/pdf",
        use_container_width=True
    )