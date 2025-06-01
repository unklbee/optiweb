#!/usr/bin/env python
"""
Script untuk setup database dan data awal
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optiontech_web.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from core.models import BusinessInfo, LaptopBrand
from services.models import ServiceCategory, Service


def setup_database():
    print("🔄 Setting up database...")

    # 1. Makemigrations
    print("1. Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])

    # 2. Migrate
    print("2. Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])

    # 3. Create superuser if not exists
    print("3. Creating superuser...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("   ✅ Superuser created: admin/admin123")
    else:
        print("   ✅ Superuser already exists")

    # 4. Create business info
    print("4. Creating business info...")
    if not BusinessInfo.objects.exists():
        BusinessInfo.objects.create(
            business_name="Service Laptop Bandung",
            address="Jl. Contoh No. 123, Bandung, Jawa Barat",
            phone="022-1234567",
            email="info@servicelaptopmandung.com",
            whatsapp="6281234567890"
        )
        print("   ✅ Business info created")
    else:
        print("   ✅ Business info already exists")

    # 5. Create laptop brands
    print("5. Creating laptop brands...")
    brands = ['Asus', 'Acer', 'HP', 'Dell', 'Lenovo', 'Toshiba', 'Sony', 'MSI']
    for brand_name in brands:
        brand, created = LaptopBrand.objects.get_or_create(
            name=brand_name,
            defaults={'slug': brand_name.lower(), 'is_supported': True}
        )
        if created:
            print(f"   ✅ Created brand: {brand_name}")

    # 6. Create service categories
    print("6. Creating service categories...")
    categories_data = [
        {'name': 'Hardware', 'icon': 'fas fa-tools', 'order': 1},
        {'name': 'Software', 'icon': 'fas fa-laptop-code', 'order': 2},
        {'name': 'Maintenance', 'icon': 'fas fa-cogs', 'order': 3},
    ]

    for cat_data in categories_data:
        category, created = ServiceCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': cat_data['name'].lower(),
                'icon': cat_data['icon'],
                'order': cat_data['order']
            }
        )
        if created:
            print(f"   ✅ Created category: {cat_data['name']}")

    # 7. Create sample services
    print("7. Creating sample services...")
    hardware_cat = ServiceCategory.objects.get(name='Hardware')

    sample_services = [
        {
            'name': 'Ganti LCD Laptop',
            'category': hardware_cat,
            'short_description': 'Penggantian layar LCD laptop yang rusak atau pecah',
            'description': 'Layanan penggantian LCD laptop dengan spare part berkualitas',
            'price_min': 500000,
            'price_max': 2000000,
            'duration_estimate': '1-2 hari',
            'is_featured': True
        },
        {
            'name': 'Ganti Keyboard Laptop',
            'category': hardware_cat,
            'short_description': 'Penggantian keyboard laptop yang rusak atau tidak responsif',
            'description': 'Layanan penggantian keyboard laptop dengan spare part original',
            'price_min': 150000,
            'price_max': 500000,
            'duration_estimate': '1 hari',
            'is_featured': True
        }
    ]

    for service_data in sample_services:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f"   ✅ Created service: {service_data['name']}")

    print("\n🎉 Database setup completed!")
    print("🔑 Admin login: admin/admin123")
    print("🌐 Admin URL: http://127.0.0.1:8000/admin/")
    print("🏠 Website: http://127.0.0.1:8000/")


if __name__ == '__main__':
    setup_database()