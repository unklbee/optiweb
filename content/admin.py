# content/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ContentPage, FAQ, Testimonial, ContactSubmission


@admin.register(ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'page_type',
        'author',
        'is_published',
        'is_featured',
        'publish_date'
    ]
    list_filter = [
        'page_type',
        'is_published',
        'is_featured',
        'author',
        'publish_date'
    ]
    search_fields = ['title', 'content', 'target_keyword']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'is_featured']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'page_type', 'author', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('SEO', {
            'fields': ('target_keyword', 'secondary_keywords', 'meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = [
        'question_short',
        'category',
        'order_priority',
        'is_featured',
        'created_at'
    ]
    list_filter = ['category', 'is_featured']
    search_fields = ['question', 'answer']
    list_editable = ['order_priority', 'is_featured']

    def question_short(self, obj):
        return obj.question[:80] + "..." if len(obj.question) > 80 else obj.question

    question_short.short_description = 'Question'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = [
        'customer_name',
        'laptop_brand',
        'service_type',
        'rating_stars',
        'is_verified',
        'is_featured',
        'created_at'
    ]
    list_filter = [
        'rating',
        'is_verified',
        'is_featured',
        'laptop_brand',
        'created_at'
    ]
    search_fields = ['customer_name', 'review_text', 'laptop_brand']
    list_editable = ['is_verified', 'is_featured']

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(f'<span style="color: gold;">{stars}</span>')

    rating_stars.short_description = 'Rating'


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'inquiry_type',
        'laptop_brand',
        'is_responded',
        'created_at'
    ]
    list_filter = [
        'inquiry_type',
        'is_responded',
        'laptop_brand',
        'created_at'
    ]
    search_fields = ['name', 'email', 'issue_description']
    list_editable = ['is_responded']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'laptop_brand', 'issue_description')
        }),
        ('Admin Notes', {
            'fields': ('is_responded', 'response_date', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.is_responded and not obj.response_date:
            obj.response_date = timezone.now()
        super().save_model(request, obj, form, change)