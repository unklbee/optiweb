# content/urls.py
from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),

    # Static pages
    path('tentang-kami/', views.about_view, name='about'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),

    # FAQ
    path('faq/', views.faq_view, name='faq'),

    # Testimonials
    path('testimonial/', views.testimonials_view, name='testimonials'),

    # Contact
    path('kontak/', views.contact_view, name='contact'),
]