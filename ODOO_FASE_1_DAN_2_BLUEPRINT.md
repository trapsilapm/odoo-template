# 📘 BLUEPRINT EKSEKUSI ODOO FOR BUSINESS (FASE 1 & FASE 2)
> **Strategi Deployment Self-Hosted, Kustomisasi Addons, & AI Integration (Hermes Agent)**

Document Version: 1.0  
Status: Ready for Implementation  
Target Infrastructure: GitHub, Cloudflare, Vercel, VPS (Sharing dengan Hermes Agent)

---

## 🏗️ Peta Arsitektur Infrastruktur

```text
[ CLIENT / USER ]
       │
       ▼
 [ Cloudflare ] (DNS, WAF, SSL Proxy)
       │
       ├─────────────────────────────────────────┐
       ▼ (Subdomain: erp.domainanda.com)        ▼ (Subdomain: app.domainanda.com - Opsional)
   [ VPS Ubuntu (Shared) ]                  [ Vercel ]
       │                                        │ (Landing Page / Webhook Gateway)
  ┌────┴──────────────────────────┐             │
  │ Docker Host                   │             │
  │                               │             │
  │ ┌───────────────────────────┐ │             │
  │ │ Container 1: Odoo ERP     │ │             │
  │ │ - Port internal: 8069     │ │◄────────────┘ (REST/XML-RPC API)
  │ └─────────────┬─────────────┘ │
  │               │ DB Connection │
  │ ┌─────────────▼─────────────┐ │
  │ │ Container 2: PostgreSQL   │ │
  │ └───────────────────────────┘ │
  │                               │
  │ ┌───────────────────────────┐ │
  │ │ Existing: Hermes Agent    │ │◄─────────── (Hermes Odoo Connector Module)
  │ └───────────────────────────┘ │
  └───────────────────────────────┘
```

---

## 🚀 FASE 1: Core Odoo Deployment & Base Setup (Hari 1 – 7)

**Fokus Utama**: Menjalankan Odoo Community Edition yang terisolasi aman di VPS bersama Hermes Agent, terhubung ke Cloudflare SSL, dan siap dipakai untuk operasional dasar.

### 1.1 Persiapan VPS & Memory Safety (Penting!)
Karena VPS dibagi bersama Hermes Agent, siapkan **Swap Memory** untuk mencegah *Out of Memory (OOM) Crash*.

```bash
# Cek memory & swap
free -h

# Buat Swap 4GB (jika belum ada swap)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Buatkan permanen di /etc/fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

### 1.2 Struktur Folder Project & Repository GitHub
Buat struktur folder berikut di VPS dan hubungkan ke GitHub Private Repo:

```text
/home/ubuntu/odoo-deployment/
├── docker-compose.yml
├── odoo.conf
├── custom_addons/        # Kustomisasi bisnis Anda (Fase 2)
└── postgres_data/       # Persistence database (Auto created)
```

---

### 1.3 Berkas `docker-compose.yml`
File konfigurasi Docker untuk mengisolasi Odoo & PostgreSQL dari Hermes Agent:

```yaml
version: '3.8'

services:
  web:
    image: odoo:17.0
    container_name: odoo_app
    depends_on:
      - db
    ports:
      - "127.0.0.1:8069:8069" # Hanya listen di localhost agar wajib lewat Nginx/Cloudflare
    volumes:
      - ./odoo.conf:/etc/odoo/odoo.conf
      - ./custom_addons:/mnt/extra-addons
      - odoo-web-data:/var/lib/odoo
    restart: always

  db:
    image: postgres:16
    container_name: odoo_db
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=SuperSecretPassword123!
      - POSTGRES_USER=odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    restart: always

volumes:
  odoo-web-data:
  odoo-db-data:
```

---

### 1.4 Berkas `odoo.conf`
```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
admin_passwd = MasterPasswordMasterKey123!
db_host = db
db_port = 5432
db_user = odoo
db_password = SuperSecretPassword123!
proxy_mode = True
list_db = False
```

---

### 1.5 Cloudflare & Nginx Reverse Proxy Setup
1. **Cloudflare DNS**: Tambahkan `A Record`: `erp.domainanda.com` $\rightarrow$ `IP_VPS_ANDA` (Proxy Status: *Proxied / Orange Cloud*).
2. **Nginx Reverse Proxy** di VPS:

```nginx
server {
    listen 80;
    server_name erp.domainanda.com;

    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;

    # Header proxy Cloudflare
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Real-IP $remote_addr;

    location / {
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8069;
    }

    location ~* /web/static/ {
        proxy_cache_valid 200 90m;
        proxy_buffering on;
        expires 8d;
        proxy_pass http://127.0.0.1:8069;
    }
}
```

---

### 1.6 Inisialisasi Modul & Data Bisnis Pertama
Buka `https://erp.domainanda.com`, lalu buat database pertama:
1. **Language**: Indonesian / English
2. **Country**: Indonesia
3. **Demo Data**: *Uncheck* (Kosongkan)
4. **Aktifkan Modul Utama**:
   - `Sales` (Penjualan)
   - `Invoicing` (Faktur & Pembayaran)
   - `Inventory` (Manajemen Stok & Gudang)
   - `Purchase` (Pembelian & Supplier)
   - `Contacts` (Buku Alamat Pelanggan & Vendor)

