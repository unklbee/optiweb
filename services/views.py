# services/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from meta.views import MetadataMixin
from .models import Service, ServiceCategory


class ServiceListView(MetadataMixin, ListView):
    """List semua services"""
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    paginate_by = 12

    # SEO Meta
    title = 'Layanan Service Laptop Bandung - Reparasi Semua Merk'
    description = 'Layanan service laptop lengkap di Bandung. Ganti LCD, keyboard, motherboard, dan lainnya. Teknisi berpengalaman, garansi resmi.'
    keywords = ['service laptop bandung', 'reparasi laptop bandung', 'layanan laptop bandung']

    def get_queryset(self):
        """Filter hanya service yang aktif"""
        queryset = Service.objects.filter(is_active=True)

        # Filter berdasarkan kategori jika ada
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        return context


class ServiceDetailView(MetadataMixin, DetailView):
    """Detail service individual"""
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Related services (same category)
        context['related_services'] = Service.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:3]

        # Breadcrumb untuk service detail
        breadcrumbs = [
            {
                'name': 'Service Laptop Bandung',
                'url': self.request.build_absolute_uri('/')
            },
            {
                'name': 'Layanan',
                'url': self.request.build_absolute_uri('/layanan/')
            }
        ]

        # Tambah category jika ada
        if self.object.category:
            breadcrumbs.append({
                'name': self.object.category.name,
                'url': self.request.build_absolute_uri(f'/layanan/kategori/{self.object.category.slug}/')
            })

        # Tambah service name
        breadcrumbs.append({
            'name': self.object.name,
            'url': self.request.build_absolute_uri(self.object.get_absolute_url())
        })

        context['breadcrumbs'] = breadcrumbs
        return context

def service_category_view(request, slug):
    """Services by category"""
    category = get_object_or_404(ServiceCategory, slug=slug)
    services = Service.objects.filter(category=category, is_active=True)

    context = {
        'category': category,
        'services': services,
        'page_title': f'Layanan {category.name} - Service Laptop Bandung'
    }

    return render(request, 'services/category.html', context)