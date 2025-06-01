# content/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from meta.views import MetadataMixin
from .models import ContentPage, FAQ, Testimonial, ContactSubmission
from .forms import ContactForm


class BlogListView(MetadataMixin, ListView):
    """List blog posts"""
    model = ContentPage
    template_name = 'content/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    title = 'Blog Service Laptop Bandung - Tips & Tutorial'
    description = 'Artikel, tips, dan tutorial seputar service laptop, maintenance, dan troubleshooting. Update terbaru dari ahli service laptop Bandung.'
    keywords = ['blog service laptop', 'tips laptop bandung', 'tutorial service laptop']

    def get_queryset(self):
        return ContentPage.objects.filter(
            page_type='blog',
            is_published=True
        )


class BlogDetailView(MetadataMixin, DetailView):
    """Detail blog post"""
    model = ContentPage
    template_name = 'content/blog_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return ContentPage.objects.filter(
            page_type='blog',
            is_published=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related posts by tags
        related_posts = ContentPage.objects.filter(
            page_type='blog',
            is_published=True,
            tags__in=self.object.tags.all()
        ).exclude(id=self.object.id).distinct()[:3]

        context['related_posts'] = related_posts
        return context


class PageDetailView(MetadataMixin, DetailView):
    """Detail static page"""
    model = ContentPage
    template_name = 'content/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return ContentPage.objects.filter(is_published=True)


def faq_view(request):
    """FAQ page with categories"""
    faqs = FAQ.objects.all()
    categories = FAQ.CATEGORIES

    # Group FAQs by category
    faq_by_category = {}
    for category_code, category_name in categories:
        faq_by_category[category_name] = faqs.filter(category=category_code)

    context = {
        'faq_by_category': faq_by_category,
        'page_title': 'FAQ - Frequently Asked Questions',
        'meta_description': 'Jawaban untuk pertanyaan yang sering diajukan tentang service laptop di Bandung. Informasi harga, garansi, dan layanan.'
    }

    return render(request, 'content/faq.html', context)


# content/views.py - update function testimonials_view
def testimonials_view(request):
    """Testimonials page"""
    testimonials = Testimonial.objects.filter(is_verified=True)

    # Calculate average rating
    total_reviews = testimonials.count()
    if total_reviews > 0:
        avg_rating = sum([t.rating for t in testimonials]) / total_reviews

        # Calculate rating distribution with percentages
        rating_distribution = {}
        for i in range(1, 6):
            count = testimonials.filter(rating=i).count()
            percentage = (count * 100 // total_reviews) if total_reviews > 0 else 0
            rating_distribution[i] = {
                'count': count,
                'percentage': percentage
            }
    else:
        avg_rating = 0
        rating_distribution = {}

    context = {
        'testimonials': testimonials,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 1),
        'rating_distribution': rating_distribution,
        'page_title': 'Testimonial Customer - Service Laptop Bandung',
        'meta_description': f'Baca {total_reviews}+ review dari customer yang puas dengan layanan service laptop kami di Bandung. Rating rata-rata {round(avg_rating, 1)}/5 bintang.'
    }

    return render(request, 'content/testimonials.html', context)


def contact_view(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()
            messages.success(request, 'Pesan Anda berhasil dikirim! Kami akan segera menghubungi Anda.')

            # Optional: Send notification email to admin
            # send_contact_notification(submission)

            return JsonResponse({
                'success': True,
                'message': 'Pesan berhasil dikirim!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': 'Kontak Kami - Service Laptop Bandung',
        'meta_description': 'Hubungi service laptop terpercaya di Bandung. Konsultasi gratis, respons cepat, layanan pickup & delivery tersedia.'
    }

    return render(request, 'content/contact.html', context)


def about_view(request):
    """About page"""
    context = {
        'page_title': 'Tentang Kami - Service Laptop Bandung Terpercaya',
        'meta_description': 'Tentang service laptop terpercaya di Bandung. Tim teknisi berpengalaman, fasilitas lengkap, dan komitmen memberikan layanan terbaik.'
    }

    return render(request, 'content/about.html', context)