---

## 🎨 FASE 2: Customization & Hermes Agent AI Integration (Minggu 2 – 4)

**Fokus Utama**: Menyesuaikan Odoo dengan identitas & aturan bisnis Indonesia, serta menghubungkan Hermes Agent sebagai Asisten AI Bisnis.

---

### 2.1 Lokalisasi & Kustomisasi Modul (`custom_addons/`)
Buat modul kustom di folder `custom_addons/` agar tidak merusak kode bawaan Odoo.

**Daftar Kustomisasi Wajib**:
1. **Format Cetak PDF (Invoice & Surat Jalan)**:
   - Tambahkan Logo Perusahaan, Catatan Rekening Bank, dan Stempel Digital.
2. **Pajak & Mata Uang**:
   - Set Default Currency ke **IDR (Rp)**.
   - Set Default Tax ke **PPN 11%** (atau tarif berlaku).
3. **Custom Dashboard Ringkas**:
   - Menyederhanakan tampilan menu agar karyawan fokus hanya ke fitur yang dipakai.

---

### 2.2 Integrasi Hermes Agent dengan Odoo (AI Assistant)

Hermes Agent yang sudah ada di VPS dapat berkomunikasi langsung dengan Odoo melalui **JSON-RPC API** bawaan Odoo.

```text
User (WhatsApp / Telegram) 
       │
       ▼
 [ Hermes Agent ] ──(JSON-RPC API)──► [ Odoo Database ]
                                              │
 User <─── (Jawaban Rangkuman AI) ────────────┘
```

#### Contoh Script Konektor Hermes -> Odoo (`hermes_odoo_bridge.py`):
Hermes Agent dapat menggunakan modul Python ini untuk query data secara aman:

```python
import xmlrpc.client

class OdooHermesBridge:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        
        # Authenticate
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.uid = common.authenticate(db, username, password, {})
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    def get_today_sales_summary(self):
        """Query omset penjualan hari ini untuk Hermes Agent"""
        orders = self.models.execute_kw(
            self.db, self.uid, self.password,
            'sale.order', 'search_read',
            [[['state', 'in', ['sale', 'done']]]],
            {'fields': ['name', 'amount_total', 'date_order']}
        )
        total_omset = sum(order['amount_total'] for order in orders)
        return f"Total omset hari ini dari {len(orders)} transaksi adalah Rp {total_omset:,.0f}"

    def check_product_stock(self, product_name):
        """Query stok barang berdasarkan nama produk"""
        products = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.product', 'search_read',
            [[['name', 'ilike', product_name]]],
            {'fields': ['name', 'qty_available']}
        )
        return products
```

#### Capabilities AI Hermes Setelah Terintegrasi:
* 📊 **Query Omset**: *"Hermes, berapa total omset penjualan minggu ini?"*
* 📦 **Cek Stok**: *"Hermes, cek sisa stok Barang X di gudang."*
* 👤 **Informasi Customer**: *"Hermes, tampilkan riwayat pembelian PT ABC."*
* 📝 **Drafting Lead**: *"Hermes, buatkan prospek customer baru nama Pak Eko HP 0812345678."*

---

### 2.3 Peran Vercel (Optional / Strategic Frontend)
Anda dapat menggunakan **Vercel** untuk keperluan berikut:
1. **Landing Page Company Profile**: Website utama perusahaan yang ringan, terpisah dari VPS Odoo agar jika VPS restart, website depan tetap 100% online.
2. **Form Lead Acquisition**: Form pendaftaran / order dari customer umum di Vercel yang mengirimkan webhook data calon pelanggan langsung masuk ke Odoo CRM via API.

---

## 📋 Checklist Eksekusi Ringkas

| Hari | Target Pekerjaan | Status |
|---|---|---|
| **Hari 1** | Setup Swap RAM 4GB & Folder Project di VPS | ⬜ Pending |
| **Hari 2** | Konfigurasi `docker-compose.yml` & Jalankan Odoo + Postgres | ⬜ Pending |
| **Hari 3** | Setup Cloudflare DNS + Nginx Reverse Proxy (HTTPS) | ⬜ Pending |
| **Hari 4** | Inisialisasi Database Odoo & Install Modul Sales, Inv, Purchase | ⬜ Pending |
| **Hari 5-7** | Input Data Master (Produk, Harga, Pelanggan, Vendor) | ⬜ Pending |
| **Minggu 2** | Setup `custom_addons` & Kustomisasi Nota/Invoice PDF IDR | ⬜ Pending |
| **Minggu 3** | Hubungkan Hermes Agent via Odoo XML-RPC/JSON-RPC API | ⬜ Pending |
| **Minggu 4** | Testing Alur Bisnis dari Input Barang $\rightarrow$ Sales $\rightarrow$ Invoicing | ⬜ Pending |

---

> **Rekomendasi**: Simpan blueprint ini di repository GitHub Anda sebagai panduan teknis selama proses penggelaran.
