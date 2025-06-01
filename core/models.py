from django.db import models


# Model dasar dengan timestamp
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Otomatis diisi saat create
    updated_at = models.DateTimeField(auto_now=True)  # Otomatis diisi saat update

    class Meta:
        abstract = True  # Model ini tidak akan jadi tabel, hanya template


# Model untuk info bisnis
class BusinessInfo(TimeStampedModel):
    business_name = models.CharField(max_length=255)  # Nama bisnis
    address = models.TextField()  # Alamat (text panjang)
    phone = models.CharField(max_length=20)  # Nomor telepon
    email = models.EmailField()  # Email (validasi otomatis)
    whatsapp = models.CharField(max_length=20)  # WhatsApp

    class Meta:
        verbose_name = "Business Information"  # Nama di admin
        verbose_name_plural = "Business Information"  # Nama plural di admin

    def __str__(self):
        return self.business_name  # Yang tampil saat print object


# Model untuk brand laptop
class LaptopBrand(TimeStampedModel):
    name = models.CharField(max_length=100)  # Nama brand
    slug = models.SlugField(unique=True)  # URL-friendly name
    logo = models.ImageField(  # Upload gambar logo
        upload_to='brands/',  # Folder penyimpanan
        blank=True,  # Boleh kosong
        null=True  # Boleh NULL di database
    )
    is_supported = models.BooleanField(default=True)  # Apakah masih didukung

    class Meta:
        ordering = ['name']  # Urutan default A-Z

    def __str__(self):
        return self.name