# core/templatetags/schema_tags.py
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.simple_tag
def local_business_schema(business_info):
    """Generate LocalBusiness schema markup"""
    if not business_info:
        return ""

    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": business_info.business_name,
        "description": "Layanan service laptop terpercaya di Bandung",
        "telephone": business_info.phone,
        "email": business_info.email,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": business_info.address,
            "addressLocality": "Bandung",
            "addressRegion": "Jawa Barat",
            "addressCountry": "ID"
        },
        "url": "https://servicelaptopdanbandung.com",
        "priceRange": "$",
        "openingHours": ["Mo-Sa 08:00-20:00"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Layanan Service Laptop",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Service Laptop"
                    }
                }
            ]
        }
    }

    # if business_info.latitude and business_info.longitude:
    #     schema["geo"] = {
    #         "@type": "GeoCoordinates",
    #         "latitude": str(business_info.latitude),
    #         "longitude": str(business_info.longitude)
    #     }

    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>')


@register.simple_tag
def service_schema(service):
    """Generate Service schema markup"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": service.name,
        "description": service.short_description,
        "provider": {
            "@type": "LocalBusiness",
            "name": "Service Laptop Bandung"
        },
        "areaServed": {
            "@type": "City",
            "name": "Bandung"
        },
        "offers": {
            "@type": "Offer",
            "priceRange": service.get_price_range(),
            "priceCurrency": "IDR"
        }
    }

    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>')


@register.simple_tag
def faq_schema(faqs):
    """Generate FAQ schema markup"""
    if not faqs:
        return ""

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }

    for faq in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq.question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq.answer
            }
        })

    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>')


@register.simple_tag
def review_schema(reviews):
    """Generate Review schema markup"""
    if not reviews:
        return ""

    total_rating = sum([r.rating for r in reviews])
    avg_rating = total_rating / len(reviews) if reviews else 0

    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Service Laptop Bandung",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": round(avg_rating, 1),
            "reviewCount": len(reviews),
            "bestRating": 5,
            "worstRating": 1
        },
        "review": []
    }

    for review in reviews[:5]:  # Limit to 5 reviews
        schema["review"].append({
            "@type": "Review",
            "author": {
                "@type": "Person",
                "name": review.customer_name
            },
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": review.rating,
                "bestRating": 5,
                "worstRating": 1
            },
            "reviewBody": review.review_text,
            "datePublished": review.created_at.strftime("%Y-%m-%d")
        })

    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>')


@register.simple_tag
def breadcrumb_schema(breadcrumbs):
    """Generate Breadcrumb schema markup"""
    if not breadcrumbs:
        return ""

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }

    for position, breadcrumb in enumerate(breadcrumbs, 1):
        schema["itemListElement"].append({
            "@type": "ListItem",
            "position": position,
            "name": breadcrumb['name'],
            "item": breadcrumb['url']
        })

    return mark_safe(f'<script type="application/ld+json">{json.dumps(schema, indent=2)}</script>')
