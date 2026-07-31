# 📖 PANDUAN LENGKAP PENGGUNAAN MODUL ODOO 17 ERP

Panduan praktis ini berisi penjelasan detail mengenai fungsi, alur kerja, dan langkah-langkah (*step-by-step*) penggunaan 10 modul utama yang aktif di sistem Odoo Anda.

---

## 📑 Daftar Isi Modul
1. [💬 Discuss (Obrolan & Komunikasi Internal)](#1-discuss-obrolan--komunikasi-internal)
2. [👥 Contacts (Buku Alamat & Manajemen Data Kontak)](#2-contacts-buku-alamat--manajemen-data-kontak)
3. [🏷️ Sales (Penjualan & Penawaran Harga)](#3-sales-penjualan--penawaran-harga)
4. [📊 Dashboards (Dashboard & Visualisasi Laporan)](#4-dashboards-dashboard--visualisasi-laporan)
5. [🛒 Point of Sale (POS - Sistem Kasir Retail/Resto)](#5-point-of-sale-pos---sistem-kasir-retailresto)
6. [🧾 Invoicing (Faktur & Keuangan)](#6-invoicing-faktur--keuangan)
7. [🛍️ Purchase (Pembelian & Pengadaan Barang)](#7-purchase-pembelian--pengadaan-barang)
8. [📦 Inventory (Manajemen Stok & Gudang)](#8-inventory-manajemen-stok--gudang)
9. [🧩 Apps (Pasang & Kelola Modul Odoo)](#9-apps-pasang--kelola-modul-odoo)
10. [⚙️ Settings (Pengaturan Sistem & Hak Akses User)](#10-settings-pengaturan-sistem--hak-akses-user)

---

## 1. 💬 Discuss (Obrolan & Komunikasi Internal)

### 📌 Buat Apa / Fungsi Utama:
Modul **Discuss** adalah pusat komunikasi internal antar anggota tim/karyawan di dalam Odoo. Modul ini menggantikan email internal dengan menyediakan saluran obrolan (*channels*), pesan langsung (*Direct Message*), notifikasi tugas/aktivitas, serta pengintegrasian catatan di setiap dokumen bisnis (seperti Sales Order atau Invoice).

### 🚀 Cara Pakai & Step-by-Step:
1. **Membuat Saluran Obrolan (Channel)**:
   - Masuk ke modul **Discuss**.
   - Di panel kiri pada bagian **Channels**, klik ikon **`+`**.
   - Ketik nama saluran (misal: `#penjualan`, `#gudang-operasional`). Pilih status *Public* (semua staf bisa gabung) atau *Private* (hanya staf yang diundang).
2. **Kirim Pesan Langsung (Direct Message)**:
   - Di panel kiri bagian **Direct Messages**, klik ikon **`+`**.
   - Cari nama rekan kerja/pengguna Odoo lain, lalu mulai obrolan pribadi.
3. **Menggunakan Fitur Mention (`@`) & Chatter**:
   - Di dalam saluran atau pesan, ketik `@nama_rekan` untuk memberikan notifikasi khusus kepada rekan kerja.
   - Di setiap dokumen Odoo (seperti SO/PO/Invoice), terdapat bagian bawah yang disebut **Chatter**. Anda bisa mengetik catatan (*Log note*) atau mention rekan di sana agar riwayat komunikasi tersimpan rapi pada dokumen tersebut.

---

## 2. 👥 Contacts (Buku Alamat & Manajemen Data Kontak)

### 📌 Buat Apa / Fungsi Utama:
Modul **Contacts** berfungsi sebagai direktori terpusat untuk menyimpan seluruh data entitas luar maupun dalam perusahaan, termasuk **Pelanggan (Customers)**, **Pemasok (Vendors)**, **Mitra Bisnis**, hingga **Kontak Karyawan**.

### 🚀 Cara Pakai & Step-by-Step:
1. **Menambahkan Kontak Baru**:
   - Buka modul **Contacts** $\rightarrow$ Klik tombol **Create / Buat**.
2. **Isi Detail Data Kontak**:
   - Pilih jenis kontak: **Individual** (Orang) atau **Company** (Perusahaan).
   - Isi Nama, Alamat Lengkap, Nomor Telepon/WhatsApp, Email, dan NPWP.
3. **Tentukan Peran Bisnis (Tab Sales & Purchase)**:
   - Pada tab *Sales & Purchase*, Anda dapat menentukan syarat pembayaran (*Payment Terms*) default, Salesperson penanggung jawab, serta status sebagai Customer atau Vendor.
4. **Hubungkan Kontak Anak (Child Contacts)**:
   - Jika kontak berupa Perusahaan (PT/CV), Anda bisa menambahkan kontak individu (PIC) seperti Manajer Keuangan atau PIC Gudang di bagian *Contacts & Addresses*.
5. **Klik Save**: Data kontak siap digunakan otomatis di modul Sales, Purchase, Invoicing, dan POS.

---

## 3. 🏷️ Sales (Penjualan & Penawaran Harga)

### 📌 Buat Apa / Fungsi Utama:
Modul **Sales** digunakan untuk mengelola alur transaksi penjualan B2B atau B2C berskala besar, mulai dari pembuatan penawaran harga (*Quotation*), pengiriman penawaran ke pelanggan, konfirmasi pesanan (*Sales Order*), hingga pemicuan pengiriman barang dan pembuatan faktur.

### 🚀 Cara Pakai & Step-by-Step:
1. **Membuat Quotation (Penawaran Harga)**:
   - Buka modul **Sales** $\rightarrow$ Klik **Create / Buat**.
   - Pilih nama **Customer** dari database kontak.
   - Tentukan tanggal penawaran dan *Payment Terms* (misal: Immediate Payment, 30 Days).
2. **Menambahkan Produk yang Dijual**:
   - Pada tab **Order Lines**, klik *Add a product*.
   - Pilih produk, tentukan Jumlah (*Quantity*), Harga Satuan (*Unit Price*), dan Pajak (misal: PPN 11%).
3. **Kirim Penawaran ke Pelanggan**:
   - Klik tombol **Send by Email** untuk mengirim dokumen PDF penawaran secara langsung via sistem, atau klik **Print Quotation** untuk mengunduh PDF.
4. **Konfirmasi Pesanan menjadi Sales Order (SO)**:
   - Setelah pelanggan menyetujui penawaran, klik tombol **Confirm**.
   - Status dokumen akan berubah dari *Quotation* menjadi **Sales Order**.
5. **Alur Lanjutan (Smart Buttons)**:
   - Di pojok kanan atas akan muncul tombol pintas (*Smart Button*):
     - **Delivery**: Mengarahkan ke modul Inventory untuk memproses pengiriman barang.
     - **Create Invoice**: Untuk membuat faktur tagihan ke pelanggan di modul Invoicing.

---

## 4. 📊 Dashboards (Dashboard & Visualisasi Laporan)

### 📌 Buat Apa / Fungsi Utama:
Modul **Dashboards** menyediakan tampilan visual *real-time* berupa grafik, diagram, dan angka statistik kunci (KPI) dari seluruh aktivitas bisnis perusahaan (Penjualan, Keuangan, Stok, Kasir).

### 🚀 Cara Pakai & Step-by-Step:
1. **Melihat Ringkasan Performa**:
   - Buka modul **Dashboards**.
   - Pilih tab dashboard yang ingin dilihat (misal: *Sales Dashboard*, *Inventory Dashboard*).
2. **Kustomisasi & Filter Data**:
   - Gunakan bilah pencarian dan *Filter* di bagian atas untuk menyaring data berdasarkan rentang waktu (bulan ini, kuartal ini) atau berdasarkan tim sales/kategori produk.
3. **Menambahkan Grafik Baru ke Dashboard**:
   - Buka modul apa saja (misal: Sales atau Invoicing), tampilkan data dalam format **Graph View** atau **Pivot View**.
   - Klik menu **Favorites** di dekat bilah pencarian $\rightarrow$ Pilih **Add to my Dashboard**.
   - Buka kembali modul Dashboards untuk melihat grafik baru tersebut.

---

## 5. 🛒 Point of Sale (POS - Sistem Kasir Retail/Resto)

### 📌 Buat Apa / Fungsi Utama:
Modul **Point of Sale (POS)** adalah aplikasi kasir berbasis web/touchscreen yang dirancang untuk transaksi tatap muka cepat di toko fisik, toko retail, atau restoran. POS tetap dapat bekerja saat koneksi internet terputus (*offline-capable*) dan langsung memotong stok di modul Inventory saat transaksi selesai.

### 🚀 Cara Pakai & Step-by-Step:
1. **Membuka Sesi Kasir (Opening Session)**:
   - Buka modul **Point of Sale** $\rightarrow$ Klik **New Session** pada mesin kasir Anda.
   - Masukkan **Opening Cash** (Modal uang tunai awal di laci kasir) $\rightarrow$ Klik **Open Session**.
2. **Memproses Transaksi Kasir**:
   - Layar kasir akan menampilkan katalog produk. Klik pada produk yang dibeli pelanggan (atau gunakan barcode scanner).
   - Atur kuantitas (*Qty*), Diskon (*Disc*), atau Harga (*Price*) jika diperlukan.
   - Klik **Customer** jika ingin mencatat nama pelanggan (opsional).
3. **Pembayaran (Payment)**:
   - Klik tombol hijau **Payment**.
   - Pilih Metode Pembayaran (Tunai / Cash, Bank Transfer, QRIS, Kartu Kredit).
   - Masukkan jumlah uang tunai yang diterima (sistem akan otomatis menghitung kembalian).
   - Klik **Validate**.
4. **Cetak Struk & Transaksi Baru**:
   - Cetak struk/nota kasir $\rightarrow$ Klik **New Order** untuk melayani pelanggan berikutnya.
5. **Menutup Sesi Kasir di Akhir Hari (Close Session)**:
   - Klik tombol **Close** di pojok kanan atas layar kasir.
   - Hitung total uang tunai fisik di laci kasir dan masukkan ke kolom *Counted Cash*.
   - Klik **Close Session & Post Entries** untuk membukukan penjualan harian ke akuntansi dan stok.

---

## 6. 🧾 Invoicing (Faktur & Keuangan)

### 📌 Buat Apa / Fungsi Utama:
Modul **Invoicing** mengelola siklus piutang pelanggan (*Accounts Receivable*) dan utang usaha (*Accounts Payable*). Modul ini menangani penerbitan faktur penjualan (*Customer Invoices*), penerimaan faktur dari pemasok (*Vendor Bills*), serta pencatatan status pelunasan/pembayaran.

### 🚀 Cara Pakai & Step-by-Step:

#### A. Memproses Faktur Penjualan (Customer Invoice):
1. Buka menu **Customers $\rightarrow$ Invoices** $\rightarrow$ Klik **Create** (atau buat dari tombol *Create Invoice* di modul Sales).
2. Isi nama Customer, tanggal faktur (*Invoice Date*), dan produk yang ditagihkan.
3. Klik **Confirm** $\rightarrow$ Faktur mendapat nomor resmi (misal: `INV/2026/00001`) dan tercatat di pembukuan.
4. Kirim faktur ke pelanggan via email atau cetak PDF.
5. **Mencatat Pembayaran**: Saat uang masuk, klik tombol **Register Payment** $\rightarrow$ Pilih rekening Bank/Kas $\rightarrow$ Klik *Create Payment*. Status faktur berubah menjadi **Paid** (Lunas).

#### B. Memproses Tagihan Pembelian (Vendor Bill):
1. Buka menu **Vendors $\rightarrow$ Bills** $\rightarrow$ Klik **Create** (atau dari tombol *Create Bill* di modul Purchase).
2. Pilih nama Vendor dan isi nomor faktur fisik asli dari vendor (*Bill Reference*).
3. Masukkan item barang/jasa yang dibeli $\rightarrow$ Klik **Confirm**.
4. **Mencatat Pelunasan Utang**: Klik **Register Payment** saat Anda sudah mentransfer uang ke vendor.

---

## 7. 🛍️ Purchase (Pembelian & Pengadaan Barang)

### 📌 Buat Apa / Fungsi Utama:
Modul **Purchase** digunakan oleh bagian pengadaan (*Procurement/Purchasing*) untuk mengelola pembelian barang/jasa dari vendor. Alurnya dimulai dari *Request for Quotation* (RFQ) hingga menjadi *Purchase Order* (PO) resmi.

### 🚀 Cara Pakai & Step-by-Step:
1. **Membuat RFQ (Permintaan Penawaran Harga ke Vendor)**:
   - Buka modul **Purchase** $\rightarrow$ Klik **Create**.
   - Pilih **Vendor** tempat Anda ingin membeli barang.
   - Pada tab *Products*, klik *Add a product*, pilih nama barang, isi jumlah kuantitas (*Quantity*), dan estimasi harga beli.
2. **Kirim RFQ ke Vendor**:
   - Klik **Send by Email** untuk mengirim dokumen RFQ ke vendor.
3. **Konfirmasi Pembelian menjadi Purchase Order (PO)**:
   - Setelah kesepakatan harga dan persetujuan vendor, klik tombol **Confirm Order**.
   - Dokumen berubah status menjadi **Purchase Order (PO)**.
4. **Penerimaan Barang & Tagihan Vendor**:
   - Muncul tombol pintas di kanan atas:
     - **Receipt**: Klik tombol ini jika barang fisik telah sampai di gudang untuk diverifikasi oleh staf gudang di modul Inventory.
     - **Create Bill**: Klik tombol ini untuk menerbitkan tagihan pembayaran di modul Invoicing.

---

## 8. 📦 Inventory (Manajemen Stok & Gudang)

### 📌 Buat Apa / Fungsi Utama:
Modul **Inventory** adalah jantung operasional fisik perusahaan. Modul ini melacak kuantitas stok barang di gudang, mengelola transaksi barang masuk (*Receipts*), barang keluar (*Delivery Orders*), transfer antar lokasi/gudang, hingga penyesuaian stok opname (*Physical Inventory*).

### 🚀 Cara Pakai & Step-by-Step:

#### A. Penerimaan Barang Masuk (Receipts):
1. Buka modul **Inventory** $\rightarrow$ Pada kartu **Receipts**, klik *X To Process* (atau akses dari tombol *Receipt* di PO).
2. Pilih dokumen penerimaan yang sesuai.
3. Verifikasi jumlah fisik barang yang diterima di kolom **Done**.
4. Klik **Validate**. Stok barang di gudang akan otomatis bertambah.

#### B. Pengiriman Barang Keluar (Delivery Orders):
1. Buka modul **Inventory** $\rightarrow$ Pada kartu **Delivery Orders**, klik *X To Process* (atau akses dari tombol *Delivery* di SO).
2. Sistem akan mengecek ketersediaan stok (*Check Availability*).
3. Isi kuantitas barang yang siap dikirim pada kolom **Done**.
4. Klik **Validate**. Stok barang di gudang akan otomatis berkurang.

#### C. Stok Opname / Penyesuaian Stok (Stock Adjustment):
1. Buka menu **Operations $\rightarrow$ Physical Inventory**.
2. Cari produk yang ingin disesuaikan.
3. Isi kuantitas fisik riil hasil hitungan di lapangan pada kolom **Counted Quantity**.
4. Klik **Apply**. Sistem akan otomatis menyesuaikan catatan stok dengan kondisi fisik.

---

## 9. 🧩 Apps (Pasang & Kelola Modul Odoo)

### 📌 Buat Apa / Fungsi Utama:
Modul **Apps** adalah direktori/marketplace internal Odoo untuk memasang (*Install/Activate*), memperbarui, atau menghapus aplikasi dan modul tambahan (baik modul resmi bawaan Odoo maupun *Custom Addons* buatan tim pengembang Anda).

### 🚀 Cara Pakai & Step-by-Step:
1. **Mencari Modul**:
   - Buka modul **Apps** (Wajib masuk sebagai pengguna dengan akses Administrator).
   - Di bilah pencarian atas, secara bawaan terdapat filter `Apps`. Jika ingin mencari modul teknis/ekstra, hapus filter tersebut dengan mengklik tanda `x`.
   - Ketik nama modul yang ingin dicari (misal: `CRM`, `Project`, `eCommerce`, atau nama *custom addon*).
2. **Mengaktifkan / Memasang Modul**:
   - Klik tombol **Activate** pada kartu modul yang dipilih.
   - Tunggu beberapa detik hingga proses instalasi selesai. Setelah selesai, modul baru akan muncul di menu utama Odoo.
3. **Pembaruan Modul Kustom (Update Apps List)**:
   - Jika Anda atau pengembang mengunggah folder *custom addons* baru ke server VPS, aktifkan *Developer Mode* terlebih dahulu.
   - Buka modul **Apps** $\rightarrow$ Klik menu atas **Update Apps List** $\rightarrow$ Klik **Update**.
   - Cari modul baru Anda lalu klik **Activate**.

---

## 10. ⚙️ Settings (Pengaturan Sistem & Hak Akses User)

### 📌 Buat Apa / Fungsi Utama:
Modul **Settings** adalah pusat kontrol administrasi seluruh sistem Odoo. Digunakan untuk mengonfigurasi profil perusahaan, mengelola akun pengguna (*Users*) dan grup hak akses (*Access Rights*), pengaturan mata uang (IDR), format laporan, hingga mengaktifkan fitur pengembang (*Developer Mode*).

### 🚀 Cara Pakai & Step-by-Step:

#### A. Mengelola Pengguna & Hak Akses (Users & Access Rights):
1. Buka modul **Settings** $\rightarrow$ Pilih menu **Users & Companies $\rightarrow$ Users**.
2. Klik tombol **Create** untuk membuat pengguna/karyawan baru.
3. Isi Nama Karyawan dan Email (digunakan untuk login).
4. Atur **Access Rights** (Hak Akses) untuk setiap modul:
   - Misal: Untuk staf kasir, set modul *Point of Sale* ke `User`, sedangkan modul *Invoicing* dan *Settings* diset ke `Blank` (Kosong) agar mereka tidak bisa mengakses laporan keuangan.
5. Klik **Save**. Pengguna akan menerima email aktivasi atau Anda dapat menetapkan kata sandi secara manual via tombol *Action $\rightarrow$ Change Password*.

#### B. Mengatur Profil Perusahaan:
1. Buka modul **Settings** $\rightarrow$ Pada bagian **General Settings**, pilih **Update Info** di bawah nama perusahaan.
2. Unggah Logo Perusahaan, isi Alamat, No Telepon, Email, Website, dan NPWP Perusahaan (Tax ID).
3. Klik **Save**. Data ini akan otomatis tampil di kop faktur, invoice PDF, dan penawaran harga.

#### C. Mengaktifkan Developer Mode (Mode Pengembang):
1. Buka modul **Settings**.
2. Gulir layar (*scroll*) sampai ke bagian paling bawah.
3. Klik tautan **Activate the developer mode**.
4. Ikon kumbang (*bug icon*) akan muncul di pojok kanan atas navigasi Odoo. Mode ini memungkinkan Anda melihat nama teknis *field*, merestart modul, dan mengonfigurasi fitur-fitur teknis tingkat lanjut.

---

> 💡 **Tip Integrasi AI Hermes Agent**:
> Semua aktivitas di modul **Inventory** (stok), **Sales** (omset), dan **Contacts/CRM** (lead) dapat ditanyakan langsung atau diinput melalui **Hermes Agent** via Telegram tanpa perlu membuka menu Odoo secara manual.
