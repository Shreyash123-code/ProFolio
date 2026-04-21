from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Project
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
import io


def redirect_to_projects():
    """Redirect to index with projects tab active."""
    from django.urls import reverse
    return redirect(reverse('index') + '?tab=projects')

@login_required(login_url='/users/login/')
def index(request):
    portfolio, created = Portfolio.objects.get_or_create(user=request.user)
    projects = portfolio.projects.all().order_by('-created_at')
    
    if request.method == 'POST':
        # Parse form data for portfolio fields
        portfolio.title = request.POST.get('title', portfolio.title)
        portfolio.tagline = request.POST.get('tagline', portfolio.tagline)
        portfolio.bio = request.POST.get('bio', portfolio.bio)
        portfolio.skills = request.POST.get('skills', portfolio.skills)
        portfolio.email = request.POST.get('email', portfolio.email)
        portfolio.github_link = request.POST.get('github_link', portfolio.github_link)
        portfolio.linkedin_link = request.POST.get('linkedin_link', portfolio.linkedin_link)
        portfolio.theme = request.POST.get('theme', portfolio.theme)
        portfolio.template = request.POST.get('template', portfolio.template)
        
        if 'profile_image' in request.FILES:
            portfolio.profile_image = request.FILES['profile_image']
            
        portfolio.save()
        messages.success(request, 'Portfolio saved successfully!')
        return redirect('index')

    return render(request, 'builder_app/index.html', {
        'portfolio': portfolio,
        'projects': projects,
    })


@login_required(login_url='/users/login/')
def add_project(request):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        project = Project(portfolio=portfolio)
            
        project.title = request.POST.get('project_title', '')
        project.description = request.POST.get('project_description', '')
        project.link = request.POST.get('project_link', '')
        project.technology_tags = request.POST.get('project_tags', '')
        
        if 'project_image' in request.FILES:
            project.image = request.FILES['project_image']
            
        project.save()
        messages.success(request, f'Project "{project.title}" added successfully!')
    return redirect_to_projects()


@login_required(login_url='/users/login/')
def edit_project(request, project_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        project = get_object_or_404(Project, id=project_id, portfolio=portfolio)

        title = request.POST.get('project_title', '').strip()
        if title:  # title is required
            project.title = title
        project.description = request.POST.get('project_description', '')
        project.link = request.POST.get('project_link', '')
        project.technology_tags = request.POST.get('project_tags', '')

        if 'project_image' in request.FILES:
            project.image = request.FILES['project_image']

        project.save()
        messages.success(request, f'Project "{project.title}" updated successfully!')
    return redirect_to_projects()


@login_required(login_url='/users/login/')
def delete_project(request, project_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, user=request.user)
        project = get_object_or_404(Project, id=project_id, portfolio=portfolio)
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" deleted successfully.')
    return redirect_to_projects()


@login_required(login_url='/users/login/')
def download_pdf(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    projects = portfolio.projects.all().order_by('-created_at')
    
    html_string = render_to_string('viewer/portfolio_pdf.html', {
        'portfolio': portfolio,
        'projects': projects,
    }, request=request)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{portfolio.user.username}_portfolio.pdf"'
    
    from xhtml2pdf import pisa
    result = pisa.CreatePDF(io.BytesIO(html_string.encode('utf-8')), dest=response)
    
    if result.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response
