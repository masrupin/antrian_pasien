![alt text](https://github.com/masrupin/antrian_pasien/blob/main/Screenshot%202024-05-28%20184018.png?raw=true)
# Website Sistem Antrian Pasien

Proyek ini adalah aplikasi web sederhana untuk mengelola antrian pasien menggunakan Python, Flask, dan MySQL.

## Persiapan Lingkungan

Pastikan Anda sudah menginstall Python, MySQL, dan pip:

1. **Python**: Unduh dan instal Python dari [situs resmi Python](https://www.python.org/downloads/).
2. **MySQL**: Unduh dan instal MySQL dari [situs resmi MySQL](https://dev.mysql.com/downloads/installer/).
3. **pip**: Pip biasanya sudah terinstal bersama Python. Anda bisa mengeceknya dengan perintah `pip --version` di terminal atau command prompt.

## Instalasi Dependensi

Jalankan perintah berikut untuk menginstal dependensi yang diperlukan:
```bash
pip install Flask mysql-connector-python

```
## Mengatur Database

1. Buka MySQL Command Line atau gunakan MySQL Workbench.
2. Buat database bernama `queue_system` dengan menjalankan perintah berikut:
   ```sql
   CREATE DATABASE queue_system;
   ```

## Mengonfigurasi Proyek

1. **Konfigurasi Database dengan Script Python:**
   - Pastikan Anda berada di path direktori proyek Anda (`queue_system`).
   - Jalankan perintah berikut di terminal untuk mengonfigurasi database:
     ```bash
     py init_db.py
     ```

2. **Jalankan Website:**
   - Jalankan perintah berikut di terminal untuk menjalankan website:
     ```bash
     py app.py
     ```

3. **Akses Website:**
   - Buka browser Anda dan akses URL berikut:
     ```
     http://127.0.0.1:5000
     ```

## Struktur Proyek

```plaintext
queue_system/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css

```

