# ========================================
# customers/models.py
# ========================================

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from core.models import TimeStampedModel
from services.models import Service


class CustomerProfile(TimeStampedModel):
    """Extended profile for customers"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Loyalty Program
    total_points = models.IntegerField(default=0)
    membership_level = models.CharField(
        max_length=20,
        choices=[
            ('BRONZE', 'Bronze'),
            ('SILVER', 'Silver'),
            ('GOLD', 'Gold'),
            ('PLATINUM', 'Platinum')
        ],
        default='BRONZE'
    )

    # Marketing preferences
    email_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=True)
    promotional_offers = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.membership_level}"

    def update_membership_level(self):
        """Update membership level based on total points"""
        if self.total_points >= 10000:
            self.membership_level = 'PLATINUM'
        elif self.total_points >= 5000:
            self.membership_level = 'GOLD'
        elif self.total_points >= 2000:
            self.membership_level = 'SILVER'
        else:
            self.membership_level = 'BRONZE'
        self.save()

    def add_points(self, points, reason=""):
        """Add points to customer account"""
        self.total_points += points
        self.update_membership_level()

        # Record point transaction
        PointTransaction.objects.create(
            customer=self,
            points=points,
            transaction_type='EARNED',
            reason=reason
        )

    def redeem_points(self, points, reason=""):
        """Redeem points from customer account"""
        if self.total_points >= points:
            self.total_points -= points
            self.save()

            # Record point transaction
            PointTransaction.objects.create(
                customer=self,
                points=-points,
                transaction_type='REDEEMED',
                reason=reason
            )
            return True
        return False

    def get_discount_percentage(self):
        """Get discount based on membership level"""
        discounts = {
            'BRONZE': 0,
            'SILVER': 5,
            'GOLD': 10,
            'PLATINUM': 15
        }
        return discounts.get(self.membership_level, 0)


class ServiceOrder(TimeStampedModel):
    """Service order tracking system"""

    STATUS_CHOICES = [
        ('PENDING', 'Menunggu Konfirmasi'),
        ('CONFIRMED', 'Dikonfirmasi'),
        ('IN_PROGRESS', 'Sedang Dikerjakan'),
        ('WAITING_PARTS', 'Menunggu Spare Part'),
        ('TESTING', 'Testing & Quality Check'),
        ('COMPLETED', 'Selesai'),
        ('DELIVERED', 'Sudah Diambil'),
        ('CANCELLED', 'Dibatalkan'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Normal'),
        ('MEDIUM', 'Prioritas'),
        ('HIGH', 'Express'),
        ('URGENT', 'Emergency')
    ]

    # Order Information
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    # Device Information
    device_brand = models.CharField(max_length=50)
    device_model = models.CharField(max_length=100)
    device_serial = models.CharField(max_length=100, blank=True)
    device_condition = models.TextField(help_text="Kondisi awal device saat diterima")
    problem_description = models.TextField()

    # Service Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='LOW')
    estimated_completion = models.DateTimeField(null=True, blank=True)
    actual_completion = models.DateTimeField(null=True, blank=True)

    # Pricing
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Technician & Notes
    assigned_technician = models.CharField(max_length=100, blank=True)
    internal_notes = models.TextField(blank=True, help_text="Internal notes for technicians")
    customer_notes = models.TextField(blank=True, help_text="Notes visible to customer")

    # Warranty
    warranty_period = models.IntegerField(default=30, help_text="Warranty period in days")
    warranty_expiry = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Service Order"
        verbose_name_plural = "Service Orders"

    def __str__(self):
        return f"{self.order_number} - {self.customer.user.get_full_name()} - {self.service.name}"

    def save(self, *args, **kwargs):
        # Generate order number if new
        if not self.order_number:
            self.order_number = self.generate_order_number()

        # Set warranty expiry when completed
        if self.status == 'COMPLETED' and not self.warranty_expiry:
            self.warranty_expiry = timezone.now() + timedelta(days=self.warranty_period)
            self.actual_completion = timezone.now()

            # Award points when service completed
            self.award_completion_points()

        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Generate unique order number"""
        import random
        import string

        # Format: SLB-YYYYMMDD-XXXX
        today = timezone.now().strftime('%Y%m%d')
        random_suffix = ''.join(random.choices(string.digits, k=4))
        return f"SLB-{today}-{random_suffix}"

    def award_completion_points(self):
        """Award points when service is completed"""
        base_points = 100  # Base points for completion

        # Bonus points based on service cost
        cost_points = int(self.final_cost / 10000) * 10  # 10 points per 10k

        # Bonus points based on priority
        priority_bonus = {
            'LOW': 0,
            'MEDIUM': 20,
            'HIGH': 50,
            'URGENT': 100
        }

        total_points = base_points + cost_points + priority_bonus.get(self.priority, 0)

        self.customer.add_points(
            total_points,
            f"Service completion: {self.service.name}"
        )

    def get_status_display_with_color(self):
        """Get status with color coding"""
        status_colors = {
            'PENDING': 'warning',
            'CONFIRMED': 'info',
            'IN_PROGRESS': 'primary',
            'WAITING_PARTS': 'secondary',
            'TESTING': 'info',
            'COMPLETED': 'success',
            'DELIVERED': 'success',
            'CANCELLED': 'danger'
        }
        return {
            'status': self.get_status_display(),
            'color': status_colors.get(self.status, 'secondary')
        }

    def get_progress_percentage(self):
        """Calculate progress percentage"""
        progress_map = {
            'PENDING': 10,
            'CONFIRMED': 20,
            'IN_PROGRESS': 50,
            'WAITING_PARTS': 60,
            'TESTING': 85,
            'COMPLETED': 95,
            'DELIVERED': 100,
            'CANCELLED': 0
        }
        return progress_map.get(self.status, 0)

    def is_warranty_valid(self):
        """Check if warranty is still valid"""
        if self.warranty_expiry:
            return timezone.now() < self.warranty_expiry
        return False

    def get_absolute_url(self):
        return reverse('customers:order_detail', kwargs={'order_number': self.order_number})


