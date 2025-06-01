# core/context_processors.py
from .models import BusinessInfo, LaptopBrand
from services.models import ServiceCategory

def business_info(request):
    """Make business info available globally"""
    try:
        business = BusinessInfo.objects.first()
        return {'business_info': business}
    except BusinessInfo.DoesNotExist:
        return {'business_info': None}

def navigation_data(request):
    """Data untuk navigation menu"""
    return {
        'nav_service_categories': ServiceCategory.objects.all()[:5],
        'nav_brands': LaptopBrand.objects.filter(is_supported=True)[:8]
    }

def seo_globals(request):
    """Global SEO data"""
    return {
        'site_name': 'Service Laptop Bandung Terpercaya',
        'site_description': 'Layanan service laptop terpercaya di Bandung dengan teknisi berpengalaman dan garansi resmi.',
        'site_keywords': 'service laptop bandung, reparasi laptop bandung, teknisi laptop bandung'
    }