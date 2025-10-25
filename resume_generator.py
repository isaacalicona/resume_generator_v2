import os
import json
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Try to load .env file if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use system environment variables


class ResumeGenerator:
    def __init__(self, api_key=None):
        """Initialize the Resume Generator with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it directly.")
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_resume_content(self, job_description, user_info):
        """
        Generate tailored resume content using GPT based on job description.
        
        Args:
            job_description (str): The job posting or description
            user_info (dict): Dictionary containing user's background information
        
        Returns:
            dict: Structured resume content
        """
        prompt = f"""You are a professional resume writer. Create a tailored resume based on the following:

JOB DESCRIPTION:
{job_description}

CANDIDATE INFORMATION:
Name: {user_info.get('name', 'John Doe')}
Email: {user_info.get('email', 'email@example.com')}
Phone: {user_info.get('phone', '(555) 123-4567')}
Location: {user_info.get('location', 'City, State')}

Background: {user_info.get('background', 'Please provide your professional background')}
Skills: {user_info.get('skills', 'Please list your skills')}
Experience: {user_info.get('experience', 'Please describe your work experience')}
Education: {user_info.get('education', 'Please describe your education')}

INSTRUCTIONS:
1. Create a professional summary that highlights relevant skills for this specific job
2. List key skills that match the job requirements
3. Tailor the work experience descriptions to emphasize relevant achievements
4. Format education appropriately
5. Keep it concise and ATS-friendly

Return the resume in the following JSON structure:
{{
    "summary": "Professional summary paragraph",
    "skills": ["skill1", "skill2", "skill3"],
    "experience": [
        {{
            "title": "Job Title",
            "company": "Company Name",
            "period": "Start Date - End Date",
            "achievements": ["achievement1", "achievement2"]
        }}
    ],
    "education": [
        {{
            "degree": "Degree Name",
            "institution": "School Name",
            "year": "Graduation Year"
        }}
    ]
}}

Provide ONLY the JSON output, no additional text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Changed from gpt-4 - 15x cheaper!
                messages=[
                    {"role": "system", "content": "You are a professional resume writer who outputs structured JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON from the response
            # Sometimes GPT wraps JSON in code blocks
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
            
            resume_data = json.loads(content)
            return resume_data
            
        except Exception as e:
            print(f"Error generating resume content: {e}")
            raise
    
    def create_pdf(self, resume_data, user_info, output_filename="resume.pdf", template='sidebar_accent'):
        """
        Create a professional PDF resume from the generated content.
        
        Args:
            resume_data (dict): Structured resume content from GPT
            user_info (dict): User's contact information
            output_filename (str): Name of the output PDF file
            template (str): Template style - 'sidebar_accent', 'diagonal_header', or 'circle_accent'
        """
        from resume_templates_unique import create_unique_resume
        
        # Map template names to actual template types
        if template == 'sidebar_accent':
            template_type = 'sidebar'
        elif template == 'diagonal_header':
            template_type = 'diagonal'
        elif template == 'circle_accent':
            template_type = 'circle'
        else:
            template_type = 'sidebar'
        
        color = 'blue'  # Default color
        
        create_unique_resume(resume_data, user_info, output_filename, template=template_type, color=color)
        print(f"✓ Resume PDF created with '{template}' template: {output_filename}")
        return  # Exit early since template handles PDF creation
        
        doc = SimpleDocTemplate(output_filename, pagesize=letter,
                               rightMargin=0.75*inch, leftMargin=0.75*inch,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#2C3E50',
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        contact_style = ParagraphStyle(
            'Contact',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='#2C3E50',
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor='#2C3E50',
            borderPadding=3
        )
        
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.leading = 14
        
        # Add name
        elements.append(Paragraph(user_info.get('name', 'Your Name'), title_style))
        
        # Add contact info
        contact_info = f"{user_info.get('email', '')} | {user_info.get('phone', '')} | {user_info.get('location', '')}"
        elements.append(Paragraph(contact_info, contact_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Add Professional Summary
        elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        elements.append(Spacer(1, 0.05*inch))
        elements.append(Paragraph(resume_data.get('summary', ''), normal_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # Add Skills
        if resume_data.get('skills'):
            elements.append(Paragraph("SKILLS", heading_style))
            elements.append(Spacer(1, 0.05*inch))
            skills_text = " • ".join(resume_data['skills'])
            elements.append(Paragraph(skills_text, normal_style))
            elements.append(Spacer(1, 0.15*inch))
        
        # Add Experience
        if resume_data.get('experience'):
            elements.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
            elements.append(Spacer(1, 0.05*inch))
            
            for exp in resume_data['experience']:
                # Job title and company
                job_title = f"<b>{exp.get('title', '')}</b> | {exp.get('company', '')}"
                elements.append(Paragraph(job_title, normal_style))
                
                # Period
                elements.append(Paragraph(f"<i>{exp.get('period', '')}</i>", normal_style))
                elements.append(Spacer(1, 0.05*inch))
                
                # Achievements
                for achievement in exp.get('achievements', []):
                    elements.append(Paragraph(f"• {achievement}", normal_style))
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Add Education
        if resume_data.get('education'):
            elements.append(Paragraph("EDUCATION", heading_style))
            elements.append(Spacer(1, 0.05*inch))
            
            for edu in resume_data['education']:
                degree_text = f"<b>{edu.get('degree', '')}</b>"
                elements.append(Paragraph(degree_text, normal_style))
                
                institution_text = f"{edu.get('institution', '')} | {edu.get('year', '')}"
                elements.append(Paragraph(institution_text, normal_style))
                elements.append(Spacer(1, 0.05*inch))
        
        # Build PDF
        doc.build(elements)
        print(f"✓ Resume PDF created: {output_filename}")


def main():
    """Main function to demonstrate usage."""
    print("=== AI Resume Generator ===\n")
    
    # Get API key
    api_key = input("Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY env variable): ").strip()
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Error: No API key provided. Please set OPENAI_API_KEY environment variable or enter it when prompted.")
        return
    
    # Initialize generator
    generator = ResumeGenerator(api_key=api_key)
    
    # Get job description
    print("\nPaste the job description (press Ctrl+D or Ctrl+Z when done):")
    job_description_lines = []
    try:
        while True:
            line = input()
            job_description_lines.append(line)
    except EOFError:
        pass
    
    job_description = "\n".join(job_description_lines)
    
    if not job_description.strip():
        print("Error: No job description provided.")
        return
    
    # Get user information
    print("\n--- Your Information ---")
    user_info = {
        'name': input("Full Name: "),
        'email': input("Email: "),
        'phone': input("Phone: "),
        'location': input("Location (City, State): "),
        'background': input("Brief background (1-2 sentences): "),
        'skills': input("Your skills (comma-separated): "),
        'experience': input("Brief work experience summary: "),
        'education': input("Education summary: ")
    }
    
    # Generate resume
    print("\n🤖 Generating tailored resume content...")
    resume_data = generator.generate_resume_content(job_description, user_info)
    
    # Create PDF
    output_file = "tailored_resume.pdf"
    print(f"\n📄 Creating PDF: {output_file}")
    generator.create_pdf(resume_data, user_info, output_file)
    
    print(f"\n✅ Success! Your resume has been saved as '{output_file}'")
    print("\nTip: Review and customize the resume before sending to ensure accuracy!")


if __name__ == "__main__":
    main()