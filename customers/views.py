# ========================================
# customers/views.py
# ========================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import CustomerProfile, ServiceOrder, LoyaltyReward, RewardRedemption, PointTransaction
from .forms import CustomerRegistrationForm, ProfileUpdateForm, ServiceOrderForm


def register_view(request):
    """Customer registration view"""
    if request.user.is_authenticated:
        return redirect('customers:dashboard')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Auto login after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Registrasi berhasil! Selamat datang di Service Laptop Bandung.')
            return redirect('customers:dashboard')
    else:
        form = CustomerRegistrationForm()

    context = {
        'form': form,
        'page_title': 'Daftar Akun Customer - Service Laptop Bandung'
    }
    return render(request, 'customers/register.html', context)


@login_required
def dashboard_view(request):
    """Customer dashboard with overview"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        # Create profile if doesn't exist
        profile = CustomerProfile.objects.create(user=request.user)

    # Get recent orders
    recent_orders = ServiceOrder.objects.filter(customer=profile).order_by('-created_at')[:5]

    # Get statistics
    total_orders = ServiceOrder.objects.filter(customer=profile).count()
    active_orders = ServiceOrder.objects.filter(
        customer=profile,
        status__in=['PENDING', 'CONFIRMED', 'IN_PROGRESS', 'WAITING_PARTS', 'TESTING']
    ).count()
    completed_orders = ServiceOrder.objects.filter(customer=profile, status='DELIVERED').count()

    # Get available rewards
    available_rewards = LoyaltyReward.objects.filter(
        is_active=True,
        points_required__lte=profile.total_points
    )[:3]

    # Get recent point transactions
    recent_points = PointTransaction.objects.filter(customer=profile)[:5]

    context = {
        'profile': profile,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'active_orders': active_orders,
        'completed_orders': completed_orders,
        'available_rewards': available_rewards,
        'recent_points': recent_points,
        'page_title': 'Dashboard Customer - Service Laptop Bandung'
    }
    return render(request, 'customers/dashboard.html', context)


@login_required
def profile_view(request):
    """Customer profile management"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile berhasil diupdate!')
            return redirect('customers:profile')
    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)

    context = {
        'form': form,
        'profile': profile,
        'page_title': 'Profile Saya - Service Laptop Bandung'
    }
    return render(request, 'customers/profile.html', context)


@login_required
def create_order_view(request):
    """Create new service order"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = profile

            # Set estimated cost based on service price range
            service = order.service
            order.estimated_cost = (service.price_min + service.price_max) / 2

            # Set estimated completion (based on service duration)
            from datetime import timedelta
            duration_map = {
                '1 hari': 1,
                '2 hari': 2,
                '1-2 hari': 2,
                '2-3 hari': 3,
                '3-5 hari': 5,
                '1 jam': 0.5,
                '2-4 jam': 0.5
            }
            duration_days = duration_map.get(service.duration_estimate, 3)
            order.estimated_completion = timezone.now() + timedelta(days=duration_days)

            order.save()

            # Create initial service update
            from .models import ServiceUpdate
            ServiceUpdate.objects.create(
                order=order,
                status='PENDING',
                message='Order baru diterima dan menunggu konfirmasi dari teknisi.',
                created_by='System'
            )

            messages.success(
                request,
                f'Order berhasil dibuat dengan nomor {order.order_number}. '
                'Kami akan segera menghubungi Anda untuk konfirmasi.'
            )
            return redirect('customers:order_detail', order_number=order.order_number)
    else:
        form = ServiceOrderForm()

    context = {
        'form': form,
        'page_title': 'Buat Order Service - Service Laptop Bandung'
    }
    return render(request, 'customers/create_order.html', context)


@login_required
def orders_view(request):
    """List all customer orders with filtering"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)

    orders = ServiceOrder.objects.filter(customer=profile).order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Search
    search = request.GET.get('search')
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(service__name__icontains=search) |
            Q(device_brand__icontains=search) |
            Q(device_model__icontains=search)
        )

    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Status choices for filter
    status_choices = ServiceOrder.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'status_choices': status_choices,
        'current_status': status_filter,
        'search_query': search,
        'page_title': 'Riwayat Order - Service Laptop Bandung'
    }
    return render(request, 'customers/orders.html', context)


