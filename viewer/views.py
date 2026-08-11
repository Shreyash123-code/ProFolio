from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from builder_app.models import Portfolio, TEMPLATE_CHOICES
import io

@xframe_options_sameorigin
def portfolio_view(request, custom_url):
    portfolio = get_object_or_404(Portfolio, custom_url=custom_url)
    projects = portfolio.projects.all()
    educations = portfolio.educations.all()
    experiences = portfolio.experiences.all()
    certificates = portfolio.certificates.all()

    template_to_use = portfolio.template or 'minimal_developer'
    preview_template = request.GET.get('preview_template')

    if preview_template and request.user.is_authenticated and request.user == portfolio.user:
        valid_templates = [choice[0] for choice in TEMPLATE_CHOICES]
        if preview_template in valid_templates:
            template_to_use = preview_template

    template_name = f'viewer/templates/{template_to_use}.html'

    return render(request, template_name, {
        'portfolio': portfolio,
        'projects': projects,
        'educations': educations,
        'experiences': experiences,
        'certificates': certificates,
    })

