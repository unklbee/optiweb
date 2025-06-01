# ========================================
# customers/admin.py
# ========================================

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CustomerProfile, ServiceOrder, ServiceUpdate,
    PointTransaction, LoyaltyReward, RewardRedemption
)


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'membership_level',
        'total_points',
        'phone',
        'created_at'
    ]
    list_filter = ['membership_level', 'email_notifications', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['total_points', 'membership_level']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone', 'whatsapp', 'address', 'birth_date')
        }),
        ('Loyalty Program', {
            'fields': ('total_points', 'membership_level'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'whatsapp_notifications', 'promotional_offers')
        })
    )


class ServiceUpdateInline(admin.TabularInline):
    model = ServiceUpdate
    extra = 1
    fields = ['status', 'message', 'is_visible_to_customer', 'created_by']


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number',
        'customer_name',
        'service',
        'device_brand',
        'status_colored',
        'priority',
        'created_at',
        'estimated_completion'
    ]
    list_filter = [
        'status',
        'priority',
        'service__category',
        'device_brand',
        'created_at'
    ]
    search_fields = [
        'order_number',
        'customer__user__username',
        'customer__user__email',
        'device_model',
        'device_serial'
    ]
    readonly_fields = ['order_number', 'warranty_expiry', 'actual_completion']

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'service', 'priority')
        }),
        ('Device Information', {
            'fields': ('device_brand', 'device_model', 'device_serial', 'device_condition', 'problem_description')
        }),
        ('Service Progress', {
            'fields': ('status', 'assigned_technician', 'estimated_completion', 'actual_completion')
        }),
        ('Pricing', {
            'fields': ('estimated_cost', 'final_cost', 'discount_amount', 'total_paid')
        }),
        ('Notes', {
            'fields': ('internal_notes', 'customer_notes')
        }),
        ('Warranty', {
            'fields': ('warranty_period', 'warranty_expiry')
        })
    )

    inlines = [ServiceUpdateInline]

    def customer_name(self, obj):
        return obj.customer.user.get_full_name() or obj.customer.user.username

    customer_name.short_description = 'Customer'

    def status_colored(self, obj):
        status_info = obj.get_status_display_with_color()
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            status_info['color'],
            status_info['status']
        )

    status_colored.short_description = 'Status'


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'points',
        'transaction_type',
        'reason',
        'created_at'
    ]
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['customer__user__username', 'reason']
    readonly_fields = ['created_at']


@admin.register(LoyaltyReward)
class LoyaltyRewardAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'reward_type',
        'points_required',
        'is_active',
        'current_usage',
        'usage_limit'
    ]
    list_filter = ['reward_type', 'is_active']
    filter_horizontal = ['applicable_services']


@admin.register(RewardRedemption)
class RewardRedemptionAdmin(admin.ModelAdmin):
    list_display = [
        'redemption_code',
        'customer',
        'reward',
        'points_used',
        'is_used',
        'created_at'
    ]
    list_filter = ['is_used', 'created_at']
    search_fields = ['redemption_code', 'customer__user__username']