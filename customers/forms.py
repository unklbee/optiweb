# ========================================
# customers/forms.py - UPDATED with Password Reset
# ========================================

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from .models import CustomerProfile, ServiceOrder


class CustomerRegistrationForm(UserCreationForm):
    """Enhanced registration form with customer profile fields and email validation"""

    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True)
    whatsapp = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs[
                'class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'

        # Update labels
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email Address'
        self.fields['first_name'].label = 'Nama Depan'
        self.fields['last_name'].label = 'Nama Belakang'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Konfirmasi Password'
        self.fields['phone'].label = 'Nomor Telepon'
        self.fields['whatsapp'].label = 'Nomor WhatsApp (Opsional)'
        self.fields['address'].label = 'Alamat Lengkap (Opsional)'

        # Add placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Pilih username unik'
        self.fields['email'].widget.attrs['placeholder'] = 'email@example.com'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nama depan Anda'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nama belakang Anda'
        self.fields['phone'].widget.attrs['placeholder'] = '08xxxxxxxxxx'
        self.fields['whatsapp'].widget.attrs['placeholder'] = '08xxxxxxxxxx (jika berbeda)'
        self.fields['address'].widget.attrs['placeholder'] = 'Alamat lengkap untuk pickup/delivery'

    def clean_email(self):
        """Validate that email is unique"""
        email = self.cleaned_data.get('email')

        if email:
            # Convert to lowercase for consistent checking
            email = email.lower()

            # Check if email already exists
            if User.objects.filter(email__iexact=email).exists():
                raise ValidationError(
                    "Email ini sudah terdaftar. Silakan gunakan email lain atau login dengan akun yang sudah ada."
                )

        return email

    def clean_username(self):
        """Validate username with better error message"""
        username = self.cleaned_data.get('username')

        if username:
            # Check if username already exists
            if User.objects.filter(username__iexact=username).exists():
                raise ValidationError(
                    "Username ini sudah digunakan. Silakan pilih username lain."
                )

        return username

    def clean_phone(self):
        """Validate phone number format and uniqueness"""
        phone = self.cleaned_data.get('phone')

        if phone:
            # Remove any non-digit characters
            clean_phone = ''.join(filter(str.isdigit, phone))

            # Basic validation
            if len(clean_phone) < 10:
                raise ValidationError("Nomor telepon tidak valid. Minimum 10 digit.")

            if len(clean_phone) > 15:
                raise ValidationError("Nomor telepon tidak valid. Maksimum 15 digit.")

            # Check if phone already exists in customer profiles
            if CustomerProfile.objects.filter(phone=phone).exists():
                raise ValidationError(
                    "Nomor telepon ini sudah terdaftar. Silakan gunakan nomor lain."
                )

        return phone

    def save(self, commit=True):
        """Save user with normalized email"""
        user = super().save(commit=False)

        # Normalize email to lowercase
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

            # Create customer profile
            CustomerProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                whatsapp=self.cleaned_data['whatsapp'] or self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )

        return user


class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form that supports email or username"""

    email = forms.CharField(
        label="Email atau Username",
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Masukkan email atau username Anda',
            'autocomplete': 'email'
        })
    )

    def clean_email(self):
        """Find user by email or username"""
        email_or_username = self.cleaned_data['email'].strip()

        if not email_or_username:
            raise ValidationError("Field ini wajib diisi.")

        # Try to find user by email or username
        try:
            from django.db.models import Q
            user = User.objects.get(
                Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)
            )

            # Return the actual email for password reset
            return user.email

        except User.DoesNotExist:
            raise ValidationError(
                "Tidak ditemukan akun dengan email atau username tersebut. "
                "Pastikan Anda memasukkan data yang benar."
            )
        except User.MultipleObjectsReturned:
            # This shouldn't happen with proper email uniqueness, but just in case
            raise ValidationError(
                "Ditemukan beberapa akun dengan data tersebut. "
                "Silakan hubungi customer service untuk bantuan."
            )

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        receiving a reset.
        """
        email_field_name = User.get_email_field_name()
        active_users = User._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
               getattr(u, email_field_name)
        )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form with better styling"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs[
                'class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'

        # Update labels and placeholders
        self.fields['new_password1'].label = 'Password Baru'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Masukkan password baru'

        self.fields['new_password2'].label = 'Konfirmasi Password Baru'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Ulangi password baru'


