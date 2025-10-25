"""
UNIQUE Professional Resume Templates
Actual design elements - not just colored rectangles!
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate


class SidebarAccentTemplate:
    """Modern template with colored sidebar and geometric accents"""
    
    @staticmethod
    def create_pdf(resume_data, user_info, output_filename, accent_color='#4A90E2', font_family='helvetica'):
        """Resume with left sidebar accent and modern design"""
        
        # Map font names to ReportLab fonts
        FONT_MAP = {
            'helvetica': ('Helvetica', 'Helvetica-Bold'),
            'times': ('Times-Roman', 'Times-Bold'),
            'courier': ('Courier', 'Courier-Bold'),
        }
        
        base_font, bold_font = FONT_MAP.get(font_family, FONT_MAP['helvetica'])
        
        class SidebarCanvas(canvas.Canvas):
            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []
                
            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()
                
            def save(self):
                # Draw sidebar on all pages
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_sidebar()
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)
                
            def draw_sidebar(self):
                # Left accent bar (1.5 inch wide)
                self.setFillColor(colors.HexColor(accent_color))
                self.rect(0, 0, 1.5*inch, 11*inch, fill=1, stroke=0)
                
                # Diagonal accent stripe
                self.setFillColor(colors.HexColor('#ffffff'))
                self.setFillAlpha(0.1)
                self.saveState()
                self.translate(0.75*inch, 5.5*inch)
                self.rotate(45)
                self.rect(-2*inch, -0.5*inch, 4*inch, 1*inch, fill=1, stroke=0)
                self.restoreState()
        
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=1.8*inch,  # Make room for sidebar
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        elements = []
        
        # Styles
        name_style = ParagraphStyle(
            'Name',
            fontSize=38,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            fontName=bold_font,
            alignment=TA_LEFT,
            leading=42
        )
        
        contact_style = ParagraphStyle(
            'Contact',
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            spaceAfter=20,
            alignment=TA_LEFT
        )
        
        section_style = ParagraphStyle(
            'Section',
            fontSize=14,
            textColor=colors.HexColor(accent_color),
            fontName=bold_font,
            spaceAfter=8,
            spaceBefore=14,
            borderWidth=0,
            leftIndent=0
        )
        
        body_style = ParagraphStyle(
            'Body',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#333333'),
            alignment=TA_JUSTIFY
        )
        
        # NAME - Left aligned, bold
        elements.append(Paragraph(user_info.get('name', 'Your Name').upper(), name_style))
        
        # Contact info
        contact_parts = []
        if user_info.get('email'):
            contact_parts.append(f"✉ {user_info['email']}")
        if user_info.get('phone'):
            contact_parts.append(f"☎ {user_info['phone']}")
        if user_info.get('location'):
            contact_parts.append(f"📍 {user_info['location']}")
        
        elements.append(Paragraph(' • '.join(contact_parts), contact_style))
        
        # Sections with geometric dividers
        if resume_data.get('summary'):
            # Circle bullet + section title
            elements.append(Paragraph('● PROFESSIONAL PROFILE', section_style))
            
            # Short line under header
            line = Table([['']], colWidths=[2*inch])
            line.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor(accent_color)),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(line)
            
            elements.append(Paragraph(resume_data['summary'], body_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Skills with visual boxes
        if resume_data.get('skills'):
            elements.append(Paragraph('● EXPERTISE', section_style))
            
            line = Table([['']], colWidths=[2*inch])
            line.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor(accent_color)),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(line)
            
            # Skills in rounded boxes
            skill_style = ParagraphStyle('Skill', fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor('#333333'))
            skill_rows = []
            for i in range(0, len(resume_data['skills']), 3):
                row_skills = resume_data['skills'][i:i+3]
                while len(row_skills) < 3:
                    row_skills.append('')
                skill_rows.append([Paragraph(s, skill_style) if s else '' for s in row_skills])
            
            skill_table = Table(skill_rows, colWidths=[2*inch, 2*inch, 2*inch])
            skill_table.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor(accent_color)),
                ('INNERGRID', (0,0), (-1,-1), 1.5, colors.HexColor(accent_color)),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
                ('ROUNDEDCORNERS', [5, 5, 5, 5]),
            ]))
            elements.append(skill_table)
            elements.append(Spacer(1, 0.15*inch))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('● PROFESSIONAL EXPERIENCE', section_style))
            
            line = Table([['']], colWidths=[2*inch])
            line.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor(accent_color)),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(line)
            
            for exp in resume_data['experience']:
                # Job title with accent
                title_style = ParagraphStyle('Title', fontSize=11, fontName=bold_font, textColor=colors.HexColor('#1a1a1a'))
                meta_style = ParagraphStyle('Meta', fontSize=9.5, textColor=colors.HexColor('#666666'))
                
                elements.append(Paragraph(f"▸ {exp.get('title', '')}", title_style))
                elements.append(Paragraph(f"{exp.get('company', '')} | {exp.get('period', '')}", meta_style))
                elements.append(Spacer(1, 0.05*inch))
                
                for achievement in exp.get('achievements', []):
                    bullet_style = ParagraphStyle('Bullet', fontSize=10, leading=14, leftIndent=15, firstLineIndent=-10)
                    elements.append(Paragraph(f'• {achievement}', bullet_style))
                
                elements.append(Spacer(1, 0.12*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('● EDUCATION', section_style))
            
            line = Table([['']], colWidths=[2*inch])
            line.setStyle(TableStyle([
                ('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor(accent_color)),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ]))
            elements.append(line)
            
            for edu in resume_data['education']:
                edu_style = ParagraphStyle('Edu', fontSize=10, textColor=colors.HexColor('#333333'))
                edu_text = f"<b>{edu.get('degree', '')}</b> — {edu.get('institution', '')} ({edu.get('year', '')})"
                elements.append(Paragraph(edu_text, edu_style))
                elements.append(Spacer(1, 0.06*inch))
        
        # Build with custom canvas
        doc.build(elements, canvasmaker=SidebarCanvas)


class DiagonalHeaderTemplate:
    """Modern template with diagonal header design and geometric elements"""
    
    @staticmethod
    def create_pdf(resume_data, user_info, output_filename, accent_color='#6366f1', font_family='helvetica'):
        """Resume with diagonal header and modern geometric design"""
        
        # Map font names to ReportLab fonts
        FONT_MAP = {
            'helvetica': ('Helvetica', 'Helvetica-Bold'),
            'times': ('Times-Roman', 'Times-Bold'),
            'courier': ('Courier', 'Courier-Bold'),
        }
        
        base_font, bold_font = FONT_MAP.get(font_family, FONT_MAP['helvetica'])
        
        class DiagonalCanvas(canvas.Canvas):
            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []
                
            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()
                
            def save(self):
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_header()
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)
                
            def draw_header(self):
                # Diagonal background shape at top
                self.setFillColor(colors.HexColor(accent_color))
                path = self.beginPath()
                path.moveTo(0, 11*inch)
                path.lineTo(8.5*inch, 11*inch)
                path.lineTo(8.5*inch, 9.5*inch)
                path.lineTo(0, 10*inch)
                path.close()
                self.drawPath(path, fill=1, stroke=0)
                
                # Accent circle in top right
                self.setFillColor(colors.white)
                self.setFillAlpha(0.2)
                self.circle(7.5*inch, 10.3*inch, 0.8*inch, fill=1, stroke=0)
        
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=0.6*inch,
            leftMargin=0.6*inch,
            topMargin=1.8*inch,  # Make room for diagonal header
            bottomMargin=0.5*inch
        )
        
        elements = []
        
        # Name in header area (will be drawn on diagonal)
        name_style = ParagraphStyle(
            'Name',
            fontSize=36,
            textColor=colors.white,
            fontName=bold_font,
            alignment=TA_LEFT
        )
        
        # We'll add name separately since it's in the header
        
        # Styles
        section_style = ParagraphStyle(
            'Section',
            fontSize=12,
            textColor=colors.HexColor(accent_color),
            fontName=bold_font,
            spaceAfter=6,
            spaceBefore=12,
            borderWidth=2,
            borderColor=colors.HexColor(accent_color),
            borderPadding=4,
            leftIndent=8
        )
        
        body_style = ParagraphStyle(
            'Body',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#333333')
        )
        
        # Contact info with icons
        contact_style = ParagraphStyle('Contact', fontSize=10, textColor=colors.HexColor('#555555'), spaceAfter=16)
        contact_parts = []
        if user_info.get('email'):
            contact_parts.append(f"✉ {user_info['email']}")
        if user_info.get('phone'):
            contact_parts.append(f"☎ {user_info['phone']}")
        if user_info.get('location'):
            contact_parts.append(f"📍 {user_info['location']}")
        
        elements.append(Paragraph(' │ '.join(contact_parts), contact_style))
        
        # Summary
        if resume_data.get('summary'):
            elements.append(Paragraph('PROFESSIONAL SUMMARY', section_style))
            elements.append(Paragraph(resume_data['summary'], body_style))
            elements.append(Spacer(1, 0.12*inch))
        
        # Skills in pill-shaped boxes
        if resume_data.get('skills'):
            elements.append(Paragraph('TECHNICAL SKILLS', section_style))
            
            skill_text = ' • '.join([f'<b>{skill}</b>' for skill in resume_data['skills']])
            skill_style = ParagraphStyle('Skills', fontSize=10, textColor=colors.HexColor('#333333'), leading=16)
            elements.append(Paragraph(skill_text, skill_style))
            elements.append(Spacer(1, 0.12*inch))
        
        # Experience with side indicators
        if resume_data.get('experience'):
            elements.append(Paragraph('EXPERIENCE', section_style))
            
            for exp in resume_data['experience']:
                # Create box with left accent
                exp_content = []
                
                title_style = ParagraphStyle('Title', fontSize=11, fontName=bold_font, textColor=colors.HexColor('#1a1a1a'))
                meta_style = ParagraphStyle('Meta', fontSize=9.5, textColor=colors.HexColor('#666666'))
                
                exp_content.append(Paragraph(exp.get('title', ''), title_style))
                exp_content.append(Paragraph(f"{exp.get('company', '')} • {exp.get('period', '')}", meta_style))
                exp_content.append(Spacer(1, 0.05*inch))
                
                for achievement in exp.get('achievements', []):
                    exp_content.append(Paragraph(f'→ {achievement}', body_style))
                
                # Box with left colored border
                exp_table = Table([[exp_content]], colWidths=[7*inch])
                exp_table.setStyle(TableStyle([
                    ('LINEBEFORE', (0,0), (0,-1), 4, colors.HexColor(accent_color)),
                    ('LEFTPADDING', (0,0), (-1,-1), 12),
                    ('RIGHTPADDING', (0,0), (-1,-1), 8),
                    ('TOPPADDING', (0,0), (-1,-1), 8),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
                ]))
                elements.append(exp_table)
                elements.append(Spacer(1, 0.1*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('EDUCATION', section_style))
            
            for edu in resume_data['education']:
                edu_style = ParagraphStyle('Edu', fontSize=10, textColor=colors.HexColor('#333333'))
                edu_text = f"<b>{edu.get('degree', '')}</b> | {edu.get('institution', '')} | {edu.get('year', '')}"
                elements.append(Paragraph(edu_text, edu_style))
                elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements, canvasmaker=DiagonalCanvas)


class CircleAccentTemplate:
    """Modern template with circular elements and unique design"""
    
    @staticmethod
    def create_pdf(resume_data, user_info, output_filename, accent_color='#14b8a6', font_family='helvetica'):
        """Resume with circular design elements"""
        
        # Map font names to ReportLab fonts
        FONT_MAP = {
            'helvetica': ('Helvetica', 'Helvetica-Bold'),
            'times': ('Times-Roman', 'Times-Bold'),
            'courier': ('Courier', 'Courier-Bold'),
        }
        
        base_font, bold_font = FONT_MAP.get(font_family, FONT_MAP['helvetica'])
        
        class CircleCanvas(canvas.Canvas):
            def __init__(self, *args, **kwargs):
                canvas.Canvas.__init__(self, *args, **kwargs)
                self.pages = []
                
            def showPage(self):
                self.pages.append(dict(self.__dict__))
                self._startPage()
                
            def save(self):
                for page in self.pages:
                    self.__dict__.update(page)
                    self.draw_circles()
                    canvas.Canvas.showPage(self)
                canvas.Canvas.save(self)
                
            def draw_circles(self):
                # Large circle in top left (partially off page)
                self.setFillColor(colors.HexColor(accent_color))
                self.setFillAlpha(0.1)
                self.circle(0.5*inch, 10.5*inch, 1.2*inch, fill=1, stroke=0)
                
                # Medium circle in bottom right
                self.circle(7.8*inch, 0.8*inch, 0.8*inch, fill=1, stroke=0)
                
                # Small accent circles
                self.setFillAlpha(0.15)
                self.circle(1*inch, 5*inch, 0.4*inch, fill=1, stroke=0)
                self.circle(7.2*inch, 7*inch, 0.5*inch, fill=1, stroke=0)
        
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            rightMargin=0.7*inch,
            leftMargin=0.7*inch,
            topMargin=0.6*inch,
            bottomMargin=0.6*inch
        )
        
        elements = []
        
        # Name with circle bullet
        name_style = ParagraphStyle(
            'Name',
            fontSize=40,
            textColor=colors.HexColor('#1a1a1a'),
            fontName=bold_font,
            alignment=TA_CENTER,
            spaceAfter=8
        )
        
        elements.append(Paragraph(user_info.get('name', 'Your Name').upper(), name_style))
        
        # Contact with circle separators
        contact_style = ParagraphStyle('Contact', fontSize=10, textColor=colors.HexColor('#555555'), alignment=TA_CENTER, spaceAfter=20)
        contact_parts = []
        if user_info.get('email'):
            contact_parts.append(user_info['email'])
        if user_info.get('phone'):
            contact_parts.append(user_info['phone'])
        if user_info.get('location'):
            contact_parts.append(user_info['location'])
        
        elements.append(Paragraph(' ● '.join(contact_parts), contact_style))
        
        # Section with circle bullet
        section_style = ParagraphStyle(
            'Section',
            fontSize=13,
            textColor=colors.HexColor(accent_color),
            fontName=bold_font,
            spaceAfter=8,
            spaceBefore=14,
            alignment=TA_CENTER
        )
        
        body_style = ParagraphStyle('Body', fontSize=10, leading=14, textColor=colors.HexColor('#333333'))
        
        # Summary with decorative border
        if resume_data.get('summary'):
            elements.append(Paragraph('◉ PROFESSIONAL PROFILE ◉', section_style))
            
            summary_table = Table([[Paragraph(resume_data['summary'], body_style)]], colWidths=[6.5*inch])
            summary_table.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 2, colors.HexColor(accent_color)),
                ('TOPPADDING', (0,0), (-1,-1), 12),
                ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                ('LEFTPADDING', (0,0), (-1,-1), 15),
                ('RIGHTPADDING', (0,0), (-1,-1), 15),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.15*inch))
        
        # Skills in circular tags
        if resume_data.get('skills'):
            elements.append(Paragraph('◉ EXPERTISE ◉', section_style))
            
            skill_style = ParagraphStyle('Skill', fontSize=9, alignment=TA_CENTER, textColor=colors.white)
            skill_rows = []
            for i in range(0, len(resume_data['skills']), 4):
                row_skills = resume_data['skills'][i:i+4]
                while len(row_skills) < 4:
                    row_skills.append('')
                skill_rows.append([Paragraph(s, skill_style) if s else '' for s in row_skills])
            
            skill_table = Table(skill_rows, colWidths=[1.625*inch]*4)
            skill_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(accent_color)),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('ROUNDEDCORNERS', [15, 15, 15, 15]),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            elements.append(skill_table)
            elements.append(Spacer(1, 0.15*inch))
        
        # Experience
        if resume_data.get('experience'):
            elements.append(Paragraph('◉ EXPERIENCE ◉', section_style))
            
            for exp in resume_data['experience']:
                title_style = ParagraphStyle('Title', fontSize=11, fontName=bold_font, textColor=colors.HexColor(accent_color))
                meta_style = ParagraphStyle('Meta', fontSize=9.5, textColor=colors.HexColor('#666666'))
                
                elements.append(Paragraph(f"◆ {exp.get('title', '')}", title_style))
                elements.append(Paragraph(f"{exp.get('company', '')} | {exp.get('period', '')}", meta_style))
                elements.append(Spacer(1, 0.05*inch))
                
                for achievement in exp.get('achievements', []):
                    elements.append(Paragraph(f'• {achievement}', body_style))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Education
        if resume_data.get('education'):
            elements.append(Paragraph('◉ EDUCATION ◉', section_style))
            
            for edu in resume_data['education']:
                edu_style = ParagraphStyle('Edu', fontSize=10, textColor=colors.HexColor('#333333'), alignment=TA_CENTER)
                edu_text = f"<b>{edu.get('degree', '')}</b> • {edu.get('institution', '')} • {edu.get('year', '')}"
                elements.append(Paragraph(edu_text, edu_style))
                elements.append(Spacer(1, 0.05*inch))
        
        doc.build(elements, canvasmaker=CircleCanvas)


# Color schemes - 16 vibrant options!
ACCENT_COLORS = {
    'blue': '#4A90E2',
    'indigo': '#6366f1',
    'purple': '#9333ea',
    'violet': '#8b5cf6',
    'teal': '#14b8a6',
    'emerald': '#10b981',
    'green': '#22c55e',
    'lime': '#84cc16',
    'rose': '#f43f5e',
    'pink': '#ec4899',
    'red': '#ef4444',
    'orange': '#f97316',
    'amber': '#f59e0b',
    'yellow': '#eab308',
    'cyan': '#06b6d4',
    'sky': '#0ea5e9',
}


def create_unique_resume(resume_data, user_info, output_filename, template='sidebar', color='blue', font='helvetica'):
    """Create resume with unique design"""
    color_hex = ACCENT_COLORS.get(color, ACCENT_COLORS['blue'])
    
    # Pass font to template
    if template == 'sidebar':
        SidebarAccentTemplate.create_pdf(resume_data, user_info, output_filename, accent_color=color_hex, font_family=font)
    elif template == 'diagonal':
        DiagonalHeaderTemplate.create_pdf(resume_data, user_info, output_filename, accent_color=color_hex, font_family=font)
    elif template == 'circle':
        CircleAccentTemplate.create_pdf(resume_data, user_info, output_filename, accent_color=color_hex, font_family=font)
    else:
        SidebarAccentTemplate.create_pdf(resume_data, user_info, output_filename, accent_color=color_hex, font_family=font)


TEMPLATES = {
    'sidebar': SidebarAccentTemplate,
    'diagonal': DiagonalHeaderTemplate,
    'circle': CircleAccentTemplate,
}