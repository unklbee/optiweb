# services/management/commands/populate_services.py

from django.core.management.base import BaseCommand
from services.models import Service, ServiceCategory
from slugify import slugify


class Command(BaseCommand):
    help = 'Populate services with SEO-optimized content'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting services population...'))

        # Create categories first
        self.create_categories()

        # Create services
        self.create_hardware_services()
        self.create_software_services()
        self.create_maintenance_services()

        self.stdout.write(self.style.SUCCESS('Successfully populated all services!'))

    def create_categories(self):
        categories_data = [
            {
                'name': 'Hardware',
                'description': 'Layanan perbaikan komponen fisik laptop seperti LCD, keyboard, motherboard, dan spare part lainnya',
                'icon': 'fas fa-tools',
                'order': 1
            },
            {
                'name': 'Software',
                'description': 'Layanan instalasi, troubleshooting, dan perbaikan sistem operasi serta aplikasi laptop',
                'icon': 'fas fa-laptop-code',
                'order': 2
            },
            {
                'name': 'Maintenance',
                'description': 'Layanan perawatan, cleaning, upgrade, dan optimasi performa laptop',
                'icon': 'fas fa-cogs',
                'order': 3
            }
        ]

        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'order': cat_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

    def create_hardware_services(self):
        hardware_category = ServiceCategory.objects.get(name='Hardware')

        hardware_services = [
            {
                'name': 'Ganti LCD Laptop',
                'short_description': 'Penggantian layar LCD laptop yang pecah, bergaris, atau mati total dengan spare part berkualitas',
                'description': '''
<h3>Layanan Ganti LCD Laptop Profesional di Bandung</h3>
<p>Kami menyediakan layanan penggantian LCD laptop terpercaya untuk semua merk dan tipe. Menggunakan spare part original dan compatible dengan kualitas terjamin.</p>

<h4>🔧 Keunggulan Layanan Ganti LCD:</h4>
<ul>
<li><strong>Spare Part Berkualitas:</strong> Original dan compatible dari supplier terpercaya</li>
<li><strong>Teknisi Berpengalaman:</strong> Lebih dari 5 tahun pengalaman service laptop</li>
<li><strong>Garansi Resmi:</strong> Garansi 1-3 bulan untuk setiap penggantian</li>
<li><strong>Proses Cepat:</strong> Pengerjaan 1-2 hari kerja</li>
<li><strong>Harga Transparan:</strong> Tanpa biaya tersembunyi</li>
</ul>

<h4>💻 Merk Laptop yang Dilayani:</h4>
<p>Asus, Acer, HP, Dell, Lenovo, Toshiba, Sony, MSI, Gigabyte, dan semua merk laptop lainnya.</p>

<h4>🔍 Gejala LCD Rusak:</h4>
<ul>
<li>Layar pecah atau retak</li>
<li>Garis-garis pada layar</li>
<li>Layar berkedip atau flickering</li>
<li>Layar gelap atau blank</li>
<li>Dead pixel atau bintik hitam</li>
</ul>
                ''',
                'price_min': 500000,
                'price_max': 2500000,
                'duration_estimate': '1-2 hari',
                'target_keywords': 'ganti lcd laptop bandung, service layar laptop, penggantian lcd laptop, service lcd laptop bandung',
                'is_featured': True
            },
            {
                'name': 'Ganti Keyboard Laptop',
                'short_description': 'Penggantian keyboard laptop yang rusak, macet, atau tidak responsif dengan garansi resmi',
                'description': '''
<h3>Service Ganti Keyboard Laptop Terpercaya</h3>
<p>Layanan penggantian keyboard laptop untuk semua merk dengan spare part original dan compatible. Solusi untuk keyboard yang macet, tidak responsif, atau rusak.</p>

<h4>✨ Keunggulan Service Keyboard:</h4>
<ul>
<li><strong>Keyboard Original:</strong> Menggunakan spare part original sesuai tipe laptop</li>
<li><strong>Layout Indonesia:</strong> Tersedia keyboard layout Indonesia dan International</li>
<li><strong>Garansi 30 Hari:</strong> Garansi penggantian jika ada masalah</li>
<li><strong>Pengerjaan Cepat:</strong> Selesai dalam 1 hari kerja</li>
</ul>

<h4>🔧 Masalah Keyboard yang Kami Tangani:</h4>
<ul>
<li>Tombol keyboard macet atau tidak berfungsi</li>
<li>Keyboard tidak responsif</li>
<li>Huruf/angka tidak muncul saat ditekan</li>
<li>Keyboard terkena cairan</li>
<li>Tombol copot atau patah</li>
</ul>
                ''',
                'price_min': 150000,
                'price_max': 500000,
                'duration_estimate': '1 hari',
                'target_keywords': 'ganti keyboard laptop bandung, service keyboard laptop, keyboard laptop rusak',
                'is_featured': True
            },
            {
                'name': 'Service Motherboard Laptop',
                'short_description': 'Perbaikan motherboard laptop yang rusak, short, atau mati total oleh teknisi ahli dengan peralatan canggih',
                'description': '''
<h3>Service Motherboard Laptop Expert</h3>
<p>Layanan perbaikan motherboard laptop dengan teknologi terkini dan teknisi berpengalaman. Kami tangani berbagai kerusakan motherboard dari ringan hingga berat.</p>

<h4>🛠️ Jenis Kerusakan Motherboard:</h4>
<ul>
<li><strong>Short Circuit:</strong> Konslet akibat cairan atau komponen rusak</li>
<li><strong>IC Power Rusak:</strong> Laptop tidak mau hidup sama sekali</li>
<li><strong>Chipset Bermasalah:</strong> Laptop restart sendiri atau hang</li>
<li><strong>VGA Onboard Rusak:</strong> No display atau layar bergaris</li>
</ul>

<h4>⚡ Keunggulan Service Motherboard:</h4>
<ul>
<li><strong>Diagnostic Akurat:</strong> Menggunakan alat test profesional</li>
<li><strong>Micro Soldering:</strong> Keahlian solder komponen kecil (BGA, IC)</li>
<li><strong>Spare Part Original:</strong> IC dan komponen original</li>
<li><strong>Garansi Service:</strong> Garansi 30-90 hari</li>
</ul>
                ''',
                'price_min': 500000,
                'price_max': 1500000,
                'duration_estimate': '2-3 hari',
                'target_keywords': 'service motherboard laptop bandung, perbaikan motherboard laptop, laptop mati total'
            },
            {
                'name': 'Ganti Baterai Laptop',
                'short_description': 'Penggantian baterai laptop yang drop, tidak charging, atau cepat habis dengan baterai original',
                'description': '''
<h3>Ganti Baterai Laptop Original</h3>
<p>Layanan penggantian baterai laptop dengan baterai original dan compatible berkualitas tinggi. Solusi untuk laptop yang tidak bisa charging atau baterai cepat habis.</p>

<h4>🔋 Tanda Baterai Laptop Rusak:</h4>
<ul>
<li>Baterai cepat habis (kurang dari 2 jam)</li>
<li>Laptop tidak bisa charging</li>
<li>Baterai kembung atau panas</li>
<li>Indikator baterai tidak akurat</li>
<li>Laptop mati mendadak meski baterai masih ada</li>
</ul>

<h4>✅ Keunggulan Baterai Original:</h4>
<ul>
<li><strong>Kapasitas Penuh:</strong> Sesuai spesifikasi original</li>
<li><strong>Umur Panjang:</strong> Tahan 2-3 tahun pemakaian normal</li>
<li><strong>Safety Protection:</strong> Dilengkapi safety circuit</li>
<li><strong>Garansi 6 Bulan:</strong> Garansi replacement jika bermasalah</li>
</ul>
                ''',
                'price_min': 300000,
                'price_max': 800000,
                'duration_estimate': '1 hari',
                'target_keywords': 'ganti baterai laptop bandung, baterai laptop original, laptop tidak charging'
            },
            {
                'name': 'Ganti Adaptor Charger',
                'short_description': 'Penggantian adaptor charger laptop yang rusak atau tidak berfungsi dengan charger original berkualitas',
                'description': '''
<h3>Ganti Adaptor Charger Laptop Original</h3>
<p>Layanan penggantian adaptor charger laptop dengan charger original dan compatible. Tersedia untuk semua merk laptop dengan berbagai watt dan voltase.</p>

<h4>⚡ Spesifikasi Charger Tersedia:</h4>
<ul>
<li><strong>19V - 65W:</strong> Untuk laptop standar (Asus, Acer, HP)</li>
<li><strong>19.5V - 90W:</strong> Untuk laptop performance (Dell, Sony)</li>
<li><strong>20V - 135W:</strong> Untuk laptop gaming dan workstation</li>
<li><strong>USB-C PD:</strong> Untuk laptop modern dengan port USB-C</li>
</ul>

<h4>🔌 Keunggulan Charger Original:</h4>
<ul>
<li><strong>Voltage Stabil:</strong> Output voltase yang stabil dan aman</li>
<li><strong>Connector Presisi:</strong> Jack yang pas dan tidak longgar</li>
<li><strong>Safety Protection:</strong> Perlindungan over voltage dan short</li>
<li><strong>Garansi 30 Hari:</strong> Garansi replacement</li>
</ul>
                ''',
                'price_min': 150000,
                'price_max': 400000,
                'duration_estimate': '1 hari',
                'target_keywords': 'ganti charger laptop bandung, adaptor laptop original, charger laptop rusak'
            },
            {
                'name': 'Service Fan Laptop',
                'short_description': 'Perbaikan dan penggantian fan laptop yang berisik, macet, atau tidak berputar untuk mencegah overheat',
                'description': '''
<h3>Service Fan Laptop Anti Overheat</h3>
<p>Layanan perbaikan dan penggantian fan laptop yang bermasalah. Mencegah laptop overheat dan menjaga performa optimal laptop Anda.</p>

<h4>🌀 Masalah Fan Laptop:</h4>
<ul>
<li>Fan berisik atau bunyi kasar</li>
<li>Fan tidak berputar sama sekali</li>
<li>Fan berputar lambat</li>
<li>Laptop panas berlebihan</li>
<li>Fan macet karena debu atau kotoran</li>
</ul>

<h4>🔧 Layanan Fan Laptop:</h4>
<ul>
<li><strong>Cleaning Fan:</strong> Pembersihan debu dan kotoran</li>
<li><strong>Ganti Fan Baru:</strong> Penggantian dengan fan original</li>
<li><strong>Ganti Thermal Paste:</strong> Aplikasi thermal paste baru</li>
<li><strong>Optimasi Cooling:</strong> Setting fan curve optimal</li>
</ul>
                ''',
                'price_min': 100000,
                'price_max': 300000,
                'duration_estimate': '1 hari',
                'target_keywords': 'service fan laptop bandung, laptop overheat, fan laptop berisik'
            },
            {
                'name': 'Ganti Jack Power',
                'short_description': 'Perbaikan jack power laptop yang longgar, patah, atau tidak bisa charging dengan spare part original',
                'description': '''
<h3>Service Jack Power Laptop</h3>
<p>Layanan perbaikan jack power (DC jack) laptop yang rusak, longgar, atau tidak bisa charging. Menggunakan spare part original dengan teknik solder yang presisi.</p>

<h4>🔌 Gejala Jack Power Rusak:</h4>
<ul>
<li>Charger harus diposisikan tertentu agar bisa charging</li>
<li>Connector charger longgar</li>
<li>Laptop tidak charging sama sekali</li>
<li>Jack power patah atau copot</li>
<li>Percikan api saat pasang charger</li>
</ul>

<h4>⚡ Keunggulan Service Jack Power:</h4>
<ul>
<li><strong>Solder Presisi:</strong> Teknik micro soldering yang akurat</li>
<li><strong>Jack Original:</strong> Spare part sesuai dengan tipe laptop</li>
<li><strong>Test Menyeluruh:</strong> Test charging dan stabilitas</li>
<li><strong>Garansi 30 Hari:</strong> Garansi service</li>
</ul>
                ''',
                'price_min': 200000,
                'price_max': 500000,
                'duration_estimate': '1-2 hari',
                'target_keywords': 'service jack power laptop, laptop tidak charging, jack power longgar'
            },
            {
                'name': 'Ganti Speaker Laptop',
                'short_description': 'Penggantian speaker laptop yang rusak, tidak bunyi, atau suara pecah dengan speaker original',
                'description': '''
<h3>Service Speaker Laptop</h3>
<p>Layanan penggantian speaker laptop yang mengalami kerusakan suara. Menggunakan speaker original dengan kualitas audio yang jernih.</p>

<h4>🔊 Masalah Speaker Laptop:</h4>
<ul>
<li>Tidak ada suara sama sekali</li>
<li>Suara pecah atau terdistorsi</li>
<li>Volume kecil atau lemah</li>
<li>Suara sebelah (mono)</li>
<li>Crackling atau static noise</li>
</ul>

<h4>🎵 Keunggulan Service Audio:</h4>
<ul>
<li><strong>Speaker Original:</strong> Kualitas audio sesuai standar pabrikan</li>
<li><strong>Test Audio:</strong> Test kualitas suara menyeluruh</li>
<li><strong>Driver Update:</strong> Update driver audio terbaru</li>
<li><strong>Garansi 30 Hari:</strong> Garansi penggantian</li>
</ul>
                ''',
                'price_min': 100000,
                'price_max': 300000,
                'duration_estimate': '1 hari',
                'target_keywords': 'ganti speaker laptop bandung, speaker laptop rusak, service audio laptop'
            }
        ]

        for service_data in hardware_services:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'category': hardware_category,
                    'slug': slugify(service_data['name']),
                    'short_description': service_data['short_description'],
                    'description': service_data['description'],
                    'price_min': service_data['price_min'],
                    'price_max': service_data['price_max'],
                    'duration_estimate': service_data['duration_estimate'],
                    'target_keywords': service_data['target_keywords'],
                    'meta_title': f"{service_data['name']} Bandung - Service Laptop Terpercaya",
                    'meta_description': f"{service_data['short_description']} Garansi resmi, teknisi berpengalaman, harga terjangkau di Bandung.",
                    'is_featured': service_data.get('is_featured', False),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created hardware service: {service.name}')

    def create_software_services(self):
        software_category = ServiceCategory.objects.get(name='Software')

        software_services = [
            {
                'name': 'Install Windows 10',
                'short_description': 'Instalasi Windows 10 original dengan driver lengkap dan aktivasi resmi untuk performa optimal',
                'description': '''
<h3>Instalasi Windows 10 Professional</h3>
<p>Layanan instalasi Windows 10 original dengan lisensi resmi dan driver lengkap. Termasuk optimasi sistem untuk performa maksimal laptop Anda.</p>

<h4>💿 Paket Instalasi Windows 10:</h4>
<ul>
<li><strong>Windows 10 Original:</strong> Lisensi resmi Microsoft</li>
<li><strong>Driver Lengkap:</strong> VGA, Audio, Network, Bluetooth</li>
<li><strong>Software Essential:</strong> Browser, Office trial, Antivirus</li>
<li><strong>Update Terbaru:</strong> Windows Update hingga versi terbaru</li>
</ul>

<h4>⚡ Keunggulan Instalasi Kami:</h4>
<ul>
<li><strong>Clean Install:</strong> Instalasi bersih tanpa bloatware</li>
<li><strong>Optimasi Performa:</strong> Setting optimal untuk laptop</li>
<li><strong>Backup Data:</strong> Backup data penting sebelum install</li>
<li><strong>Garansi 30 Hari:</strong> Garansi sistem berjalan lancar</li>
</ul>

<h4>📋 Yang Termasuk dalam Service:</h4>
<ul>
<li>Partisi harddisk optimal</li>
<li>Instalasi driver original</li>
<li>Setting power management</li>
<li>Aktivasi Windows original</li>
<li>Transfer data penting</li>
</ul>
                ''',
                'price_min': 100000,
                'price_max': 200000,
                'duration_estimate': '2-4 jam',
                'target_keywords': 'install windows 10 bandung, instalasi windows 10, service laptop windows 10',
                'is_featured': True
            },
            {
                'name': 'Install Windows 11',
                'short_description': 'Instalasi Windows 11 terbaru dengan fitur lengkap dan optimasi khusus untuk laptop modern',
                'description': '''
<h3>Instalasi Windows 11 Latest Version</h3>
<p>Layanan instalasi Windows 11 terbaru dengan semua fitur modern dan keamanan terdepan. Cocok untuk laptop dengan spesifikasi yang mendukung.</p>

<h4>🆕 Fitur Windows 11:</h4>
<ul>
<li><strong>Interface Modern:</strong> Start Menu dan Taskbar baru</li>
<li><strong>Microsoft Teams:</strong> Terintegrasi untuk komunikasi</li>
<li><strong>Enhanced Security:</strong> TPM 2.0 dan Secure Boot</li>
<li><strong>Performance Boost:</strong> Optimasi untuk SSD dan multi-core</li>
</ul>

<h4>✅ Persyaratan Windows 11:</h4>
<ul>
<li>Processor: Intel 8th Gen atau AMD Ryzen 2000</li>
<li>RAM: Minimum 4GB (Recommended 8GB)</li>
<li>Storage: 64GB available space</li>
<li>TPM: Version 2.0</li>
<li>UEFI firmware dengan Secure Boot</li>
</ul>
                ''',
                'price_min': 150000,
                'price_max': 250000,
                'duration_estimate': '2-4 jam',
                'target_keywords': 'install windows 11 bandung, instalasi windows 11, upgrade windows 11'
            },
            {
                'name': 'Remove Virus Malware',
                'short_description': 'Pembersihan virus dan malware secara menyeluruh dengan tools professional untuk keamanan data',
                'description': '''
<h3>Remove Virus & Malware Professional</h3>
<p>Layanan pembersihan virus, malware, spyware, dan ransomware menggunakan tools professional dan teknik advanced. Melindungi data dan sistem dari ancaman digital.</p>

<h4>🦠 Jenis Malware yang Kami Tangani:</h4>
<ul>
<li><strong>Virus:</strong> Program perusak yang menginfeksi file</li>
<li><strong>Malware:</strong> Software berbahaya dan adware</li>
<li><strong>Spyware:</strong> Program mata-mata pencuri data</li>
<li><strong>Ransomware:</strong> Malware pengunci file</li>
<li><strong>Trojan:</strong> Program penyamar berbahaya</li>
</ul>

<h4>🛡️ Metode Pembersihan:</h4>
<ul>
<li><strong>Deep Scan:</strong> Scan mendalam seluruh sistem</li>
<li><strong>Registry Cleaning:</strong> Pembersihan registry Windows</li>
<li><strong>Browser Cleaning:</strong> Remove hijacker dan adware</li>
<li><strong>System Restore:</strong> Restore sistem ke kondisi bersih</li>
</ul>

<h4>🔒 Keamanan Tambahan:</h4>
<ul>
<li>Instalasi antivirus premium</li>
<li>Update sistem keamanan</li>
<li>Setting firewall optimal</li>
<li>Edukasi keamanan digital</li>
</ul>
                ''',
                'price_min': 100000,
                'price_max': 200000,
                'duration_estimate': '2-4 jam',
                'target_keywords': 'remove virus laptop bandung, cleaning malware, laptop kena virus'
            },
            {
                'name': 'Recovery Data Hilang',
                'short_description': 'Pemulihan data yang hilang, terhapus, atau corrupt dengan teknologi recovery professional',
                'description': '''
<h3>Data Recovery Professional Service</h3>
<p>Layanan pemulihan data dengan teknologi advanced dan tingkat keberhasilan tinggi. Kami tangani berbagai kasus kehilangan data dari ringan hingga kompleks.</p>

<h4>💾 Jenis Data Recovery:</h4>
<ul>
<li><strong>Deleted Files:</strong> File yang terhapus permanen</li>
<li><strong>Formatted Drive:</strong> Harddisk yang terformat</li>
<li><strong>Corrupted Files:</strong> File yang corrupt atau rusak</li>
<li><strong>System Crash:</strong> Data hilang karena sistem crash</li>
<li><strong>Hardware Failure:</strong> Kerusakan fisik harddisk</li>
</ul>

<h4>🔧 Metode Recovery:</h4>
<ul>
<li><strong>Software Recovery:</strong> Menggunakan tools professional</li>
<li><strong>Hardware Recovery:</strong> Perbaikan fisik harddisk</li>
<li><strong>Sector Recovery:</strong> Recovery dari bad sector</li>
<li><strong>Deep Recovery:</strong> Recovery tingkat low-level</li>
</ul>

<h4>📊 Tingkat Keberhasilan:</h4>
<ul>
<li>Deleted files: 95% success rate</li>
<li>Formatted drive: 85% success rate</li>
<li>Corrupted files: 80% success rate</li>
<li>Hardware failure: 70% success rate</li>
</ul>
                ''',
                'price_min': 200000,
                'price_max': 800000,
                'duration_estimate': '1-3 hari',
                'target_keywords': 'recovery data laptop bandung, data hilang, kembalikan file terhapus'
            },
            {
                'name': 'Service Blue Screen',
                'short_description': 'Perbaikan laptop yang sering blue screen (BSOD) dengan analisis mendalam dan solusi permanen',
                'description': '''
<h3>Service Blue Screen of Death (BSOD)</h3>
<p>Layanan perbaikan laptop yang mengalami blue screen dengan analisis error code dan solusi yang tepat sasaran.</p>

<h4>💙 Penyebab Blue Screen:</h4>
<ul>
<li><strong>Driver Conflict:</strong> Driver yang tidak kompatibel</li>
<li><strong>Hardware Failure:</strong> RAM, HDD, atau motherboard rusak</li>
<li><strong>System Corruption:</strong> File sistem Windows corrupt</li>
<li><strong>Overheating:</strong> Laptop terlalu panas</li>
<li><strong>Malware Attack:</strong> Virus yang merusak sistem</li>
</ul>

<h4>🔍 Metode Diagnostic:</h4>
<ul>
<li><strong>Error Code Analysis:</strong> Analisis kode error BSOD</li>
<li><strong>Memory Test:</strong> Test RAM dengan MemTest86</li>
<li><strong>Hardware Diagnostic:</strong> Test komponen hardware</li>
<li><strong>System File Check:</strong> SFC dan DISM scan</li>
</ul>
                ''',
                'price_min': 150000,
                'price_max': 400000,
                'duration_estimate': '2-4 jam',
                'target_keywords': 'service blue screen bandung, laptop blue screen, bsod laptop'
            },
            {
                'name': 'Service Laptop Lemot',
                'short_description': 'Optimasi laptop yang lemot dan lambat dengan cleaning sistem dan tuning performa menyeluruh',
                'description': '''
<h3>Optimasi Laptop Lemot</h3>
<p>Layanan optimasi laptop yang lambat dengan berbagai teknik tuning performa untuk mengembalikan kecepatan optimal laptop.</p>

<h4>🐌 Penyebab Laptop Lemot:</h4>
<ul>
<li><strong>Startup Programs:</strong> Terlalu banyak program startup</li>
<li><strong>Disk Full:</strong> Harddisk hampir penuh</li>
<li><strong>Malware:</strong> Virus atau malware tersembunyi</li>
<li><strong>Registry Corrupt:</strong> Registry Windows bermasalah</li>
<li><strong>Hardware Aging:</strong> Komponen hardware tua</li>
</ul>

<h4>⚡ Metode Optimasi:</h4>
<ul>
<li><strong>Disk Cleanup:</strong> Pembersihan file sampah</li>
<li><strong>Registry Cleanup:</strong> Optimasi registry Windows</li>
<li><strong>Startup Optimization:</strong> Disable program tidak perlu</li>
<li><strong>Service Optimization:</strong> Optimasi Windows services</li>
<li><strong>Defragmentation:</strong> Defrag harddisk (jika HDD)</li>
</ul>
                ''',
                'price_min': 100000,
                'price_max': 250000,
                'duration_estimate': '1-3 jam',
                'target_keywords': 'laptop lemot bandung, optimasi laptop lambat, laptop lelet'
            }
        ]

        for service_data in software_services:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'category': software_category,
                    'slug': slugify(service_data['name']),
                    'short_description': service_data['short_description'],
                    'description': service_data['description'],
                    'price_min': service_data['price_min'],
                    'price_max': service_data['price_max'],
                    'duration_estimate': service_data['duration_estimate'],
                    'target_keywords': service_data['target_keywords'],
                    'meta_title': f"{service_data['name']} Bandung - Service Laptop Professional",
                    'meta_description': f"{service_data['short_description']} Teknisi ahli, garansi resmi, harga terjangkau di Bandung.",
                    'is_featured': service_data.get('is_featured', False),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created software service: {service.name}')

    def create_maintenance_services(self):
        maintenance_category = ServiceCategory.objects.get(name='Maintenance')

        maintenance_services = [
            {
                'name': 'Cleaning Laptop Menyeluruh',
                'short_description': 'Pembersihan laptop menyeluruh dari debu, kotoran, dan maintenance preventif untuk performa optimal',
                'description': '''
<h3>Cleaning Laptop Professional</h3>
<p>Layanan pembersihan laptop menyeluruh dengan teknik yang aman dan efektif. Menjaga laptop tetap bersih dan berperforma optimal.</p>

<h4>🧹 Yang Dibersihkan:</h4>
<ul>
<li><strong>Keyboard & Touchpad:</strong> Pembersihan tombol dan area touchpad</li>
<li><strong>LCD Screen:</strong> Cleaning layar dengan cairan khusus</li>
<li><strong>Cooling System:</strong> Cleaning fan dan heatsink</li>
<li><strong>Internal Component:</strong> Pembersihan motherboard dan komponen dalam</li>
<li><strong>Port & Connector:</strong> Cleaning semua port dan connector</li>
</ul>

<h4>✨ Manfaat Cleaning Rutin:</h4>
<ul>
<li><strong>Temperature Optimal:</strong> Mencegah overheat</li>
<li><strong>Performa Stabil:</strong> Menjaga performa laptop</li>
<li><strong>Umur Panjang:</strong> Memperpanjang usia laptop</li>
<li><strong>Higenis:</strong> Bebas bakteri dan kuman</li>
</ul>

<h4>🔧 Proses Cleaning:</h4>
<ul>
<li>Disassembly laptop dengan hati-hati</li>
<li>Cleaning dengan compressed air</li>
<li>Pembersihan dengan cairan isopropyl</li>
<li>Pengecekan komponen internal</li>
<li>Assembly kembali dengan teliti</li>
</ul>
                ''',
                'price_min': 75000,
                'price_max': 150000,
                'duration_estimate': '1-2 jam',
                'target_keywords': 'cleaning laptop bandung, service cleaning laptop, laptop kotor berdebu',
                'is_featured': True
            },
            {
                'name': 'Upgrade RAM Laptop',
                'short_description': 'Upgrade RAM laptop untuk meningkatkan performa multitasking dengan memory berkualitas tinggi',
                'description': '''
<h3>Upgrade RAM Laptop Professional</h3>
<p>Layanan upgrade RAM laptop dengan memory berkualitas tinggi untuk meningkatkan performa multitasking dan kecepatan sistem.</p>

<h4>💾 Jenis RAM Tersedia:</h4>
<ul>
<li><strong>DDR3:</strong> Untuk laptop lama (2GB, 4GB, 8GB)</li>
<li><strong>DDR4:</strong> Untuk laptop modern (4GB, 8GB, 16GB, 32GB)</li>
<li><strong>DDR5:</strong> Untuk laptop terbaru (8GB, 16GB, 32GB)</li>
<li><strong>SO-DIMM:</strong> Form factor khusus laptop</li>
</ul>

<h4>⚡ Manfaat Upgrade RAM:</h4>
<ul>
<li><strong>Multitasking Smooth:</strong> Buka banyak aplikasi bersamaan</li>
<li><strong>Gaming Performance:</strong> FPS lebih stabil untuk gaming</li>
<li><strong>Editing Performance:</strong> Faster rendering video/photo</li>
<li><strong>System Responsiveness:</strong> Sistem lebih responsif</li>
</ul>

<h4>📊 Rekomendasi Kapasitas:</h4>
<ul>
<li><strong>4GB:</strong> Basic computing (office, browsing)</li>
<li><strong>8GB:</strong> Standard usage (multitasking ringan)</li>
<li><strong>16GB:</strong> Power user (gaming, editing)</li>
<li><strong>32GB:</strong> Professional (rendering, virtualization)</li>
</ul>
                ''',
                'price_min': 500000,
                'price_max': 2000000,
                'duration_estimate': '1 jam',
                'target_keywords': 'upgrade ram laptop bandung, tambah memory laptop, laptop lemot kurang ram'
            },
            {
                'name': 'Upgrade SSD Laptop',
                'short_description': 'Upgrade harddisk ke SSD untuk performa super cepat dengan teknologi storage terbaru',
                'description': '''
<h3>Upgrade SSD Professional</h3>
<p>Layanan upgrade dari HDD ke SSD atau upgrade SSD ke kapasitas lebih besar untuk performa yang dramatically faster.</p>

<h4>💽 Jenis SSD Tersedia:</h4>
<ul>
<li><strong>SATA SSD:</strong> 2.5" untuk replacement HDD (120GB-2TB)</li>
<li><strong>NVMe M.2:</strong> Ultra-fast untuk laptop modern (256GB-2TB)</li>
<li><strong>PCIe 4.0:</strong> Terbaru dengan kecepatan maksimal</li>
<li><strong>Brand Premium:</strong> Samsung, WD, Crucial, Kingston</li>
</ul>

<h4>🚀 Manfaat Upgrade SSD:</h4>
<ul>
<li><strong>Boot Time:</strong> Windows start dalam 10-15 detik</li>
<li><strong>App Loading:</strong> Aplikasi buka instant</li>
<li><strong>File Transfer:</strong> Copy file super cepat</li>
<li><strong>Silent Operation:</strong> Tidak ada suara moving parts</li>
<li><strong>Power Efficient:</strong> Baterai lebih awet</li>
</ul>

<h4>📈 Perbandingan Kecepatan:</h4>
<ul>
<li><strong>HDD:</strong> 80-160 MB/s read/write</li>
<li><strong>SATA SSD:</strong> 500-550 MB/s read/write</li>
<li><strong>NVMe SSD:</strong> 3,000-7,000 MB/s read/write</li>
</ul>

<h4>🔄 Layanan Include:</h4>
<ul>
<li>Clone data dari HDD lama</li>
<li>Instalasi SSD dengan bracket</li>
<li>Optimasi Windows untuk SSD</li>
<li>Garansi 1 tahun untuk SSD</li>
</ul>
                ''',
                'price_min': 700000,
                'price_max': 3000000,
                'duration_estimate': '1-2 jam',
                'target_keywords': 'upgrade ssd laptop bandung, ganti hdd ke ssd, laptop lambat startup'
            },
            {
                'name': 'Ganti Thermal Paste',
                'short_description': 'Penggantian thermal paste untuk mengatasi laptop overheat dan menjaga suhu optimal processor',
                'description': '''
<h3>Ganti Thermal Paste Professional</h3>
<p>Layanan penggantian thermal paste dengan pasta thermal berkualitas tinggi untuk menjaga suhu processor dan VGA optimal.</p>

<h4>🌡️ Tanda Thermal Paste Kering:</h4>
<ul>
<li><strong>Overheat:</strong> Laptop cepat panas saat digunakan</li>
<li><strong>Throttling:</strong> Performa menurun karena panas</li>
<li><strong>Fan Noise:</strong> Fan bekerja keras terus menerus</li>
<li><strong>Shutdown:</strong> Laptop mati otomatis karena panas</li>
<li><strong>Blue Screen:</strong> BSOD karena temperature tinggi</li>
</ul>

<h4>❄️ Thermal Paste Premium:</h4>
<ul>
<li><strong>Arctic MX-4:</strong> Performance tinggi, tahan lama</li>
<li><strong>Thermal Grizzly:</strong> Premium grade untuk enthusiast</li>
<li><strong>Noctua NT-H1:</strong> Professional thermal compound</li>
<li><strong>Non-Conductive:</strong> Aman tidak menghantarkan listrik</li>
</ul>

<h4>⚡ Manfaat Ganti Thermal Paste:</h4>
<ul>
<li><strong>Temperature Drop:</strong> Suhu turun 10-20°C</li>
<li><strong>Stable Performance:</strong> Tidak ada thermal throttling</li>
<li><strong>Quiet Operation:</strong> Fan tidak bekerja keras</li>
<li><strong>Longevity:</strong> Memperpanjang umur processor</li>
</ul>

<h4>🔧 Proses Aplikasi:</h4>
<ul>
<li>Disassembly laptop total</li>
<li>Cleaning thermal paste lama</li>
<li>Aplikasi thermal paste baru (dot method)</li>
<li>Reassembly dengan torque yang tepat</li>
<li>Temperature testing dan monitoring</li>
</ul>
                ''',
                'price_min': 100000,
                'price_max': 200000,
                'duration_estimate': '1-2 jam',
                'target_keywords': 'ganti thermal paste laptop bandung, laptop overheat panas, service cooling laptop'
            },
            {
                'name': 'Service Laptop Overheat',
                'short_description': 'Solusi komprehensif untuk laptop yang overheat dengan cleaning cooling system dan optimasi thermal',
                'description': '''
<h3>Service Laptop Overheat Complete</h3>
<p>Layanan komprehensif untuk mengatasi laptop overheat dengan pendekatan multi-layer dari hardware cleaning hingga software optimization.</p>

<h4>🔥 Penyebab Laptop Overheat:</h4>
<ul>
<li><strong>Dust Accumulation:</strong> Debu menumpuk di heatsink</li>
<li><strong>Fan Malfunction:</strong> Fan tidak berputar optimal</li>
<li><strong>Thermal Paste Dry:</strong> Thermal paste mengering</li>
<li><strong>Blocked Vents:</strong> Ventilasi tertutup atau tersumbat</li>
<li><strong>High CPU Usage:</strong> Process berat berjalan terus</li>
</ul>

<h4>❄️ Solusi Overheat:</h4>
<ul>
<li><strong>Deep Cleaning:</strong> Cleaning menyeluruh cooling system</li>
<li><strong>Fan Service:</strong> Cleaning atau ganti fan</li>
<li><strong>Thermal Paste:</strong> Aplikasi thermal paste baru</li>
<li><strong>Vent Cleaning:</strong> Cleaning semua ventilasi</li>
<li><strong>Software Optimization:</strong> Optimasi power management</li>
</ul>

<h4>📊 Temperature Monitoring:</h4>
<ul>
<li><strong>Before Service:</strong> Monitor suhu sebelum service</li>
<li><strong>Stress Test:</strong> Test dengan beban maksimal</li>
<li><strong>After Service:</strong> Verifikasi penurunan suhu</li>
<li><strong>Thermal Report:</strong> Laporan temperature sebelum/sesudah</li>
</ul>

<h4>✅ Garansi Temperature:</h4>
<ul>
<li>Garansi penurunan suhu minimal 15°C</li>
<li>Free re-service jika masih overheat dalam 30 hari</li>
<li>Konsultasi gratis optimasi cooling</li>
</ul>
                ''',
                'price_min': 150000,
                'price_max': 300000,
                'duration_estimate': '1-2 jam',
                'target_keywords': 'service laptop overheat bandung, laptop panas mati sendiri, cooling laptop rusak'
            },
            {
                'name': 'Diagnostic Laptop',
                'short_description': 'Diagnostic menyeluruh untuk mendeteksi masalah laptop dengan tools professional dan laporan detail',
                'description': '''
<h3>Diagnostic Laptop Professional</h3>
<p>Layanan diagnostic comprehensive menggunakan tools professional untuk mendeteksi semua masalah hardware dan software laptop.</p>

<h4>🔍 Jenis Diagnostic:</h4>
<ul>
<li><strong>Hardware Diagnostic:</strong> Test semua komponen hardware</li>
<li><strong>Software Diagnostic:</strong> Analisis sistem dan driver</li>
<li><strong>Performance Test:</strong> Benchmark performa laptop</li>
<li><strong>Temperature Monitoring:</strong> Monitor suhu semua komponen</li>
<li><strong>Battery Health:</strong> Test kondisi baterai</li>
</ul>

<h4>🛠️ Tools Professional:</h4>
<ul>
<li><strong>MemTest86:</strong> Test RAM secara mendalam</li>
<li><strong>CrystalDiskInfo:</strong> Health check harddisk/SSD</li>
<li><strong>FurMark:</strong> Stress test VGA card</li>
<li><strong>Prime95:</strong> Stress test processor</li>
<li><strong>HWiNFO:</strong> Monitor komponen real-time</li>
</ul>

<h4>📋 Laporan Diagnostic:</h4>
<ul>
<li><strong>Executive Summary:</strong> Ringkasan kondisi laptop</li>
<li><strong>Component Status:</strong> Status setiap komponen</li>
<li><strong>Performance Score:</strong> Skor performa overall</li>
<li><strong>Recommendation:</strong> Rekomendasi perbaikan/upgrade</li>
<li><strong>Priority Issues:</strong> Masalah yang perlu segera ditangani</li>
</ul>

<h4>💡 Manfaat Diagnostic:</h4>
<ul>
<li>Deteksi dini masalah sebelum fatal</li>
<li>Rekomendasi upgrade yang tepat</li>
<li>Estimasi biaya perbaikan akurat</li>
<li>Panduan maintenance preventif</li>
</ul>
                ''',
                'price_min': 50000,
                'price_max': 100000,
                'duration_estimate': '1 jam',
                'target_keywords': 'diagnostic laptop bandung, cek laptop bermasalah, analisis laptop rusak'
            },
            {
                'name': 'Performance Tuning',
                'short_description': 'Optimasi performa laptop secara menyeluruh untuk memaksimalkan kecepatan dan responsivitas sistem',
                'description': '''
<h3>Performance Tuning Professional</h3>
<p>Layanan optimasi performa laptop secara comprehensive untuk memaksimalkan kecepatan dan responsivitas sistem operasi.</p>

<h4>⚡ Area Optimasi:</h4>
<ul>
<li><strong>Windows Services:</strong> Disable service yang tidak perlu</li>
<li><strong>Startup Programs:</strong> Optimasi program startup</li>
<li><strong>Visual Effects:</strong> Tuning visual untuk performa</li>
<li><strong>Power Settings:</strong> Optimasi power management</li>
<li><strong>Network Settings:</strong> Optimasi koneksi internet</li>
</ul>

<h4>🚀 Teknik Optimasi:</h4>
<ul>
<li><strong>Registry Optimization:</strong> Clean dan optimize registry</li>
<li><strong>Disk Optimization:</strong> Defrag dan disk cleanup</li>
<li><strong>Memory Optimization:</strong> Optimasi penggunaan RAM</li>
<li><strong>CPU Optimization:</strong> Tuning processor affinity</li>
<li><strong>GPU Optimization:</strong> Setting VGA untuk performa</li>
</ul>

<h4>📈 Hasil yang Diharapkan:</h4>
<ul>
<li><strong>Boot Time:</strong> Faster startup 30-50%</li>
<li><strong>Application Launch:</strong> App buka lebih cepat</li>
<li><strong>System Response:</strong> UI lebih responsif</li>
<li><strong>Gaming FPS:</strong> Frame rate lebih tinggi</li>
<li><strong>Multitasking:</strong> Smooth switching antar app</li>
</ul>

<h4>🔧 Tools Optimization:</h4>
<ul>
<li>CCleaner Professional untuk system cleanup</li>
<li>Autoruns untuk startup management</li>
<li>Process Explorer untuk process optimization</li>
<li>MSConfig untuk system configuration</li>
<li>Custom scripts untuk automation</li>
</ul>
                ''',
                'price_min': 150000,
                'price_max': 300000,
                'duration_estimate': '2-4 jam',
                'target_keywords': 'optimasi laptop bandung, tuning performa laptop, laptop lambat optimize'
            }
        ]

        for service_data in maintenance_services:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'category': maintenance_category,
                    'slug': slugify(service_data['name']),
                    'short_description': service_data['short_description'],
                    'description': service_data['description'],
                    'price_min': service_data['price_min'],
                    'price_max': service_data['price_max'],
                    'duration_estimate': service_data['duration_estimate'],
                    'target_keywords': service_data['target_keywords'],
                    'meta_title': f"{service_data['name']} Bandung - Service Laptop Expert",
                    'meta_description': f"{service_data['short_description']} Teknisi professional, garansi service, harga terjangkau di Bandung.",
                    'is_featured': service_data.get('is_featured', False),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created maintenance service: {service.name}')
