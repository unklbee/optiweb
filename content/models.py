# content/models.py
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from meta.models import ModelMeta
from slugify import slugify
from core.models import TimeStampedModel


class ContentPage(TimeStampedModel, ModelMeta):
    """Model untuk halaman konten (blog, artikel, landing pages)"""

    PAGE_TYPES = [
        ('blog', 'Blog Post'),
        ('page', 'Static Page'),
        ('faq', 'FAQ'),
        ('tutorial', 'Tutorial'),
        ('news', 'News'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField()
    excerpt = models.TextField(
        blank=True,
        help_text="Ringkasan singkat untuk preview"
    )
    featured_image = models.ImageField(
        upload_to='content/',
        blank=True,
        null=True
    )

    # Content Classification
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # SEO Fields
    target_keyword = models.CharField(
        max_length=255,
        blank=True,
        help_text="Keyword utama untuk SEO"
    )
    secondary_keywords = models.JSONField(
        default=list,
        blank=True,
        help_text="Keywords tambahan (JSON list)"
    )
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # Publishing
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False,
        help_text="Tampilkan di homepage?"
    )
    publish_date = models.DateTimeField(auto_now_add=True)

    # Tags
    tags = TaggableManager(blank=True)

    # Meta configuration for django-meta
    _metadata = {
        'title': 'get_meta_title',
        'description': 'get_meta_description',
        'keywords': 'get_meta_keywords',
        'image': 'get_meta_image',
    }

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "Content Page"
        verbose_name_plural = "Content Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.page_type == 'blog':
            return reverse('content:blog_detail', kwargs={'slug': self.slug})
        return reverse('content:page_detail', kwargs={'slug': self.slug})

    # SEO Methods
    def get_meta_title(self):
        if self.meta_title:
            return self.meta_title
        return f"{self.title} - Service Laptop Bandung"

    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        return self.excerpt or f"{self.title} - Artikel terbaru tentang service laptop di Bandung"

    def get_meta_keywords(self):
        keywords = ['service laptop bandung', 'artikel laptop']
        if self.target_keyword:
            keywords.append(self.target_keyword)
        keywords.extend(self.secondary_keywords)
        keywords.extend([tag.name for tag in self.tags.all()])
        return keywords

    def get_meta_image(self):
        return self.featured_image.url if self.featured_image else None


class FAQ(TimeStampedModel):
    """Model untuk Frequently Asked Questions"""

    CATEGORIES = [
        ('general', 'Umum'),
        ('pricing', 'Harga'),
        ('warranty', 'Garansi'),
        ('service', 'Layanan'),
        ('technical', 'Teknis'),
    ]

    question = models.TextField()
    answer = RichTextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='general'
    )
    order_priority = models.IntegerField(
        default=0,
        help_text="Angka kecil = tampil di atas"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Tampilkan di homepage?"
    )

    class Meta:
        ordering = ['order_priority', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question[:100]


class Testimonial(TimeStampedModel):
    """Model untuk testimonial/review pelanggan"""

    customer_name = models.CharField(max_length=100)
    customer_photo = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True
    )
    laptop_brand = models.CharField(max_length=100, blank=True)
    service_type = models.CharField(max_length=100, blank=True)

    # Review Content
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],  # 1-5 stars
        help_text="Rating 1-5 bintang"
    )
    review_text = models.TextField()

    # Verification
    is_verified = models.BooleanField(
        default=False,
        help_text="Review sudah diverifikasi?"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Tampilkan di homepage?"
    )

    # Location (opsional)
    customer_location = models.CharField(
        max_length=100,
        blank=True,
        help_text="Contoh: Bandung, Dago"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"

    def get_star_range(self):
        """Return range for template loop"""
        return range(self.rating)

    def get_empty_star_range(self):
        """Return range for empty stars"""
        return range(5 - self.rating)


class ContactSubmission(TimeStampedModel):
    """Model untuk menyimpan form contact/inquiry"""

    INQUIRY_TYPES = [
        ('service', 'Service Inquiry'),
        ('quote', 'Price Quote'),
        ('general', 'General Question'),
        ('complaint', 'Complaint'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(
        max_length=20,
        choices=INQUIRY_TYPES,
        default='general'
    )
    laptop_brand = models.CharField(max_length=50, blank=True)
    issue_description = models.TextField()

    # Status tracking
    is_responded = models.BooleanField(default=False)
    response_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(
        blank=True,
        help_text="Internal notes untuk admin"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.name} - {self.inquiry_type}"