class ProfileUpdateForm(forms.ModelForm):
    """Form to update customer profile"""

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomerProfile
        fields = ['phone', 'whatsapp', 'address', 'birth_date', 'email_notifications', 'whatsapp_notifications',
                  'promotional_offers']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.user = user

        # Add CSS classes
        for field_name, field in self.fields.items():
            if field_name in ['email_notifications', 'whatsapp_notifications', 'promotional_offers']:
                field.widget.attrs['class'] = 'mr-2'
            else:
                field.widget.attrs[
                    'class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'

        # Update labels
        self.fields['phone'].label = 'Nomor Telepon'
        self.fields['whatsapp'].label = 'Nomor WhatsApp'
        self.fields['address'].label = 'Alamat Lengkap'
        self.fields['birth_date'].label = 'Tanggal Lahir'
        self.fields['email_notifications'].label = 'Notifikasi Email'
        self.fields['whatsapp_notifications'].label = 'Notifikasi WhatsApp'
        self.fields['promotional_offers'].label = 'Penawaran Promosi'

    def clean_email(self):
        """Validate email is unique (except for current user)"""
        email = self.cleaned_data.get('email')

        if email:
            email = email.lower()

            # Check if email exists for other users
            existing_users = User.objects.filter(email__iexact=email)
            if hasattr(self, 'user'):
                existing_users = existing_users.exclude(id=self.user.id)

            if existing_users.exists():
                raise ValidationError(
                    "Email ini sudah digunakan oleh user lain. Silakan gunakan email lain."
                )

        return email

    def clean_phone(self):
        """Validate phone number is unique (except for current profile)"""
        phone = self.cleaned_data.get('phone')

        if phone:
            # Remove any non-digit characters
            clean_phone = ''.join(filter(str.isdigit, phone))

            # Basic validation
            if len(clean_phone) < 10:
                raise ValidationError("Nomor telepon tidak valid. Minimum 10 digit.")

            if len(clean_phone) > 15:
                raise ValidationError("Nomor telepon tidak valid. Maksimum 15 digit.")

            # Check if phone exists for other profiles
            existing_profiles = CustomerProfile.objects.filter(phone=phone)
            if self.instance and self.instance.pk:
                existing_profiles = existing_profiles.exclude(id=self.instance.id)

            if existing_profiles.exists():
                raise ValidationError(
                    "Nomor telepon ini sudah digunakan. Silakan gunakan nomor lain."
                )

        return phone

    def save(self, commit=True):
        """Save profile and update user"""
        profile = super().save(commit=False)

        if commit:
            # Update user fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email'].lower()
            user.save()

            profile.save()

        return profile


class ServiceOrderForm(forms.ModelForm):
    """Form for customers to submit service orders"""

    class Meta:
        model = ServiceOrder
        fields = [
            'service',
            'device_brand',
            'device_model',
            'device_serial',
            'problem_description',
            'priority'
        ]
        widgets = {
            'problem_description': forms.Textarea(attrs={'rows': 4}),
            'device_serial': forms.TextInput(attrs={'placeholder': 'Opsional - jika diketahui'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs[
                'class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'

        # Update labels
        self.fields['service'].label = 'Jenis Layanan'
        self.fields['device_brand'].label = 'Merk Laptop'
        self.fields['device_model'].label = 'Model/Tipe Laptop'
        self.fields['device_serial'].label = 'Serial Number (Opsional)'
        self.fields['problem_description'].label = 'Deskripsi Masalah'
        self.fields['priority'].label = 'Prioritas Service'

        # Add placeholders
        self.fields['device_brand'].widget.attrs['placeholder'] = 'Contoh: Asus, HP, Acer'
        self.fields['device_model'].widget.attrs['placeholder'] = 'Contoh: VivoBook S14, Pavilion 14'
        self.fields['problem_description'].widget.attrs['placeholder'] = 'Jelaskan masalah laptop Anda secara detail...'

        # Filter only active services
        from services.models import Service
        self.fields['service'].queryset = Service.objects.filter(is_active=True)