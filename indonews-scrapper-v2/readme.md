Tentu, ini adalah draf README.md yang komprehensif untuk program scraper berita yang telah kita buat. Anda dapat menyalin teks di bawah ini dan menyimpannya dalam file bernama README.md.

Scraper Berita Indonesia
Proyek ini adalah sebuah skrip Python yang dirancang untuk melakukan web scraping (pengambilan data) dari berbagai situs berita di Indonesia. Skrip ini secara otomatis mengumpulkan tautan artikel melalui RSS feed, kemudian mengekstrak informasi penting seperti judul, penulis, tanggal publikasi, dan isi berita dari setiap artikel.

Hasil akhir dari proses ini adalah sebuah file .csv tunggal yang berisi kumpulan data dari semua situs yang berhasil di-scrape.

Fitur Utama
Multi-Sumber: Mampu mengambil data dari 10+ situs berita populer di Indonesia.
Pengambilan Link via RSS: Secara otomatis menemukan artikel-artikel terbaru dari setiap situs menggunakan file link_scrapping.csv.
Penanganan Subdomain Cerdas: Mampu mengenali subdomain (misalnya, finance.detik.com atau news.detik.com) dan menerapkan aturan scraping dari domain utamanya (detik.com).
Paralel & Cepat: Menggunakan multi-threading untuk menjalankan beberapa proses scraping secara bersamaan, sehingga menghemat banyak waktu.
Ekstraksi Konten Terstruktur: Mengekstrak data spesifik (Judul, Penulis, Tanggal, Isi) berdasarkan CSS Selector yang telah dikonfigurasi.
Output Bersih: Menghasilkan satu file scrapping_news_{tanggal}.csv yang siap untuk dianalisis lebih lanjut.
Mudah Diperluas: Didesain agar mudah untuk menambahkan situs berita baru hanya dengan mendefinisikan selector-nya.
Prasyarat
Pastikan Anda memiliki Python 3.6 atau versi lebih baru terinstal di sistem Anda.

Instalasi
Clone atau Unduh Proyek
Unduh file skrip (scraper.py) dan file link_scrapping.csv ke dalam satu direktori yang sama di komputer Anda.

Buat File requirements.txt
Buat sebuah file baru bernama requirements.txt di direktori yang sama dan isi dengan daftar pustaka (library) berikut:

Plaintext

pandas
requests
beautifulsoup4
feedparser
tqdm
Instal Dependensi
Buka terminal atau command prompt di direktori proyek Anda, lalu jalankan perintah berikut untuk menginstal semua library yang dibutuhkan:

Bash

pip install -r requirements.txt
Cara Penggunaan
Siapkan RSS Feed
Pastikan file link_scrapping.csv berisi daftar URL RSS feed dari situs-situs berita yang ingin Anda scrape. Setiap URL harus berada di baris baru.

Contoh isi link_scrapping.csv:

Code snippet

https://rss.detik.com/index.php/detikcom
https://www.tribunnews.com/rss
https://www.republika.co.id/rss
...
Jalankan Skrip
Buka terminal atau command prompt di direktori proyek dan jalankan skrip dengan perintah:

Bash

python scraper.py
Catatan: Ganti scraper.py dengan nama file skrip Python Anda jika berbeda.

Tunggu Proses Selesai
Skrip akan menampilkan progress bar saat membaca RSS feed dan saat melakukan scraping artikel.

Membaca RSS Feeds: 100%|██████████| 10/10 [00:05<00:00,  1.82it/s]
Scraping Artikel: 100%|██████████| 520/520 [01:30<00:00,  5.78it/s]
Lihat Hasilnya
Setelah selesai, sebuah file CSV baru akan dibuat di direktori yang sama dengan nama scrapping_news_YYYY-MM-DD.csv (misalnya, scrapping_news_2025-06-18.csv).

File ini akan berisi kolom-kolom berikut:

sumber: Domain utama situs berita (misal: detik.com).
url: URL lengkap dari artikel.
judul: Judul artikel.
author: Nama penulis atau editor.
tanggal_publikasi: Tanggal artikel diterbitkan.
isi_berita: Konten lengkap dari artikel.
Cara Menambah Situs Berita Baru
Anda dapat dengan mudah menambahkan dukungan untuk situs berita lain dengan memodifikasi dictionary SELECTORS di dalam skrip scraper.py.

Dapatkan CSS Selector
Gunakan developer tools di browser Anda (biasanya dengan klik kanan -> "Inspect") untuk menemukan CSS selector untuk elemen-elemen berikut di situs berita baru:

Judul artikel
Nama penulis/author
Tanggal publikasi
Parent container dari isi berita (tag <div> atau <article> yang membungkus semua paragraf <p> dari konten).
Tambahkan ke Dictionary SELECTORS
Tambahkan entri baru ke dalam dictionary SELECTORS dengan format berikut:

Python

SELECTORS = {
    # ... selector yang sudah ada ...

    'namadomainbaru.com': {
        'judul': 'selector_css_untuk_judul',
        'author': 'selector_css_untuk_author',
        'date': 'selector_css_untuk_tanggal',
        'isi': 'selector_css_untuk_kontainer_isi'
    }
}
Tambahkan RSS Feed
Jangan lupa menambahkan URL RSS feed dari situs baru tersebut ke dalam file link_scrapping.csv.

Setelah itu, jalankan kembali skrip, dan situs baru tersebut akan ikut di-scrape.
