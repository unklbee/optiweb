from django.shortcuts import render
from django.http import HttpResponse
from .models import BusinessInfo, LaptopBrand
from services.models import Service
from content.models import FAQ, Testimonial

# View sederhana yang return HttpResponse
def home(request):
    return HttpResponse("Selamat datang di Service Laptop Bandung!")


# View yang render template
def home_template(request):
    # Ambil data dari database
    business = BusinessInfo.objects.first()  # Ambil data bisnis pertama
    brands = LaptopBrand.objects.filter(is_supported=True)  # Brand yang didukung
    featured_services = Service.objects.filter(is_featured=True, is_active=True)[:6]
    featured_faqs = FAQ.objects.filter(is_featured=True)[:5]
    featured_reviews = Testimonial.objects.filter(is_featured=True, is_verified=True)[:3]

    # Breadcrumb untuk homepage
    breadcrumbs = [
        {
            'name': 'Service Laptop Bandung Terpercaya',
            'url': request.build_absolute_uri('/')
        }
    ]

    # Data yang dikirim ke template
    context = {
        'business_info': business,
        'laptop_brands': brands,
        'featured_services': featured_services,
        'featured_faqs': featured_faqs,
        'featured_reviews': featured_reviews,
        'breadcrumbs': breadcrumbs,
        'page_title': 'Service Laptop Bandung Terpercaya | Reparasi Laptop Profesional | optiontech.id',
        'meta_description': 'Service laptop terpercaya di Bandung dengan teknisi berpengalaman. Garansi resmi, harga terjangkau, pickup & delivery. Melayani semua brand laptop.'
    }

    # Render template dengan context
    return render(request, 'core/home.html', context)