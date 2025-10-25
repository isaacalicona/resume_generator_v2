"""
COMPLEX Professional Resume Templates
Visually interesting layouts with structure and design
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors


class ModernTwoColumnTemplate:
    """Complex two-column layout like the example - visually interesting!"""
    
    @staticmethod
    def create_pdf(resume_data, user_info, output_filename, accent_color='#4A90E2'):
        """
        Modern template with two-column work history and full-width colored headers
        """
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.4*inch,
            bottomMargin=0.4*inch
        )
        
        elements = []
        
        # Parse color
        header_color = colors.HexColor(accent_color)
        
        # Styles - MUCH BIGGER NAME
        name_style = ParagraphStyle(
            'Name',
            fontSize=48,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=8,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            leading=52,
            letterSpacing=2
        )
        
        contact_style = ParagraphStyle(
            'Contact',
            fontSize=10,
            textColor=colors.HexColor('#4a5568'),
            spaceAfter=20,
            alignment=TA_CENTER,
            leading=14
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            fontSize=13,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            leftIndent=15,
            leading=16
        )
        
        body_style = ParagraphStyle(
            'Body',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#2d3748'),
            alignment=TA_LEFT,
            spaceBefore=8
        )
        
        # NAME - HUGE and bold
        name = user_info.get('name', 'Your Name').upper()
        elements.append(Paragraph(name, name_style))
        
        # Contact - single line
        contact_parts = []
        if user_info.get('email'):
            contact_parts.append(user_info['email'])
        if user_info.get('phone'):
            contact_parts.append(f"H: {user_info['phone']}")
        if user_info.get('location'):
            contact_parts.append(user_info['location'])
        
        contact_text = ' | '.join(contact_parts)
        elements.append(Paragraph(contact_text, contact_style))
        
        # PROFESSIONAL SUMMARY - Full width colored bar
        summary_table = Table(
            [[Paragraph('PROFESSIONAL SUMMARY', section_title_style)]],
            colWidths=[7.5*inch]
        )
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), header_color),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Summary text
        elements.append(Paragraph(resume_data.get('summary', ''), body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # SKILLS - Full width colored bar
        if resume_data.get('skills'):
            skills_table = Table(
                [[Paragraph('SKILLS', section_title_style)]],
                colWidths=[7.5*inch]
            )
            skills_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), header_color),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 15),
            ]))
            elements.append(skills_table)
            elements.append(Spacer(1, 0.15*inch))
            
            # Skills in TWO columns like the example
            skills = resume_data['skills']
            skill_style = ParagraphStyle('Skill', fontSize=10, leading=16, textColor=colors.HexColor('#2d3748'))
            
            # Split into two columns
            mid = (len(skills) + 1) // 2
            left_skills = skills[:mid]
            right_skills = skills[mid:]
            
            # Make equal length
            while len(left_skills) < len(right_skills):
                left_skills.append('')
            while len(right_skills) < len(left_skills):
                right_skills.append('')
            
            skill_data = []
            for left, right in zip(left_skills, right_skills):
                row = [
                    Paragraph(f'• {left}' if left else '', skill_style),
                    Paragraph(f'• {right}' if right else '', skill_style)
                ]
                skill_data.append(row)
            
            skill_table = Table(skill_data, colWidths=[3.75*inch, 3.75*inch])
            skill_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (0,-1), 15),
                ('LEFTPADDING', (1,0), (1,-1), 15),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ]))
            elements.append(skill_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # WORK HISTORY - Full width colored bar
        if resume_data.get('experience'):
            work_table = Table(
                [[Paragraph('WORK HISTORY', section_title_style)]],
                colWidths=[7.5*inch]
            )
            work_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), header_color),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 15),
            ]))
            elements.append(work_table)
            elements.append(Spacer(1, 0.15*inch))
            
            # TWO-COLUMN LAYOUT for work history - dates/title on LEFT, bullets on RIGHT
            for exp in resume_data['experience']:
                date_style = ParagraphStyle('Date', fontSize=9.5, textColor=colors.HexColor('#4a5568'), leading=13, spaceAfter=2)
                title_style = ParagraphStyle('Title', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1a202c'), leading=13, spaceAfter=2)
                company_style = ParagraphStyle('Company', fontSize=10, textColor=colors.HexColor('#2d3748'), leading=13)
                achievement_style = ParagraphStyle('Achievement', fontSize=10, leading=15, textColor=colors.HexColor('#2d3748'), spaceAfter=3)
                
                # Build LEFT COLUMN as single string with line breaks
                left_text = f"{exp.get('period', '')}<br/>"
                left_text += f"<b>{exp.get('title', '')}</b><br/>"
                left_text += f"{exp.get('company', '')}"
                left_para = Paragraph(left_text, date_style)
                
                # Build RIGHT COLUMN as list of bullet paragraphs  
                right_paras = []
                for achievement in exp.get('achievements', []):
                    right_paras.append(Paragraph(f'• {achievement}', achievement_style))
                
                # Create two-column table - LEFT narrow, RIGHT wide
                exp_data = [[left_para, right_paras]]
                exp_table = Table(exp_data, colWidths=[2.2*inch, 5.3*inch], rowHeights=None)
                exp_table.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (0,-1), 15),
                    ('LEFTPADDING', (1,0), (1,-1), 30),
                    ('RIGHTPADDING', (0,0), (-1,-1), 15),
                    ('TOPPADDING', (0,0), (-1,-1), 5),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ]))
                elements.append(exp_table)
                elements.append(Spacer(1, 0.12*inch))
        
        # EDUCATION - Full width colored bar
        if resume_data.get('education'):
            edu_table = Table(
                [[Paragraph('EDUCATION', section_title_style)]],
                colWidths=[7.5*inch]
            )
            edu_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), header_color),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 15),
            ]))
            elements.append(edu_table)
            elements.append(Spacer(1, 0.15*inch))
            
            for edu in resume_data['education']:
                edu_style = ParagraphStyle('Edu', fontSize=10, leading=14, textColor=colors.HexColor('#2d3748'))
                date_style = ParagraphStyle('EduDate', fontSize=9.5, textColor=colors.HexColor('#4a5568'))
                
                # Format: Year on left, degree and school on same line
                edu_text = f"{edu.get('year', '')}<br/><b>{edu.get('degree', '')}</b>: {edu.get('institution', '')}"
                elements.append(Paragraph(edu_text, edu_style))
                elements.append(Spacer(1, 0.1*inch))
        
        doc.build(elements)


class VisualBlockTemplate:
    """Eye-catching template with visual blocks and sections"""
    
    @staticmethod
    def create_pdf(resume_data, user_info, output_filename, accent_color='#2563eb'):
        """
        Template with visual blocks and interesting structure
        """
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.4*inch,
            bottomMargin=0.4*inch
        )
        
        elements = []
        
        # Colors
        primary_color = colors.HexColor(accent_color)
        dark_text = colors.HexColor('#1a202c')
        light_text = colors.HexColor('#4a5568')
        
        # BIG NAME with colored background box
        name_style = ParagraphStyle(
            'Name',
            fontSize=42,
            textColor=colors.white,
            spaceAfter=0,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            leading=50
        )
        
        # Name in colored box
        name_table = Table(
            [[Paragraph(user_info.get('name', 'Your Name').upper(), name_style)]],
            colWidths=[7.5*inch]
        )
        name_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), primary_color),
            ('TOPPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        elements.append(name_table)
        elements.append(Spacer(1, 0.08*inch))
        
        # Contact info
        contact_style = ParagraphStyle('Contact', fontSize=10, alignment=TA_CENTER, textColor=light_text)
        contact_parts = []
        if user_info.get('email'):
            contact_parts.append(user_info['email'])
        if user_info.get('phone'):
            contact_parts.append(user_info['phone'])
        if user_info.get('location'):
            contact_parts.append(user_info['location'])
        
        elements.append(Paragraph(' | '.join(contact_parts), contact_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Section header style
        section_style = ParagraphStyle(
            'Section',
            fontSize=14,
            textColor=primary_color,
            fontName='Helvetica-Bold',
            leftIndent=0,
            borderWidth=0,
            borderPadding=5,
            borderColor=primary_color,
            spaceAfter=8
        )
        
        body_style = ParagraphStyle('Body', fontSize=10, leading=14, textColor=dark_text)
        
        # Summary with left border
        summary_table = Table(
            [[Paragraph('PROFILE', section_style)], [Paragraph(resume_data.get('summary', ''), body_style)]],
            colWidths=[7.5*inch]
        )
        summary_table.setStyle(TableStyle([
            ('LINEABOVE', (0,0), (0,0), 3, primary_color),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (0,0), 10),
            ('TOPPADDING', (0,1), (0,1), 5),
            ('BOTTOMPADDING', (0,1), (0,1), 10),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Skills in boxes
        if resume_data.get('skills'):
            elements.append(Paragraph('EXPERTISE', section_style))
            elements.append(Spacer(1, 0.08*inch))
            
            # Create skill boxes
            skill_style = ParagraphStyle('Skill', fontSize=9, alignment=TA_CENTER, textColor=dark_text)
            skill_boxes = []
            for i in range(0, len(resume_data['skills']), 4):
                row_skills = resume_data['skills'][i:i+4]
                while len(row_skills) < 4:
                    row_skills.append('')
                skill_boxes.append([Paragraph(s, skill_style) if s else '' for s in row_skills])
            
            skill_table = Table(skill_boxes, colWidths=[1.875*inch]*4)
            skill_table.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
                ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(skill_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('EXPERIENCE', section_style))
            elements.append(Spacer(1, 0.08*inch))
            
            for exp in resume_data['experience']:
                title_style = ParagraphStyle('Title', fontSize=11, fontName='Helvetica-Bold', textColor=dark_text)
                meta_style = ParagraphStyle('Meta', fontSize=9.5, textColor=light_text)
                
                # Experience box
                exp_content = []
                exp_content.append(Paragraph(exp.get('title', ''), title_style))
                exp_content.append(Paragraph(f"{exp.get('company', '')} | {exp.get('period', '')}", meta_style))
                exp_content.append(Spacer(1, 0.05*inch))
                
                for achievement in exp.get('achievements', []):
                    exp_content.append(Paragraph(f'• {achievement}', body_style))
                
                exp_table = Table([[exp_content]], colWidths=[7.5*inch])
                exp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
                    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
                    ('TOPPADDING', (0,0), (-1,-1), 10),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                    ('LEFTPADDING', (0,0), (-1,-1), 12),
                    ('RIGHTPADDING', (0,0), (-1,-1), 12),
                ]))
                elements.append(exp_table)
                elements.append(Spacer(1, 0.12*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', section_style))
            elements.append(Spacer(1, 0.08*inch))
            
            for edu in resume_data['education']:
                edu_style = ParagraphStyle('Edu', fontSize=10, textColor=dark_text)
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')} ({edu.get('year', '')})"
                elements.append(Paragraph(edu_text, edu_style))
                elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements)


# Color schemes
ACCENT_COLORS = {
    'blue': '#4A90E2',
    'indigo': '#6366f1',
    'teal': '#14b8a6',
    'emerald': '#10b981',
    'violet': '#8b5cf6',
    'rose': '#f43f5e',
    'amber': '#f59e0b',
    'cyan': '#06b6d4',
}


def create_complex_resume(resume_data, user_info, output_filename, template='modern', color='blue'):
    """Create resume with complex layout"""
    color_hex = ACCENT_COLORS.get(color, ACCENT_COLORS['blue'])
    
    if template == 'modern':
        ModernTwoColumnTemplate.create_pdf(resume_data, user_info, output_filename, accent_color=color_hex)
    elif template == 'visual':
        VisualBlockTemplate.create_pdf(resume_data, user_info, output_filename, accent_color=color_hex)
    else:
        ModernTwoColumnTemplate.create_pdf(resume_data, user_info, output_filename, accent_color=color_hex)


# Template registry
TEMPLATES = {
    'modern': ModernTwoColumnTemplate,
    'visual': VisualBlockTemplate,
}


def get_template(template_name='modern'):
    """Get template"""
    return TEMPLATES.get(template_name, ModernTwoColumnTemplate)