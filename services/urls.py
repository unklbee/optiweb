# services/urls.py
from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # List semua services
    path('', views.ServiceListView.as_view(), name='list'),

    # Services by category
    path('kategori/<slug:slug>/', views.service_category_view, name='category'),

    # Detail service
    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='detail'),
]