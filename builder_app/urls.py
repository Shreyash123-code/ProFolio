from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-project/', views.add_project, name='add_project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    
    path('add-education/', views.add_education, name='add_education'),
    path('edit-education/<int:edu_id>/', views.edit_education, name='edit_education'),
    path('delete-education/<int:edu_id>/', views.delete_education, name='delete_education'),
    
    path('add-experience/', views.add_experience, name='add_experience'),
    path('edit-experience/<int:exp_id>/', views.edit_experience, name='edit_experience'),
    path('delete-experience/<int:exp_id>/', views.delete_experience, name='delete_experience'),
    
    path('add-certificate/', views.add_certificate, name='add_certificate'),
    path('edit-certificate/<int:cert_id>/', views.edit_certificate, name='edit_certificate'),
    path('delete-certificate/<int:cert_id>/', views.delete_certificate, name='delete_certificate'),
    
    path('api/generate-ai-content/', views.generate_ai_content, name='generate_ai_content'),
    path('api/import-resume/', views.import_resume, name='import_resume'),
    path('api/import-github-repos/', views.import_github_repos, name='import_github_repos'),
    path('export-zip/', views.export_portfolio_zip, name='export_portfolio_zip'),
]

