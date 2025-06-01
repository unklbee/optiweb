# core/management/commands/setup_initial_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import BusinessInfo, LaptopBrand
from services.models import ServiceCategory, Service
from content.models import FAQ, Testimonial
from customers.models import CustomerProfile


class Command(BaseCommand):
    help = 'Setup initial data for the application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔄 Setting up initial data...'))

        # Create business info
        self.create_business_info()

        # Create laptop brands
        self.create_laptop_brands()

        # Create service categories
        self.create_service_categories()

        # Create sample services
        self.create_sample_services()

        # Create FAQs
        self.create_faqs()

        # Create testimonials
        self.create_testimonials()

        # Create test customer
        self.create_test_customer()

        self.stdout.write(self.style.SUCCESS('✅ Initial data setup completed!'))

    def create_business_info(self):
        if not BusinessInfo.objects.exists():
            BusinessInfo.objects.create(
                business_name="Service Laptop Bandung",
                address="Jl. Sudirman No. 123, Bandung, Jawa Barat 40123",
                phone="022-1234567",
                email="info@servicelaptopmandung.com",
                whatsapp="6281234567890"
            )
            self.stdout.write('✅ Business info created')
        else:
            self.stdout.write('✅ Business info already exists')

    def create_laptop_brands(self):
        brands = [
            'Asus', 'Acer', 'HP', 'Dell', 'Lenovo',
            'Toshiba', 'Sony', 'MSI', 'Gigabyte', 'Apple'
        ]

        for brand_name in brands:
            brand, created = LaptopBrand.objects.get_or_create(
                name=brand_name,
                defaults={
                    'slug': brand_name.lower(),
                    'is_supported': True
                }
            )
            if created:
                self.stdout.write(f'✅ Created brand: {brand_name}')

    def create_service_categories(self):
        categories = [
            {
                'name': 'Hardware',
                'description': 'Layanan perbaikan komponen fisik laptop',
                'icon': 'fas fa-tools',
                'order': 1
            },
            {
                'name': 'Software',
                'description': 'Layanan instalasi dan perbaikan software',
                'icon': 'fas fa-laptop-code',
                'order': 2
            },
            {
                'name': 'Maintenance',
                'description': 'Layanan perawatan dan optimasi laptop',
                'icon': 'fas fa-cogs',
                'order': 3
            }
        ]

        for cat_data in categories:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✅ Created category: {cat_data["name"]}')

    def create_sample_services(self):
        # Get categories
        hardware = ServiceCategory.objects.get(name='Hardware')
        software = ServiceCategory.objects.get(name='Software')
        maintenance = ServiceCategory.objects.get(name='Maintenance')

        services = [
            # Hardware
            {
                'name': 'Ganti LCD Laptop',
                'category': hardware,
                'short_description': 'Penggantian layar LCD laptop yang rusak atau pecah dengan spare part berkualitas',
                'description': '<p>Layanan penggantian LCD laptop profesional dengan spare part berkualitas tinggi. Melayani semua merk laptop dengan garansi resmi.</p>',
                'price_min': 500000,
                'price_max': 2500000,
                'duration_estimate': '1-2 hari',
                'icon': 'fas fa-desktop',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Ganti Keyboard Laptop',
                'category': hardware,
                'short_description': 'Penggantian keyboard laptop yang rusak atau tidak responsif',
                'description': '<p>Layanan penggantian keyboard laptop dengan spare part original. Tersedia layout Indonesia dan International.</p>',
                'price_min': 150000,
                'price_max': 500000,
                'duration_estimate': '1 hari',
                'icon': 'fas fa-keyboard',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Service Motherboard',
                'category': hardware,
                'short_description': 'Perbaikan motherboard laptop yang rusak atau mati total',
                'description': '<p>Layanan perbaikan motherboard laptop dengan teknisi berpengalaman dan peralatan canggih.</p>',
                'price_min': 300000,
                'price_max': 1500000,
                'duration_estimate': '2-3 hari',
                'icon': 'fas fa-microchip',
                'is_featured': True,
                'is_active': True
            },

            # Software
            {
                'name': 'Install Windows 10',
                'category': software,
                'short_description': 'Instalasi Windows 10 original dengan driver lengkap',
                'description': '<p>Instalasi Windows 10 original dengan lisensi resmi, driver lengkap, dan optimasi sistem.</p>',
                'price_min': 100000,
                'price_max': 200000,
                'duration_estimate': '2-4 jam',
                'icon': 'fab fa-windows',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Remove Virus',
                'category': software,
                'short_description': 'Pembersihan virus dan malware secara menyeluruh',
                'description': '<p>Layanan pembersihan virus, malware, dan spyware menggunakan tools professional.</p>',
                'price_min': 50000,
                'price_max': 150000,
                'duration_estimate': '1-2 jam',
                'icon': 'fas fa-shield-virus',
                'is_featured': True,
                'is_active': True
            },

            # Maintenance
            {
                'name': 'Cleaning Laptop',
                'category': maintenance,
                'short_description': 'Pembersihan laptop menyeluruh dari debu dan kotoran',
                'description': '<p>Layanan cleaning laptop menyeluruh untuk menjaga performa dan mencegah overheat.</p>',
                'price_min': 75000,
                'price_max': 150000,
                'duration_estimate': '1-2 jam',
                'icon': 'fas fa-broom',
                'is_featured': True,
                'is_active': True
            }
        ]

        for service_data in services:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'✅ Created service: {service_data["name"]}')

    def create_faqs(self):
        faqs = [
            {
                'question': 'Berapa lama waktu service laptop?',
                'answer': '<p>Waktu service bervariasi tergantung jenis kerusakan. Untuk service ringan seperti instalasi software: 2-4 jam. Untuk penggantian spare part: 1-3 hari kerja.</p>',
                'category': 'general',
                'order_priority': 1,
                'is_featured': True
            },
            {
                'question': 'Apakah ada garansi untuk service?',
                'answer': '<p>Ya, kami memberikan garansi untuk setiap pekerjaan yang kami lakukan. Garansi bervariasi dari 1-3 bulan tergantung jenis service.</p>',
                'category': 'warranty',
                'order_priority': 2,
                'is_featured': True
            },
            {
                'question': 'Bagaimana cara mengetahui estimasi biaya service?',
                'answer': '<p>Untuk estimasi biaya, Anda bisa konsultasi gratis dengan teknisi kami melalui WhatsApp atau datang langsung untuk diagnosa.</p>',
                'category': 'pricing',
                'order_priority': 3,
                'is_featured': True
            },
        ]

        for faq_data in faqs:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'✅ Created FAQ: {faq_data["question"][:50]}...')

    def create_testimonials(self):
        testimonials = [
            {
                'customer_name': 'Andi Wijaya',
                'laptop_brand': 'Asus',
                'service_type': 'Ganti LCD',
                'rating': 5,
                'review_text': 'Service sangat memuaskan! LCD laptop saya diganti dengan cepat dan hasilnya seperti baru. Teknisinya juga sangat profesional.',
                'customer_location': 'Bandung',
                'is_verified': True,
                'is_featured': True
            },
            {
                'customer_name': 'Sari Melati',
                'laptop_brand': 'HP',
                'service_type': 'Cleaning Laptop',
                'rating': 5,
                'review_text': 'Laptop saya yang tadinya panas dan berisik sekarang sudah normal kembali setelah di-cleaning. Pelayanan ramah dan harga terjangkau.',
                'customer_location': 'Bandung',
                'is_verified': True,
                'is_featured': True
            },
            {
                'customer_name': 'Budi Santoso',
                'laptop_brand': 'Acer',
                'service_type': 'Install Windows',
                'rating': 4,
                'review_text': 'Instalasi Windows 10 berjalan lancar. Driver sudah lengkap dan laptop jadi lebih cepat. Recommended!',
                'customer_location': 'Bandung',
                'is_verified': True,
                'is_featured': True
            }
        ]

        for testimonial_data in testimonials:
            testimonial, created = Testimonial.objects.get_or_create(
                customer_name=testimonial_data['customer_name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'✅ Created testimonial: {testimonial_data["customer_name"]}')

    def create_test_customer(self):
        # Create test user
        if not User.objects.filter(username='customer').exists():
            user = User.objects.create_user(
                username='customer',
                email='customer@test.com',
                password='customer123',
                first_name='John',
                last_name='Doe'
            )

            # Create customer profile
            CustomerProfile.objects.create(
                user=user,
                phone='081234567890',
                whatsapp='081234567890',
                address='Jl. Test No. 123, Bandung',
                total_points=250
            )

            self.stdout.write('✅ Test customer created: customer/customer123')
        else:
            self.stdout.write('✅ Test customer already exists')