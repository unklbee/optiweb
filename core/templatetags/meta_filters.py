# core/templatetags/meta_filters.py
from django import template
from django.utils.html import strip_tags
from django.utils.text import Truncator

register = template.Library()


@register.filter
def meta_description(content, length=160):
    """Generate meta description from content"""
    if not content:
        return ""

    # Strip HTML tags
    clean_content = strip_tags(content)

    # Truncate to specified length
    truncator = Truncator(clean_content)
    return truncator.chars(length, truncate='...')


@register.filter
def reading_time(content):
    """Calculate reading time in minutes"""
    if not content:
        return 0

    # Average reading speed: 200 words per minute
    word_count = len(strip_tags(content).split())
    return max(1, round(word_count / 200))


@register.filter
def social_share_url(url, platform, title=""):
    """Generate social media share URLs"""
    if platform == 'facebook':
        return f"https://www.facebook.com/sharer/sharer.php?u={url}"
    elif platform == 'twitter':
        return f"https://twitter.com/intent/tweet?url={url}&text={title}"
    elif platform == 'whatsapp':
        return f"https://wa.me/?text={title} {url}"
    elif platform == 'telegram':
        return f"https://t.me/share/url?url={url}&text={title}"
    return url