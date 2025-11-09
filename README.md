# 🗃️ TikTok Shop Scraping Project Documentation

> Panduan untuk scraping TikTok Shop dengan Appium dan AWS.

---

## 📑 Table of Contents
- [🗃️ TikTok Shop Scraping Project Documentation](#️-tiktok-shop-scraping-project-documentation)
  - [📑 Table of Contents](#-table-of-contents)
  - [⚙️ Persiapan Awal](#️-persiapan-awal)
    - [👥 Untuk Staf yg Scrape TikTokShop](#-untuk-staf-yg-scrape-tiktokshop)
    - [👩‍💻 Tambahan khusus PIC TikTokShop](#-tambahan-khusus-pic-tiktokshop)
  - [🗂️ Struktur Directory](#️-struktur-directory)
  - [🧩 Penjelasan Program](#-penjelasan-program)
    - [☁️ Running on AWS (Folder `io_tools.AWS_DIR`)](#️-running-on-aws-folder-io_toolsaws_dir)
    - [📘 Library (Folder `io_tools.TOOLKIT_DIR`)](#-library-folder-io_toolstoolkit_dir)
    - [🤖 Appium Automation (Folder `io_tools.SCRIPT_DIR`)](#-appium-automation-folder-io_toolsscript_dir)
    - [🧾 Data Processing](#-data-processing)
    - [🌩️ For Interacting with AWS](#️-for-interacting-with-aws)
    - [📂 Archive Scripts (Folder `io_tools.ARCHIVE_DIR`)](#-archive-scripts-folder-io_toolsarchive_dir)
    - [▶️ Sebelum Menjalankan `appium_*.py`](#️-sebelum-menjalankan-appium_py)
  - [🔌 Cara Connect Smartphone ke PC](#-cara-connect-smartphone-ke-pc)
    - [🔗 Via USB](#-via-usb)
    - [📡 Via WiFi](#-via-wifi)
  - [🧠 Cara Pakai Appium Inspector](#-cara-pakai-appium-inspector)
  - [🛰️ Cara Upload Layers](#️-cara-upload-layers)
    - [🧪 Untuk Library Eksternal](#-untuk-library-eksternal)
    - [🧬 Untuk Library Buatan Sendiri](#-untuk-library-buatan-sendiri)
    - [🚀 Upload Layer ke AWS Lambda via console](#-upload-layer-ke-aws-lambda-via-console)
      - [📤 Upload Pertama](#-upload-pertama)
      - [🔄 Update Layer yang Sudah Ada](#-update-layer-yang-sudah-ada)
  - [💥 Info Penting](#-info-penting)
    - [🛠️ Operasional dan Penggunaan](#️-operasional-dan-penggunaan)
    - [💣 Kendala Umum \& Solusi](#-kendala-umum--solusi)
    - [🌐 Jenis URL Produk](#-jenis-url-produk)
    - [🕒 Jadwal Otomatis](#-jadwal-otomatis)
    - [🤝 Workflow Scraping Seller (Multi-Device)](#-workflow-scraping-seller-multi-device)
    - [💾 Catatan Tambahan](#-catatan-tambahan)
    - [💡 Suggestion for Improvements](#-suggestion-for-improvements)

---

## ⚙️ Persiapan Awal

### 👥 Untuk Staf yg Scrape TikTokShop
1. Smartphone dengan TikTok & TikTokShop (Android ≥ 8.2)
2. Kabel data & PC
3. Nonaktifkan layar kunci, aktifkan Developer Mode & USB Debugging (beberapa butuh aktifkan Wireless ADB)
4. Set bahasa TikTok ke **Bahasa Indonesia**
5. Install:
   - Python & Selenium  
   - JDK, Node.js, npm, adb  
   - Appium server → `npm install -g appium`  
   - Appium Inspector  
   - Appium-Python-Client → `pip install Appium-Python-Client`  
   - UiAutomator2 → `appium driver install uiautomator2`  
   - Appium gesture plugin → `appium plugin install --source=npm appium-gestures-plugin`  
   - boto3  
   - easyocr (khusus scraping data seller)
6. Tambahkan Android SDK & adb ke `PATH`
7. Pull repo dan buat file baru di `io_tools.COMMAND_DIR` & `io_tools.CONFIG_DIR` untuk masing-masing staf
8. IAM User (dibuatkan pic)
---

### 👩‍💻 Tambahan khusus PIC TikTokShop

Selain langkah di atas:
1. Buat akun **AWS Admin**
2. Setup pipeline (SQS, Lambda, EventBridge Schedules, DynamoDB)
3. Buat **IAM roles, permissions, & IAM User** untuk setiap staf scraper

---

## 🗂️ Struktur Directory

| Folder                 | Deskripsi                                                           |
| ---------------------- | ------------------------------------------------------------------- |
| `io_tools.ARCHIVE_DIR` | Arsip file lama (mungkin masih terpakai)                            |
| `io_tools.AWS_DIR`     | Fungsi Lambda, & Layer-nya utk di-run di AWS, sekalian template-nya |
| `io_tools.COMMAND_DIR` | Perintah terminal biar gampang copy paste                           |
| `io_tools.CONFIG_DIR`  | Konfigurasi per device                                              |
| `io_tools.DATA_DIR`    | Data input & output                                                 |
| `io_tools.IMAGE_DIR`   | Gambar                                                              |
| `io_tools.SCRIPT_DIR`  | Script Python eksekusi                                              |
| `io_tools.TOOLKIT_DIR` | Library internal project                                            |

---

## 🧩 Penjelasan Program

> Berikut daftar script utama beserta fungsi dan alur kerjanya.  

---

### ☁️ Running on AWS (Folder `io_tools.AWS_DIR`)
- **`lambda/polling-sqs*.zip`** → Fungsi untuk *scrape* detail produk. Hanya berjalan di AWS Lambda (disimpan lokal sebagai backup).
- **`detail_scraper/python/detail_scraper.py`** → Library utama *scraping* detail produk, diunggah sebagai Lambda Layer agar dapat dipanggil di AWS.

---

### 📘 Library (Folder `io_tools.TOOLKIT_DIR`)
- **`appium_tools.py`** → Berisi fungsi umum untuk kontrol otomatis smartphone via Appium (misalnya gesture, tap, scroll, cek element).
- **`aws_tools.py`** → Berisi fungsi & variabel umum untuk berinteraksi dengan pipeline AWS (SQS, Lambda, DynamoDB, EventBridge).
- **`io_tools.py`** → Menangani akses direktori, input/output file, dan penyimpanan data.

---

### 🤖 Appium Automation (Folder `io_tools.SCRIPT_DIR`)
- **`appium_keyword_search.py`** → Crawling URL produk berdasarkan keyword pencarian di TikTok Shop.
  - search keyword yg diinginkan.
  - setelah hasil pencarian muncul, bisa urutkan produk sesuai harga/lainnya.
  - scroll down sedikit sampai tab filter hilang & setidaknya kotak keterangan produk ke-3 & 4 terlihat penuh di layar.
  - run (atau bisa scroll ke bawah lagi)
- **`appium_image_search.py`** → Crawling berdasarkan gambar mirip dari suatu produk.
  - Tap ikon kamera di pojok kanan bawah foto produk pada hasil pencarian produk.
  - Jika tidak ada ikon kamera, tab produk, tap gambar produk pada halaman produk.
  - lalu swipe ke samping untuk memilih gambar yg diinginkan, bebas pilih asal sesuai keyword.
  - Tap “Temukan produk serupa” di TikTok Shop.
  - setelah hasil pencarian muncul, di bagian atas ada pilihan potongan gambar bagian mana yg mau dicari produk yg mirip, bebas pilih asal sesuai keyword, bisa juga diurutkan sesuai harga/lainnya.
  - scroll down sedikit sampai tab pengurutan berada di atas & setidaknya kotak keterangan produk ke-3 & 4 terlihat penuh di layar.
  - run (atau bisa scroll ke bawah lagi)
- **`appium_seller_data_scraper.py`** → Scraping *seller location* & *seller type (badge)*.
  - Input: `SELLER_DATA`
  - Output: `UPDATED_SELLER_DATA` per device.
  - Seller yang gagal di-*scrape* diberi kolom `failure_reason` agar bisa diulang lain waktu.
  Sebaiknya buka tiktok dulu sebelum mulai supaya lebih cepat.

---

### 🧾 Data Processing
- **`detail_scraper_tester.py`** → Testing library `detail_scraper.py` langsung dari PC.
  - Berguna untuk debug AWS Lambda layer.
  - Tidak direkomendasikan untuk scraping karena rawan *block*.
- **`data_downloader.py`** → Mengunduh hasil scraping dari DynamoDB ke lokal.
  - Menghasilkan dua output:
    - `PRODUCT_DATA` → Data produk hasil scraping (belum lengkap).
    - `SELLER_DATA` → Data seller tanpa duplikasi, siap untuk disebar ke staf lain.
  - Sekaligus menjalankan `progress_reporter.py`.
- **`progress_reporter.py`** → Membuat laporan JSON `PROGRESS_REPORT` berisi jumlah produk, seller, keyword, dll.  
  Dapat dijalankan manual atau otomatis saat `data_downloader.py` berjalan.
- **`seller_data_merger.py`** → Menggabungkan hasil scraping data seller dari beberapa device.  
  - Input: `UPDATED_SELLER_DATA` per device.
  - Output: `SELLER_DATA`
  Dapat digunakan juga untuk mengganti *device assignment*.
- **`data_final_combiner.py`** → Menggabungkan hasil scraping produk (`PRODUCT_DATA`) dan data seller (`SELLER_DATA`) yang sudah lengkap menjadi `FINAL_DATA`.
- **`parquet_converter.py`** → Mengubah file parquet menjadi CSV/Excel.

---

### 🌩️ For Interacting with AWS
- **`return_failed_urls.py`** → Mengembalikan URL gagal dari Dead Letter Queue (DLQ) ke SQS utama agar bisa diproses ulang.
- **`create_or_truncate_table.py`** → Membuat atau mengosongkan tabel DynamoDB berdasarkan konfigurasi di `aws_tools`.

---

### 📂 Archive Scripts (Folder `io_tools.ARCHIVE_DIR`)
> Skrip lama yang masih disimpan untuk referensi atau debugging.

- **`appium_manual_crawl.py`** → Crawl manual URL produk (untuk debugging). cukup tap share link, otomatis tersimpan.
- **`from_pc_category.py`** → Scraping berbasis kategori dari PC (sudah tidak dipakai karena terbatas 1000 produk).
- **`from_pc_recursive_crawl.py`** → Crawling rekursif berdasarkan produk terkait (tidak dipakai karena hasil makin tidak relevan).
- **`keyword_extractor.py`** → Lambda Layer lama untuk ekstraksi keyword produk (fungsi kini digabung ke `detail_scraper.py`).
- **`selenium_product_details.py`** → Versi lama scraper berbasis Selenium, dibuat saat HTML TikTokShop sempat berubah.
- **`semi_manual_data_cleaner.py`** → Pembersihan semi-manual kolom keyword. Sekarang ditangani oleh divisi BI.

---

### ▶️ Sebelum Menjalankan `appium_*.py`

Pastikan semua langkah berikut sudah dilakukan sebelum menjalankan program Appium automation:

1. **Hubungkan** smartphone Android dan PC via USB atau WiFi.  
2. **Cek koneksi device** di terminal:  
   ```bash
   adb devices
   ```
   Pastikan device muncul dan statusnya tidak offline.
3. Jalankan Appium server dengan gesture plugin aktif di terminal lain:
   ```bash
   appium --use-plugins=gestures
   ```
4. Buka aplikasi TikTokShop di smartphone  
5. Pastikan tidak sedang menggunakan Appium Inspector (karena akan mengganggu koneksi)  
6. Di terminal pertama, jalankan program untuk mulai crawl URL produk

---

## 🔌 Cara Connect Smartphone ke PC

### 🔗 Via USB
1. Pastikan Developer Mode & USB Debugging aktif.  
2. Hubungkan kabel USB

### 📡 Via WiFi
1. Pastikan PC & smartphone di jaringan WiFi yang sama.  
2. Mungkin perlu switch device ke wireless debungging mode dulu, tapi perlu disambung via USB dulu, lalu jalankan:
   ```bash
   adb tcpip 5555
   ```
   selanjutnya bisa disconnect USB
3. Hubungkan PC & smartphone menggunakan ip address smartphone, contoh:
   ```bash
   adb connect 192.168.100.81
   ```
---

## 🧠 Cara Pakai Appium Inspector

1. Pastikan device sudah terhubung  
2. Jalankan Appium server dengan port sesuai config (`staff_name.yaml`).  
3. BUat desired capabilities berikut:
   ```json
   {
     "platformName": "Android",
     "appium:automationName": "UiAutomator2",
     "appium:noReset": true,
     "appium:disableIdLocatorAutocompletion": true
   }
   ```
4. Save dengan nama terserah anda.
5. Gunakan *desired capability* di atas bila sudah tersimpan.
6. sesuaikan remote port dgn device yg dipakai
7. Start session (tunggu agak lama)
8. kalau direfresh ga bisa/error waktu klik/search element, biasanya karena putus koneksi, jadi perlu keluar terus Start Session lagi
---

## 🛰️ Cara Upload Layers

### 🧪 Untuk Library Eksternal
1. Buat folder `layer_name/python` di `AWS_DIR`  
2. Tambahkan `requirements.txt`  
3. Install dependensi:  
   ```bash
   pip install -r requirements.txt -t aws/tiktokshop_dependencies/python
   ```
4. Zip folder `python` → upload ke AWS Lambda Layers. folder `python` bisa dihapus kalau sudah upload

### 🧬 Untuk Library Buatan Sendiri
1. Buat folder `layer_name/python` di `AWS_DIR`  
2. Taruh file program di dalamnya  
3. Zip dan upload ke AWS

⚠️ **Catatan:** Nama folder layer_name bebas, `phyton` jangan diganti agar dapat dibaca oleh Lambda.

### 🚀 Upload Layer ke AWS Lambda via console

#### 📤 Upload Pertama
1. Buka **AWS Console**
2. Masuk ke **Lambda → Layers**
3. Klik **Create Layer**
4. Isi nama layer, lalu pilih **Upload a .zip file → Choose file**
5. Centang semua opsi **Compatible architectures**
6. Centang semua versi Python yang sesuai di bagian **Compatible runtimes**
7. Klik **Create**

#### 🔄 Update Layer yang Sudah Ada
1. Buka **AWS Console**
2. Masuk ke **Lambda → Layers**
3. Pilih layer yang ingin diperbarui (`layer_name`)
4. Klik **Create Version**
5. Tambahkan deskripsi perubahan dan pilih **Upload a .zip file → Choose file**
6. Centang semua opsi **Compatible architectures**
7. Centang semua versi Python yang sesuai di **Compatible runtimes**
8. Klik **Create**

---

## 💥 Info Penting

### 🛠️ Operasional dan Penggunaan
1. Lihat `IMAGE_DIR/tiktokshop_pipeline.png` untuk diagram pipeline lengkap.  
2. Lihat `IMAGE_DIR/appium_*_instruction.png` untuk ilustrasi koordinat, batas scroll, dan faktor pergerakan.  
3. Simpan credential akun IAM di `.env`.  
4. Buat file config berbeda di `CONFIG_DIR` untuk setiap staf (hindari nama device yang sama meski beda staff).  
5. Buat file terminal_commands berbeda di `COMMAND_DIR` untuk setiap staf (run dari direktori Tiktokshop)
6. Emulator tidak bisa dipakai karena terdeteksi bot (banyak captcha & program tidak bisa bypass).  
7. **Staf selain PIC hanya perlu menjalankan program `appium_*.py` saja.**

### 💣 Kendala Umum & Solusi
- Program `appium_*.py` kadang crash karena faktor Appium, jaringan, kabel data, atau overheat device.  
  **Solusi cepat:** restart Appium server atau jeda scraping beberapa menit.
  ```bash
  adb kill-server
  adb start-server
  ```
- Pipeline AWS didesain agar setiap program bisa berjalan mandiri tanpa menunggu tahap sebelumnya selesai.
- Jika data input diperbarui saat proses berjalan, data baru akan otomatis di-*append* tanpa menghapus yang lama.

### 🌐 Jenis URL Produk
1. **short_url** → Contoh: `https://vt.tiktok.com/t/{random_chars}`  
   - Terbentuk saat menyalin link dari smartphone.  
   - Autogenerated setiap tap share link, Selalu unik meski produk sama, jadi **tidak bisa dijadikan ID.**
2. **long_url** → Contoh: `https://www.tiktok.com/view/product/{product_id}?{params}`  
   - Redirect dari short URL saat dibuka di PC.  
   - Kadang menyertakan nama produk di path url.
3. **shop_id URL** → Contoh: `https://shop-id.tiktok.com/pdp/{product_id}?{params}`  
   - Tidak digunakan di project ini, sekedar info saja.

### 🕒 Jadwal Otomatis
- EventBridge Schedules menjalankan scraping otomatis minimal setiap **1 menit**.  
- Tiap eksekusi memproses **2 URL per menit** dan hasilnya langsung di-*append* ke DynamoDB.

### 🤝 Workflow Scraping Seller (Multi-Device)
1. PIC menanyakan ke staf device yang dipakai & bobotnya (tablet 2x lebih cepat dari smartphone karena tidak perlu scroll).  
2. PIC menjalankan `data_downloader.py` → menghasilkan `SELLER_DATA` terdistribusi.  
3. Staf menjalankan `appium_seller_data_scraper.py` di device masing-masing.  
4. Staf mengirimkan hasil (`UPDATED_SELLER_DATA`) ke PIC.  
5. PIC menjalankan `seller_data_merger.py` untuk menggabungkan semuanya.  
6. Bila masih ada seller gagal di-scrape, PIC dapat memperbarui daftar device dan menjalankan ulang.

### 💾 Catatan Tambahan
- Pipeline tidak bisa digunakan bersamaan untuk >1 project karena keterbatasan scraping rate (2 URL/menit) & perlu smartphone tambahan.  
- URL di SQS Queue otomatis dihapus jika tidak diproses dalam **2 minggu.**
- Pencarian TikTokShop berbasis keyword **dibatasi jumlah hasilnya**, sehingga perlu diulang berkali-kali.
- Duplicate detection belum sempurna karena keterbatasan inspect element smartphone, hanya menggunakan judul produk, itupun terpotong tergantung layar smartphone.

### 💡 Suggestion for Improvements

1. 🔒 **Gunakan metode scraping yang lebih sulit terdeteksi (undetectable).**  
   Sistem TikTokShop memperkuat anti-bot dari waktu ke waktu.
   Dulu scraping dari pc butuh waktu agak lama untuk kena captcha, sekarang baru sebentar sudah kena.  
   Dulu dijeda 25 detik antar url aman, sekarang jeda 1 menit pun tetap kena.  
   Bahkan scraping dari cloud baru-baru ini jadi ikut sering kena block padahal sebelumnya aman.  
   Untung kalau kena block di cloud masih bisa lanjut scraping. 
   Kalau di pc program harus di-stop dulu dan sebaiknya dijeda sebelum mulai lagi.

2. 🔍 **Optimalkan deteksi duplicate.**  
   Saat ini, duplikasi hanya dicek berdasarkan *judul produk* yang terpotong di tampilan.  
   Gunakan atribut lain seperti harga, rating atau unit terjual untuk skip produk yang sudah di-crawl.  
   Implementasi *pre-filtering* di tahap crawling akan menghemat waktu dan mencegah request berulang ke produk sama.
   Bagus kalau perlu search berulang-ulang, tapi kemungkinan butuh waktu tambahan untuk mendeteksi elemen.

3. 🎥 **Tambahkan deteksi video/live produk.**  
   Setelah crawling produk yang sedang live/ada video, program menunggu lama sebelum keluar video.  
   Jika bisa mendeteksi video aktif lebih awal, proses bisa langsung *skip* dan menghemat waktu scraping.
   tapi kemungkinan butuh waktu tambahan untuk mendeteksi elemen.

4. ♻️ **Tangani URL gagal scrape secara otomatis.**  
   Sebagian besar kegagalan disebabkan *temporary block* dan akhir-akhir ini sering kena block.  
   Solusi yang disarankan:
   - Program untuk mengembalikan url ke `SQS_QUEUE_URL` dijalankan otomatis di cloud.
   - Kirim kembali URL gagal **dengan delay** (misal 1–2 jam).

---
