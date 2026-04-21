from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-project/', views.add_project, name='add_project'),
    path('edit-project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]
