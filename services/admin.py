# services/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Service, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'price_range_display',
        'duration_estimate',
        'is_featured',
        'is_active',
        'created_at'
    ]
    list_filter = [
        'category',
        'is_featured',
        'is_active',
        'created_at'
    ]
    search_fields = ['name', 'description', 'target_keywords']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_active']

    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('name', 'slug', 'category', 'short_description', 'description')
        }),
        ('Harga & Durasi', {
            'fields': ('price_min', 'price_max', 'duration_estimate')
        }),
        ('Display Settings', {
            'fields': ('icon', 'featured_image', 'is_featured', 'is_active')
        }),
        ('SEO Optimization', {
            'fields': ('meta_title', 'meta_description', 'target_keywords'),
            'classes': ('collapse',)  # Bisa di-collapse
        }),
    )

    def price_range_display(self, obj):
        """Custom display untuk price range"""
        return obj.get_price_range()

    price_range_display.short_description = 'Harga'

    def save_model(self, request, obj, form, change):
        """Custom save untuk auto-generate SEO jika kosong"""
        if not obj.meta_title:
            obj.meta_title = f"{obj.name} - Service Laptop Bandung"
        if not obj.meta_description:
            obj.meta_description = f"{obj.short_description} Layanan terpercaya di Bandung."
        super().save_model(request, obj, form, change)