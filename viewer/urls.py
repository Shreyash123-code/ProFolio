from django.urls import path
from . import views

urlpatterns = [
    path('<slug:custom_url>/', views.portfolio_view, name='portfolio_view'),
    path('<slug:custom_url>/pdf/', views.portfolio_pdf, name='portfolio_pdf'),
]
