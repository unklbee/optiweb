# ========================================
# customers/urls.py - UPDATED
# ========================================

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'customers'

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='customers/login.html',
        redirect_authenticated_user=True,
        extra_context={'page_title': 'Login Customer - Service Laptop Bandung'}
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Password Reset with Custom Forms
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='customers/password_reset.html',
        email_template_name='customers/password_reset_email.html',
        html_email_template_name='customers/password_reset_email.html',
        subject_template_name='customers/password_reset_subject.txt',
        form_class=CustomPasswordResetForm,
        extra_context={
            'page_title': 'Reset Password - Service Laptop Bandung'
        }
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='customers/password_reset_done.html',
        extra_context={
            'page_title': 'Reset Password Terkirim - Service Laptop Bandung'
        }
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='customers/password_reset_confirm.html',
        form_class=CustomSetPasswordForm,
        extra_context={
            'page_title': 'Konfirmasi Reset Password - Service Laptop Bandung'
        }
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='customers/password_reset_complete.html',
        extra_context={
            'page_title': 'Password Berhasil Direset - Service Laptop Bandung'
        }
    ), name='password_reset_complete'),

    # Customer Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('notifications/', views.notifications_view, name='notifications'),

    # Orders
    path('orders/', views.orders_view, name='orders'),
    path('orders/create/', views.create_order_view, name='create_order'),
    path('orders/<str:order_number>/', views.order_detail_view, name='order_detail'),

    # Loyalty Program
    path('loyalty/', views.loyalty_view, name='loyalty'),
    path('loyalty/redeem/<int:reward_id>/', views.redeem_reward_view, name='redeem_reward'),

    # AJAX Endpoints
    path('ajax/order-status/<str:order_number>/', views.check_order_status_ajax, name='check_order_status'),
    path('ajax/service-price/<int:service_id>/', views.get_service_price_ajax, name='get_service_price'),
]