class ServiceUpdate(TimeStampedModel):
    """Service progress updates"""

    order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=20, choices=ServiceOrder.STATUS_CHOICES)
    message = models.TextField()
    is_visible_to_customer = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100, default='System')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"


class PointTransaction(TimeStampedModel):
    """Point transaction history"""

    TRANSACTION_TYPES = [
        ('EARNED', 'Points Earned'),
        ('REDEEMED', 'Points Redeemed'),
        ('EXPIRED', 'Points Expired'),
        ('BONUS', 'Bonus Points'),
        ('ADJUSTMENT', 'Manual Adjustment')
    ]

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='point_transactions')
    points = models.IntegerField()  # Positive for earned, negative for redeemed
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    reason = models.CharField(max_length=255)
    order = models.ForeignKey(ServiceOrder, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.user.username} - {self.points} points - {self.transaction_type}"


class LoyaltyReward(TimeStampedModel):
    """Available loyalty rewards"""

    REWARD_TYPES = [
        ('DISCOUNT', 'Discount Percentage'),
        ('FIXED_AMOUNT', 'Fixed Amount Discount'),
        ('FREE_SERVICE', 'Free Service'),
        ('UPGRADE', 'Service Upgrade'),
        ('GIFT', 'Physical Gift')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    points_required = models.IntegerField()

    # Discount settings
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Availability
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True, help_text="Max number of redemptions")
    current_usage = models.IntegerField(default=0)

    # Conditions
    minimum_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    applicable_services = models.ManyToManyField(Service, blank=True)
    membership_levels = models.JSONField(default=list, help_text="List of membership levels")

    class Meta:
        ordering = ['points_required']

    def __str__(self):
        return f"{self.name} - {self.points_required} points"

    def is_available(self):
        """Check if reward is currently available"""
        now = timezone.now()

        # Check active status
        if not self.is_active:
            return False

        # Check date validity
        if self.valid_until and now > self.valid_until:
            return False

        if now < self.valid_from:
            return False

        # Check usage limit
        if self.usage_limit and self.current_usage >= self.usage_limit:
            return False

        return True

    def can_redeem(self, customer, order_value=0):
        """Check if customer can redeem this reward"""
        if not self.is_available():
            return False

        # Check points
        if customer.total_points < self.points_required:
            return False

        # Check minimum order value
        if order_value < self.minimum_order_value:
            return False

        # Check membership level
        if self.membership_levels and customer.membership_level not in self.membership_levels:
            return False

        return True


class RewardRedemption(TimeStampedModel):
    """Reward redemption history"""

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    reward = models.ForeignKey(LoyaltyReward, on_delete=models.CASCADE)
    order = models.ForeignKey(ServiceOrder, on_delete=models.SET_NULL, null=True, blank=True)
    points_used = models.IntegerField()
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    redemption_code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.redemption_code:
            self.redemption_code = self.generate_redemption_code()
        super().save(*args, **kwargs)

    def generate_redemption_code(self):
        """Generate unique redemption code"""
        import random
        import string

        # Format: RWD-XXXXXXXX
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"RWD-{random_suffix}"

    def __str__(self):
        return f"{self.customer.user.username} - {self.reward.name} - {self.redemption_code}"