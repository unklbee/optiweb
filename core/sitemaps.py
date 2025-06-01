# core/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from services.models import Service, ServiceCategory
from content.models import ContentPage


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home', 'content:about']

    def location(self, item):
        if ':' in item:
            return reverse(item)
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return ServiceCategory.objects.all()

    def location(self, obj):
        return reverse('services:category', args=[obj.slug])


class ContentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ContentPage.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return ContentPage.objects.filter(page_type='blog', is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()