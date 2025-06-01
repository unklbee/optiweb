from django.urls import path
from django.views.generic import TemplateView
from . import views  # Import views dari app ini

urlpatterns = [
    path('', views.home_template, name='home'),
    path('simple/', views.home, name='home_simple'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
]