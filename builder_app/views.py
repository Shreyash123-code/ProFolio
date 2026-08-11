import io
import json
import re
import zipfile
import urllib.request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from .models import Portfolio, Project, Education, Experience, Certificate, TEMPLATE_CHOICES


def redirect_with_tab(tab_name):
    """Redirect to index with specified tab active."""
    from django.urls import reverse
    return redirect(reverse('index') + f'?tab={tab_name}')


@login_required(login_url='/users/login/')
def index(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    projects = portfolio.projects.all()
    educations = portfolio.educations.all()
    experiences = portfolio.experiences.all()
    certificates = portfolio.certificates.all()

    if request.method == 'POST':
        # Helper: return new value if provided, else keep existing
        def post_val(key, current, allow_blank=False):
            val = request.POST.get(key, None)
            if val is None:           # key not in POST at all
                return current
            val = val.strip()
            if val == '' and not allow_blank:
                return current        # keep existing if empty submitted
            return val or None        # store None for blank URL fields

        # Parse portfolio basic info and customization fields
        portfolio.title = request.POST.get('title', portfolio.title) or portfolio.title
        portfolio.professional_title = post_val('professional_title', portfolio.professional_title, allow_blank=True)
        portfolio.tagline = post_val('tagline', portfolio.tagline, allow_blank=True)
        portfolio.bio = post_val('bio', portfolio.bio, allow_blank=True)
        portfolio.skills = post_val('skills', portfolio.skills, allow_blank=True)
        portfolio.email = post_val('email', portfolio.email, allow_blank=True)
        portfolio.phone = post_val('phone', portfolio.phone, allow_blank=True)
        portfolio.location = post_val('location', portfolio.location, allow_blank=True)

        # URL fields — store None for blanks to avoid URLField issues
        portfolio.github_link = post_val('github_link', portfolio.github_link)
        portfolio.linkedin_link = post_val('linkedin_link', portfolio.linkedin_link)
        portfolio.twitter_link = post_val('twitter_link', portfolio.twitter_link)
        portfolio.instagram_link = post_val('instagram_link', portfolio.instagram_link)
        portfolio.website_link = post_val('website_link', portfolio.website_link)

        portfolio.theme = request.POST.get('theme', portfolio.theme) or portfolio.theme
        portfolio.template = request.POST.get('template', portfolio.template) or portfolio.template
        portfolio.accent_color = request.POST.get('accent_color', portfolio.accent_color) or portfolio.accent_color
        portfolio.font_family = request.POST.get('font_family', portfolio.font_family) or portfolio.font_family
        portfolio.animation_style = request.POST.get('animation_style', portfolio.animation_style) or portfolio.animation_style
        portfolio.layout_style = request.POST.get('layout_style', portfolio.layout_style) or portfolio.layout_style
        portfolio.section_order = request.POST.get('section_order', portfolio.section_order) or portfolio.section_order

        if 'profile_image' in request.FILES:
            portfolio.profile_image = request.FILES['profile_image']

        portfolio.save()
        messages.success(request, 'Portfolio updated successfully!')
        tab = request.POST.get('active_tab', 'content')
        return redirect(f"/?tab={tab}")

    return render(request, 'builder_app/index.html', {
        'portfolio': portfolio,
        'projects': projects,
        'educations': educations,
        'experiences': experiences,
        'certificates': certificates,
        'template_choices': TEMPLATE_CHOICES,
    })


# ══════════════════════════════════════════════════════════════════════════════
# PROJECTS CRUD
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
def add_project(request):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        project = Project(portfolio=portfolio)
        project.title = request.POST.get('project_title', '').strip()
        project.description = request.POST.get('project_description', '').strip()
        project.link = request.POST.get('project_link', '').strip()
        project.github_link = request.POST.get('project_github_link', '').strip()
        project.demo_link = request.POST.get('project_demo_link', '').strip()
        project.technology_tags = request.POST.get('project_tags', '').strip()
        project.is_featured = request.POST.get('is_featured') == 'on' or request.POST.get('is_featured') == 'true'

        if 'project_image' in request.FILES:
            project.image = request.FILES['project_image']

        if project.title:
            project.save()
            messages.success(request, f'Project "{project.title}" added successfully!')
        else:
            messages.error(request, 'Project title is required.')
    return redirect_with_tab('projects')


@login_required(login_url='/users/login/')
def edit_project(request, project_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        project = get_object_or_404(Project, id=project_id, portfolio=portfolio)
        title = request.POST.get('project_title', '').strip()
        if title:
            project.title = title
        project.description = request.POST.get('project_description', '').strip()
        project.link = request.POST.get('project_link', '').strip()
        project.github_link = request.POST.get('project_github_link', '').strip()
        project.demo_link = request.POST.get('project_demo_link', '').strip()
        project.technology_tags = request.POST.get('project_tags', '').strip()
        project.is_featured = request.POST.get('is_featured') == 'on' or request.POST.get('is_featured') == 'true'

        if 'project_image' in request.FILES:
            project.image = request.FILES['project_image']

        project.save()
        messages.success(request, f'Project "{project.title}" updated successfully!')
    return redirect_with_tab('projects')


@login_required(login_url='/users/login/')
def delete_project(request, project_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        project = get_object_or_404(Project, id=project_id, portfolio=portfolio)
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted successfully.')
    return redirect_with_tab('projects')


# ══════════════════════════════════════════════════════════════════════════════
# EDUCATION CRUD
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
def add_education(request):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        degree = request.POST.get('degree', '').strip()
        college = request.POST.get('college', '').strip()
        year = request.POST.get('year', '').strip()
        cgpa = request.POST.get('cgpa', '').strip()

        if degree and college:
            Education.objects.create(
                portfolio=portfolio,
                degree=degree,
                college=college,
                year=year,
                cgpa=cgpa
            )
            messages.success(request, f'Education "{degree}" added!')
        else:
            messages.error(request, 'Degree and College are required.')
    return redirect_with_tab('content')


@login_required(login_url='/users/login/')
def edit_education(request, edu_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        edu = get_object_or_404(Education, id=edu_id, portfolio=portfolio)
        edu.degree = request.POST.get('degree', edu.degree).strip()
        edu.college = request.POST.get('college', edu.college).strip()
        edu.year = request.POST.get('year', edu.year).strip()
        edu.cgpa = request.POST.get('cgpa', edu.cgpa).strip()
        edu.save()
        messages.success(request, 'Education entry updated!')
    return redirect_with_tab('content')


@login_required(login_url='/users/login/')
def delete_education(request, edu_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        edu = get_object_or_404(Education, id=edu_id, portfolio=portfolio)
        edu.delete()
        messages.success(request, 'Education entry removed.')
    return redirect_with_tab('content')


# ══════════════════════════════════════════════════════════════════════════════
# EXPERIENCE CRUD
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
def add_experience(request):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        company = request.POST.get('company', '').strip()
        role = request.POST.get('role', '').strip()
        duration = request.POST.get('duration', '').strip()
        description = request.POST.get('description', '').strip()

        if company and role:
            Experience.objects.create(
                portfolio=portfolio,
                company=company,
                role=role,
                duration=duration,
                description=description
            )
            messages.success(request, f'Experience at "{company}" added!')
        else:
            messages.error(request, 'Company and Role are required.')
    return redirect_with_tab('content')


@login_required(login_url='/users/login/')
def edit_experience(request, exp_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        exp = get_object_or_404(Experience, id=exp_id, portfolio=portfolio)
        exp.company = request.POST.get('company', exp.company).strip()
        exp.role = request.POST.get('role', exp.role).strip()
        exp.duration = request.POST.get('duration', exp.duration).strip()
        exp.description = request.POST.get('description', exp.description).strip()
        exp.save()
        messages.success(request, 'Experience entry updated!')
    return redirect_with_tab('content')


@login_required(login_url='/users/login/')
def delete_experience(request, exp_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        exp = get_object_or_404(Experience, id=exp_id, portfolio=portfolio)
        exp.delete()
        messages.success(request, 'Experience entry removed.')
    return redirect_with_tab('content')


# ══════════════════════════════════════════════════════════════════════════════
# CERTIFICATE CRUD
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
def add_certificate(request):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        name = request.POST.get('name', '').strip()
        organization = request.POST.get('organization', '').strip()
        year = request.POST.get('year', '').strip()
        link = request.POST.get('link', '').strip()

        if name and organization:
            Certificate.objects.create(
                portfolio=portfolio,
                name=name,
                organization=organization,
                year=year,
                link=link
            )
            messages.success(request, f'Certificate "{name}" added!')
        else:
            messages.error(request, 'Certificate Name and Organization are required.')
    return redirect_with_tab('content')


@login_required(login_url='/users/login/')
def edit_certificate(request, cert_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        cert = get_object_or_404(Certificate, id=cert_id, portfolio=portfolio)
        cert.name = request.POST.get('name', cert.name).strip()
        cert.organization = request.POST.get('organization', cert.organization).strip()
        cert.year = request.POST.get('year', cert.year).strip()
        cert.link = request.POST.get('link', cert.link).strip()
        cert.save()
        messages.success(request, 'Certificate updated!')
    return redirect_with_tab('content')


@login_required(login_url='/users/login/')
def delete_certificate(request, cert_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        cert = get_object_or_404(Certificate, id=cert_id, portfolio=portfolio)
        cert.delete()
        messages.success(request, 'Certificate removed.')
    return redirect_with_tab('content')


# ══════════════════════════════════════════════════════════════════════════════
# AI CONTENT ASSISTANCE ENDPOINT
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
@require_POST
def generate_ai_content(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        prompt = data.get('prompt', '').strip()
        gen_type = data.get('type', 'project_desc')

        if not prompt:
            return JsonResponse({'status': 'error', 'message': 'Prompt is required.'}, status=400)

        # Smart NLP AI generation templates
        result_text = ""
        if gen_type == 'project_desc':
            result_text = f"Developed a high-performance application featuring {prompt}. Implemented clean architecture, robust user workflows, responsive interfaces, and optimized data processing to deliver a seamless user experience."
        elif gen_type == 'intro':
            result_text = f"Passionate {prompt} with a strong foundation in building scalable digital solutions. Dedicated to creating high-impact applications, solving complex problems, and writing clean, maintainable code."
        elif gen_type == 'about':
            result_text = f"I am a driven tech professional focusing on {prompt}. Over the course of my career and academic journey, I have specialized in building modern web systems, modern UI design, and data-driven solutions. I thrive in collaborative environments and love turning innovative ideas into real-world products."
        elif gen_type == 'resume_summary':
            result_text = f"Results-oriented tech specialist with expertise in {prompt}. Proven track record of developing full-stack applications, optimizing workflows, and integrating modern frameworks to drive performance and user engagement."
        elif gen_type == 'skills_suggestion':
            # Generate relevant skills list based on prompt
            base_skills = ["Python", "JavaScript", "React", "Django", "Node.js", "HTML5/CSS3", "REST APIs", "Git", "SQL", "Docker", "AWS", "Tailwind CSS", "TypeScript"]
            matching = [s for s in base_skills if s.lower() in prompt.lower()]
            if not matching:
                matching = ["Python", "JavaScript", "React", "Django", "REST APIs", "Git", "SQL"]
            result_text = ", ".join(matching)
        else:
            result_text = f"Enhanced content for: {prompt}"

        return JsonResponse({'status': 'success', 'result': result_text})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# ══════════════════════════════════════════════════════════════════════════════
# RESUME PDF IMPORT ENDPOINT
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
@require_POST
def import_resume(request):
    if 'resume_pdf' not in request.FILES:
        return JsonResponse({'status': 'error', 'message': 'No PDF file uploaded.'}, status=400)

    pdf_file = request.FILES['resume_pdf']
    if not pdf_file.name.endswith('.pdf'):
        return JsonResponse({'status': 'error', 'message': 'File must be a PDF.'}, status=400)

    text_content = ""
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content += extracted + "\n"
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'PDF Parsing Error: {str(e)}'}, status=500)

    if not text_content.strip():
        return JsonResponse({'status': 'error', 'message': 'Could not extract text from PDF. It might be scanned or empty.'}, status=400)

    # Heuristic parsing of resume text
    portfolio = get_object_or_404(Portfolio, user=request.user)

    # Email extraction
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text_content)
    if email_match:
        portfolio.email = email_match.group(0)

    # Phone extraction
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text_content)
    if phone_match:
        portfolio.phone = phone_match.group(0)

    # Name heuristic (usually first line)
    lines = [l.strip() for l in text_content.split('\n') if l.strip()]
    if lines:
        possible_name = lines[0]
        if len(possible_name) < 50 and not '@' in possible_name:
            portfolio.title = possible_name

    # Skills extraction from known tech dictionary
    tech_keywords = [
        "Python", "JavaScript", "TypeScript", "React", "Vue", "Angular", "Django", "Flask",
        "Node.js", "Express", "HTML", "CSS", "Tailwind", "Bootstrap", "Git", "Docker",
        "Kubernetes", "AWS", "Azure", "GCP", "SQL", "PostgreSQL", "MySQL", "MongoDB",
        "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "Flutter", "Machine Learning",
        "Deep Learning", "TensorFlow", "PyTorch", "Data Analysis", "Figma", "REST API"
    ]
    extracted_skills = set()
    for kw in tech_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text_content, re.IGNORECASE):
            extracted_skills.add(kw)

    if extracted_skills:
        existing_skills = set(portfolio.skills_list())
        combined_skills = existing_skills.union(extracted_skills)
        portfolio.skills = ", ".join(sorted(list(combined_skills)))

    portfolio.save()

    # Experience section extraction heuristic
    if 'Experience' in text_content or 'Work History' in text_content:
        # Heuristically check lines after Experience
        exp_lines = re.split(r'Experience|Work History', text_content, flags=re.IGNORECASE)
        if len(exp_lines) > 1:
            snippet = exp_lines[1][:400].strip()
            if snippet and not portfolio.experiences.exists():
                Experience.objects.create(
                    portfolio=portfolio,
                    company="Extracted Experience",
                    role="Software Specialist",
                    duration="Recent",
                    description=snippet[:300]
                )

    # Education extraction heuristic
    if 'Education' in text_content or 'Academic' in text_content:
        edu_lines = re.split(r'Education|Academic', text_content, flags=re.IGNORECASE)
        if len(edu_lines) > 1:
            snippet = edu_lines[1][:200].strip()
            if snippet and not portfolio.educations.exists():
                Education.objects.create(
                    portfolio=portfolio,
                    degree="Bachelor Degree",
                    college=snippet.split('\n')[0][:100] if snippet else "University",
                    year="2020 - 2024"
                )

    messages.success(request, 'Resume successfully imported! Portfolio fields auto-filled.')
    return JsonResponse({
        'status': 'success',
        'message': 'Resume imported successfully!',
        'extracted': {
            'name': portfolio.title,
            'email': portfolio.email,
            'phone': portfolio.phone,
            'skills': portfolio.skills
        }
    })


# ══════════════════════════════════════════════════════════════════════════════
# GITHUB AUTO-IMPORT REPOS ENDPOINT
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
@require_POST
def import_github_repos(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username', '').strip()

        portfolio = get_object_or_404(Portfolio, user=request.user)

        if not username and portfolio.github_link:
            # Extract username from github link
            parts = portfolio.github_link.rstrip('/').split('/')
            if parts:
                username = parts[-1]

        if not username:
            return JsonResponse({'status': 'error', 'message': 'GitHub username or link is required.'}, status=400)

        url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
        req = urllib.request.Request(url, headers={'User-Agent': 'ProFolio-App'})

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                repos = json.loads(response.read().decode('utf-8'))
                imported_count = 0
                for repo in repos:
                    if repo.get('fork'):
                        continue  # skip forks
                    name = repo.get('name', 'Project')
                    desc = repo.get('description') or 'GitHub Repository'
                    html_url = repo.get('html_url')
                    language = repo.get('language') or 'Code'
                    homepage = repo.get('homepage') or ''

                    # Avoid duplicate titles
                    if not Project.objects.filter(portfolio=portfolio, title=name).exists():
                        Project.objects.create(
                            portfolio=portfolio,
                            title=name,
                            description=desc,
                            link=html_url,
                            github_link=html_url,
                            demo_link=homepage,
                            technology_tags=language,
                            is_featured=imported_count < 3
                        )
                        imported_count += 1

                return JsonResponse({
                    'status': 'success',
                    'message': f'Successfully imported {imported_count} projects from GitHub!'
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to reach GitHub API.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# ══════════════════════════════════════════════════════════════════════════════
# EXPORT PORTFOLIO ZIP ENDPOINT
# ══════════════════════════════════════════════════════════════════════════════
@login_required(login_url='/users/login/')
def export_portfolio_zip(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    projects = portfolio.projects.all()
    educations = portfolio.educations.all()
    experiences = portfolio.experiences.all()
    certificates = portfolio.certificates.all()

    template_to_use = portfolio.template or 'minimal_developer'
    template_name = f'viewer/templates/{template_to_use}.html'

    # Render complete portfolio HTML
    html_content = render_to_string(template_name, {
        'portfolio': portfolio,
        'projects': projects,
        'educations': educations,
        'experiences': experiences,
        'certificates': certificates,
    })

    # Create ZIP archive in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('index.html', html_content)
        
        # README.md deployment guide inside zip
        readme = f"""# {portfolio.title} — Portfolio Website

Exported from ProFolio (https://profolio.me)

## How to Deploy:
1. **GitHub Pages**: Create a repository named `<username>.github.io` and upload `index.html`.
2. **Netlify**: Drag & drop this folder into the Netlify Sites dashboard.
3. **Vercel**: Run `vercel` in terminal or connect your GitHub repository.

Enjoy your portfolio!
"""
        zip_file.writestr('README.md', readme)

        # Netlify config
        zip_file.writestr('netlify.toml', '[[redirects]]\n  from = "/*"\n  to = "/index.html"\n  status = 200\n')

        # Vercel config
        zip_file.writestr('vercel.json', '{"rewrites": [{"source": "/(.*)", "destination": "/index.html"}]}\n')

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    filename = f"profolio-{portfolio.custom_url or portfolio.user.username}.zip"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

