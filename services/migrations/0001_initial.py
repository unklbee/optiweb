# Generated by Django 4.2.21 on 2025-06-01 07:37

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import meta.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=255)),
                ('order', models.IntegerField(default=0, help_text='Urutan tampil')),
            ],
            options={
                'verbose_name': 'Service Category',
                'verbose_name_plural': 'Service Categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Nama layanan (contoh: Ganti LCD Laptop)', max_length=255)),
                ('slug', models.SlugField(blank=True, help_text='URL-friendly name (otomatis)', unique=True)),
                ('description', ckeditor.fields.RichTextField(help_text='Deskripsi lengkap layanan')),
                ('short_description', models.CharField(help_text='Deskripsi singkat untuk preview', max_length=500)),
                ('price_min', models.DecimalField(decimal_places=2, help_text='Harga minimum (Rp)', max_digits=10)),
                ('price_max', models.DecimalField(decimal_places=2, help_text='Harga maksimum (Rp)', max_digits=10)),
                ('duration_estimate', models.CharField(help_text='Estimasi waktu (contoh: 1-2 hari)', max_length=100)),
                ('icon', models.CharField(blank=True, help_text='CSS class icon (contoh: fas fa-laptop)', max_length=255)),
                ('featured_image', models.ImageField(blank=True, help_text='Gambar utama layanan', null=True, upload_to='services/')),
                ('is_featured', models.BooleanField(default=False, help_text='Tampilkan di homepage?')),
                ('is_active', models.BooleanField(default=True, help_text='Layanan masih tersedia?')),
                ('meta_title', models.CharField(blank=True, help_text='Judul SEO (kosongkan untuk otomatis)', max_length=255)),
                ('meta_description', models.TextField(blank=True, help_text='Deskripsi SEO (kosongkan untuk otomatis)')),
                ('target_keywords', models.CharField(blank=True, help_text='Keywords utama (pisahkan dengan koma)', max_length=500)),
                ('category', models.ForeignKey(blank=True, help_text='Kategori layanan', null=True, on_delete=django.db.models.deletion.SET_NULL, to='services.servicecategory')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ['name'],
            },
            bases=(models.Model, meta.models.ModelMeta),
        ),
    ]
