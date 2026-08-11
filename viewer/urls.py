from django.urls import path
from . import views

urlpatterns = [
    path('<slug:custom_url>/', views.portfolio_view, name='portfolio_view'),
]
