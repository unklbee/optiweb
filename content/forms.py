# content/forms.py
from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = [
            'name',
            'email',
            'phone',
            'inquiry_type',
            'laptop_brand',
            'issue_description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nama lengkap Anda'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '08xxxxxxxxxx'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'laptop_brand': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Contoh: Asus, HP, Acer, dll'
            }),
            'issue_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Jelaskan masalah laptop Anda secara detail...',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nama Lengkap'
        self.fields['email'].label = 'Email'
        self.fields['phone'].label = 'Nomor WhatsApp/HP'
        self.fields['inquiry_type'].label = 'Jenis Pertanyaan'
        self.fields['laptop_brand'].label = 'Merk Laptop'
        self.fields['issue_description'].label = 'Deskripsi Masalah'

        # Make phone optional
        self.fields['phone'].required = False
        self.fields['laptop_brand'].required = False