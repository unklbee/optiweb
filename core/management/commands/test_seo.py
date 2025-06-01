# core/management/commands/test_seo.py
from django.core.management.base import BaseCommand
from django.test.client import Client
from django.urls import reverse
from services.models import Service
from content.models import ContentPage


class Command(BaseCommand):
    help = 'Test SEO elements across the site'

    def handle(self, *args, **options):
        client = Client()

        # Test homepage
        response = client.get('/')
        self.check_seo_elements(response, 'Homepage')

        # Test services
        services = Service.objects.filter(is_active=True)[:3]
        for service in services:
            response = client.get(service.get_absolute_url())
            self.check_seo_elements(response, f'Service: {service.name}')

        # Test blog posts
        blog_posts = ContentPage.objects.filter(page_type='blog', is_published=True)[:3]
        for post in blog_posts:
            response = client.get(post.get_absolute_url())
            self.check_seo_elements(response, f'Blog: {post.title}')

        self.stdout.write(self.style.SUCCESS('SEO testing completed!'))

    def check_seo_elements(self, response, page_name):
        content = response.content.decode('utf-8')

        # Check title tag
        if '<title>' in content and '</title>' in content:
            title = content.split('<title>')[1].split('</title>')[0]
            self.stdout.write(f"✅ {page_name}: Title OK - {title[:50]}...")
        else:
            self.stdout.write(f"❌ {page_name}: Missing title tag")

        # Check meta description
        if 'name="description"' in content:
            self.stdout.write(f"✅ {page_name}: Meta description OK")
        else:
            self.stdout.write(f"❌ {page_name}: Missing meta description")

        # Check schema markup
        if 'application/ld+json' in content:
            self.stdout.write(f"✅ {page_name}: Schema markup OK")
        else:
            self.stdout.write(f"⚠️  {page_name}: No schema markup found")