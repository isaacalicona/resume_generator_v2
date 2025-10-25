from flask import Flask, render_template, request, send_file, send_from_directory, flash, redirect, url_for, session
from resume_generator import ResumeGenerator
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this to a random string

# Configure upload folder
UPLOAD_FOLDER = 'generated_resumes'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """Home page with the form."""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_resume():
    """Handle form submission and generate resume."""
    try:
        # Get form data
        job_description = request.form.get('job_description')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        location = request.form.get('location')
        background = request.form.get('background')
        skills = request.form.get('skills')
        experience = request.form.get('experience')
        education = request.form.get('education')
        api_key = request.form.get('api_key') or os.getenv('OPENAI_API_KEY')
        template = request.form.get('template', 'sidebar_accent')
        color_scheme = request.form.get('color_scheme', 'blue')
        font_family = request.form.get('font_family', 'helvetica')  # NEW: Font selection
        
        # Validate inputs
        if not job_description or not name or not api_key:
            flash('Please fill in all required fields (Job Description, Name, and API Key)', 'error')
            return redirect(url_for('index'))
        
        # Prepare user info
        user_info = {
            'name': name,
            'email': email,
            'phone': phone,
            'location': location,
            'background': background,
            'skills': skills,
            'experience': experience,
            'education': education
        }
        
        # Initialize generator
        generator = ResumeGenerator(api_key=api_key)
        
        # Generate resume content
        resume_data = generator.generate_resume_content(job_description, user_info)
        
        # Create PDF with timestamp in filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"resume_{name.replace(' ', '_')}_{timestamp}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Generate with unique design templates
        from resume_templates_unique import create_unique_resume
        color = color_scheme if color_scheme else 'blue'
        
        # Map template names to types
        if template == 'sidebar_accent':
            template_type = 'sidebar'
        elif template == 'diagonal_header':
            template_type = 'diagonal'
        elif template == 'circle_accent':
            template_type = 'circle'
        else:
            template_type = 'sidebar'  # Default
        
        create_unique_resume(resume_data, user_info, filepath, template=template_type, color=color, font=font_family)
        
        # Store data in session for editor
        session['resume_data'] = resume_data
        session['user_info'] = user_info
        session['template'] = template
        session['color_scheme'] = color_scheme
        session['font_family'] = font_family
        session['api_key'] = api_key
        session['filename'] = filename
        
        # Redirect to editor page
        return redirect(url_for('edit_resume', filename=filename))
        
    except Exception as e:
        flash(f'Error generating resume: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    """Download the generated resume."""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except:
        flash('File not found', 'error')
        return redirect(url_for('index'))


@app.route('/edit/<filename>')
def edit_resume(filename):
    """Show editor page with current resume data."""
    resume_data = session.get('resume_data', {})
    user_info = session.get('user_info', {})
    template = session.get('template', 'sidebar_accent')
    color_scheme = session.get('color_scheme', 'blue')
    font_family = session.get('font_family', 'helvetica')
    api_key = session.get('api_key', '')
    
    return render_template('edit.html', 
                         filename=filename,
                         resume_data=resume_data,
                         user_info=user_info,
                         template=template,
                         color_scheme=color_scheme,
                         font_family=font_family,
                         api_key=api_key)


@app.route('/regenerate', methods=['POST'])
def regenerate_resume():
    """Regenerate resume with manual edits."""
    try:
        # Get form data
        template = request.form.get('template')
        color_scheme = request.form.get('color_scheme')
        font_family = request.form.get('font_family')
        api_key = request.form.get('api_key')
        
        # User info
        user_info = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'location': request.form.get('location')
        }
        
        # Resume data
        resume_data = {
            'summary': request.form.get('summary'),
            'skills': [s.strip() for s in request.form.get('skills', '').split(',') if s.strip()],
            'experience': [],
            'education': []
        }
        
        # Parse experience
        exp_index = 0
        while f'exp_title_{exp_index}' in request.form:
            achievements_text = request.form.get(f'exp_achievements_{exp_index}', '')
            achievements = [a.strip() for a in achievements_text.split('\n') if a.strip()]
            
            resume_data['experience'].append({
                'title': request.form.get(f'exp_title_{exp_index}'),
                'company': request.form.get(f'exp_company_{exp_index}'),
                'period': request.form.get(f'exp_period_{exp_index}'),
                'achievements': achievements
            })
            exp_index += 1
        
        # Parse education
        edu_index = 0
        while f'edu_degree_{edu_index}' in request.form:
            resume_data['education'].append({
                'degree': request.form.get(f'edu_degree_{edu_index}'),
                'institution': request.form.get(f'edu_institution_{edu_index}'),
                'year': request.form.get(f'edu_year_{edu_index}')
            })
            edu_index += 1
        
        # Generate new PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"resume_{user_info['name'].replace(' ', '_')}_{timestamp}.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        from resume_templates_unique import create_unique_resume
        
        # Map template names
        if template == 'sidebar_accent':
            template_type = 'sidebar'
        elif template == 'diagonal_header':
            template_type = 'diagonal'
        elif template == 'circle_accent':
            template_type = 'circle'
        else:
            template_type = 'sidebar'
        
        create_unique_resume(resume_data, user_info, filepath, template=template_type, color=color_scheme, font=font_family)
        
        # Update session
        session['resume_data'] = resume_data
        session['user_info'] = user_info
        session['filename'] = filename
        
        flash('Resume regenerated successfully!', 'success')
        return redirect(url_for('edit_resume', filename=filename))
        
    except Exception as e:
        flash(f'Error regenerating resume: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/preview/<filename>')
def preview_resume(filename):
    """Serve PDF for preview in iframe."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # Run the app
    print("\n" + "="*50)
    print("🚀 AI Resume Generator Web App")
    print("="*50)
    print("📍 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)