@login_required
def order_detail_view(request, order_number):
    """Detailed view of specific order"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)

    order = get_object_or_404(ServiceOrder, order_number=order_number, customer=profile)
    updates = order.updates.filter(is_visible_to_customer=True).order_by('-created_at')

    context = {
        'order': order,
        'updates': updates,
        'page_title': f'Order {order.order_number} - Service Laptop Bandung'
    }
    return render(request, 'customers/order_detail.html', context)


@login_required
def loyalty_view(request):
    """Loyalty program dashboard"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)

    # Available rewards
    available_rewards = LoyaltyReward.objects.filter(is_active=True)
    redeemable_rewards = [r for r in available_rewards if r.can_redeem(profile)]

    # Point transactions
    point_transactions = PointTransaction.objects.filter(customer=profile)[:20]

    # Redemption history
    redemptions = RewardRedemption.objects.filter(customer=profile).order_by('-created_at')[:10]

    # Membership progress
    membership_progress = {
        'BRONZE': {'min': 0, 'max': 1999, 'next': 'SILVER'},
        'SILVER': {'min': 2000, 'max': 4999, 'next': 'GOLD'},
        'GOLD': {'min': 5000, 'max': 9999, 'next': 'PLATINUM'},
        'PLATINUM': {'min': 10000, 'max': float('inf'), 'next': None}
    }

    current_progress = membership_progress.get(profile.membership_level, membership_progress['BRONZE'])

    context = {
        'profile': profile,
        'available_rewards': available_rewards,
        'redeemable_rewards': redeemable_rewards,
        'point_transactions': point_transactions,
        'redemptions': redemptions,
        'current_progress': current_progress,
        'page_title': 'Program Loyalty - Service Laptop Bandung'
    }
    return render(request, 'customers/loyalty.html', context)


@login_required
def redeem_reward_view(request, reward_id):
    """Redeem loyalty reward"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)

    reward = get_object_or_404(LoyaltyReward, id=reward_id, is_active=True)

    if request.method == 'POST':
        if reward.can_redeem(profile):
            # Redeem points
            if profile.redeem_points(reward.points_required, f"Redeemed: {reward.name}"):
                # Create redemption record
                redemption = RewardRedemption.objects.create(
                    customer=profile,
                    reward=reward,
                    points_used=reward.points_required
                )

                # Update reward usage
                reward.current_usage += 1
                reward.save()

                messages.success(
                    request,
                    f'Reward "{reward.name}" berhasil ditukar! '
                    f'Kode redemption: {redemption.redemption_code}'
                )
                return redirect('customers:loyalty')
            else:
                messages.error(request, 'Poin tidak mencukupi untuk menukar reward ini.')
        else:
            messages.error(request, 'Reward tidak tersedia atau tidak memenuhi syarat.')

    context = {
        'reward': reward,
        'profile': profile,
        'can_redeem': reward.can_redeem(profile),
        'page_title': f'Tukar Reward: {reward.name}'
    }
    return render(request, 'customers/redeem_reward.html', context)


@login_required
def notifications_view(request):
    """Customer notifications center"""
    try:
        profile = request.user.customerprofile
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile.objects.create(user=request.user)

    # Get notifications from order updates
    notifications = []

    # Recent order updates
    recent_updates = []
    for order in ServiceOrder.objects.filter(customer=profile)[:10]:
        for update in order.updates.filter(is_visible_to_customer=True)[:2]:
            recent_updates.append({
                'type': 'order_update',
                'title': f'Update Order {order.order_number}',
                'message': update.message,
                'date': update.created_at,
                'order': order
            })

    # Point transactions
    for transaction in PointTransaction.objects.filter(customer=profile)[:5]:
        recent_updates.append({
            'type': 'points',
            'title': f'Points {transaction.get_transaction_type_display()}',
            'message': f'{transaction.points} points - {transaction.reason}',
            'date': transaction.created_at
        })

    # Sort by date
    notifications = sorted(recent_updates, key=lambda x: x['date'], reverse=True)[:20]

    context = {
        'notifications': notifications,
        'profile': profile,
        'page_title': 'Notifikasi - Service Laptop Bandung'
    }
    return render(request, 'customers/notifications.html', context)


# AJAX Views
@login_required
def check_order_status_ajax(request, order_number):
    """AJAX endpoint to check order status"""
    try:
        profile = request.user.customerprofile
        order = ServiceOrder.objects.get(order_number=order_number, customer=profile)

        return JsonResponse({
            'status': order.status,
            'status_display': order.get_status_display(),
            'progress': order.get_progress_percentage(),
            'last_update': order.updates.filter(
                is_visible_to_customer=True).first().created_at.isoformat() if order.updates.exists() else None
        })
    except (CustomerProfile.DoesNotExist, ServiceOrder.DoesNotExist):
        return JsonResponse({'error': 'Order not found'}, status=404)


@login_required
def get_service_price_ajax(request, service_id):
    """AJAX endpoint to get service price range"""
    try:
        from services.models import Service
        service = Service.objects.get(id=service_id, is_active=True)

        return JsonResponse({
            'price_min': float(service.price_min),
            'price_max': float(service.price_max),
            'price_range': service.get_price_range(),
            'duration': service.duration_estimate
        })
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)