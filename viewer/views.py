from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from builder_app.models import Portfolio, TEMPLATE_CHOICES
import io

def portfolio_view(request, custom_url):
    portfolio = get_object_or_404(Portfolio, custom_url=custom_url)
    projects = portfolio.projects.all().order_by('-created_at')
    
    template_to_use = portfolio.template
    preview_template = request.GET.get('preview_template')
    
    if preview_template and request.user.is_authenticated and request.user == portfolio.user:
        valid_templates = [choice[0] for choice in TEMPLATE_CHOICES]
        if preview_template in valid_templates:
            template_to_use = preview_template
            
    template_name = f'viewer/templates/{template_to_use}.html'
    
    return render(request, template_name, {
        'portfolio': portfolio,
        'projects': projects,
    })


def portfolio_pdf(request, custom_url):
    """Public PDF download for any portfolio."""
    portfolio = get_object_or_404(Portfolio, custom_url=custom_url)
    projects = portfolio.projects.all().order_by('-created_at')
    
    from django.template.loader import render_to_string
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
