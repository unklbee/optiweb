# ========================================
# customers/forms.py
# ========================================

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomerProfile, ServiceOrder


class CustomerRegistrationForm(UserCreationForm):
    """Enhanced registration form with customer profile fields"""

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
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

    def save(self, commit=True):
        profile = super().save(commit=False)

        if commit:
            # Update user fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
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