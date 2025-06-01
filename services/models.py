# services/models.py
from django.core import cache
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from meta.models import ModelMeta
from slugify import slugify
from core.models import TimeStampedModel


class Service(TimeStampedModel, ModelMeta):
    """Model untuk layanan service laptop"""

    name = models.CharField(max_length=255, help_text="Nama layanan (contoh: Ganti LCD Laptop)")
    slug = models.SlugField(unique=True, blank=True, help_text="URL-friendly name (otomatis)")
    description = RichTextField(help_text="Deskripsi lengkap layanan")
    short_description = models.CharField(
        max_length=500,
        help_text="Deskripsi singkat untuk preview"
    )

    # Pricing & Duration
    price_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Harga minimum (Rp)"
    )
    price_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Harga maksimum (Rp)"
    )
    duration_estimate = models.CharField(
        max_length=100,
        help_text="Estimasi waktu (contoh: 1-2 hari)"
    )

    # SEO & Display
    icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="CSS class icon (contoh: fas fa-laptop)"
    )
    featured_image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        help_text="Gambar utama layanan"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Tampilkan di homepage?"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Layanan masih tersedia?"
    )

    # SEO Fields
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Judul SEO (kosongkan untuk otomatis)"
    )
    meta_description = models.TextField(
        blank=True,
        help_text="Deskripsi SEO (kosongkan untuk otomatis)"
    )
    target_keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="Keywords utama (pisahkan dengan koma)"
    )

    # Django-meta configuration
    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'image': 'get_meta_image',
    }

    class Meta:
        ordering = ['name']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """URL untuk detail service"""
        return reverse('services:detail', kwargs={'slug': self.slug})

    def get_price_range(self):
        """Format harga range"""
        if self.price_min == self.price_max:
            return f"Rp {self.price_min:,.0f}"
        return f"Rp {self.price_min:,.0f} - {self.price_max:,.0f}"

    # SEO Methods
    def get_meta_title(self):
        """Generate SEO title"""
        if self.meta_title:
            return self.meta_title
        return f"{self.name} - Service Laptop Bandung Terpercaya"

    def get_meta_description(self):
        """Generate SEO description"""
        if self.meta_description:
            return self.meta_description
        return f"{self.short_description} Layanan {self.name} terpercaya di Bandung dengan harga {self.get_price_range()}."

    def get_meta_keywords(self):
        """Generate SEO keywords"""
        keywords = ['service laptop bandung', 'reparasi laptop bandung']
        if self.target_keywords:
            keywords.extend([kw.strip() for kw in self.target_keywords.split(',')])
        keywords.append(self.name.lower())
        return keywords

    def get_meta_image(self):
        """Get meta image URL"""
        if self.featured_image:
            return self.featured_image.url
        return None

    def get_related_services(self):
        """Get related services with caching"""
        cache_key = f'related_services_{self.id}'
        related = cache.get(cache_key)

        if related is None:
            related = Service.objects.filter(
                category=self.category,
                is_active=True
            ).exclude(id=self.id)[:3]
            cache.set(cache_key, related, 60 * 15)  # Cache for 15 minutes

        return related


class ServiceCategory(TimeStampedModel):
    """Kategori layanan untuk grouping"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0, help_text="Urutan tampil")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# Update Service model - tambahkan relationship ke category
# Tambahkan field ini di class Service setelah field is_active:
Service.add_to_class('category', models.ForeignKey(
    ServiceCategory,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    help_text="Kategori layanan"
))
