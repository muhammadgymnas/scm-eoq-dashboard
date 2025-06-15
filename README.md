# 📦 Analisis Biaya Persediaan (EOQ Dashboard)
Aplikasi web interaktif yang dibangun menggunakan Streamlit untuk menganalisis dan memvisualisasikan model Economic Order Quantity (EOQ) dalam manajemen rantai pasok (Supply Chain Management). Aplikasi ini bertujuan untuk membantu pengguna, baik mahasiswa maupun praktisi, dalam memahami cara mengoptimalkan biaya persediaan dengan menentukan kuantitas pesanan yang paling ekonomis.


(Ganti link gambar dan link aplikasi di atas dengan milik Anda)

✨ Fitur Utama
Kalkulator EOQ Interaktif: Menghitung Ukuran Pesanan Optimal (Q*), Reorder Point (R), dan Siklus Waktu (T) secara dinamis berdasarkan input pengguna.

Analisis Biaya Komprehensif: Memberikan rincian Ongkos Pembelian (OB), Ongkos Pemesanan (OP), Ongkos Penyimpanan (OS), dan Total Ongkos (OT).

Visualisasi Data Dinamis: Grafik interaktif (dibuat dengan Plotly) untuk menampilkan:

Kurva Biaya Pemesanan vs. Biaya Penyimpanan untuk menemukan titik optimal.

Komposisi total biaya dalam bentuk diagram lingkaran (pie chart).

Analisis Sensitivitas: Memungkinkan pengguna untuk melihat dampak perubahan parameter kunci (seperti permintaan atau biaya) terhadap kuantitas pesanan optimal dan total biaya.

Panduan & Teori Terintegrasi: Dilengkapi dengan tab khusus yang berisi tutorial penggunaan aplikasi dan penjelasan singkat mengenai teori EOQ yang mendasarinya.

Tema Ganda: Pilihan antara mode terang (Light Mode) dan gelap (Dark Mode) untuk kenyamanan visual.

🛠️ Teknologi yang Digunakan
Bahasa: Python

Framework: Streamlit

Library: Pandas, NumPy, Plotly

🚀 Cara Menggunakan
Buka aplikasi melalui link.

Pada sidebar kiri, masukkan semua parameter dasar yang dibutuhkan:

D: Permintaan Tahunan

C: Harga Beli per Unit

A: Ongkos Tetap per Pemesanan

h: Ongkos Penyimpanan per Unit per Tahun

L: Lead Time (dalam tahun)

Jelajahi hasil perhitungan dan visualisasi pada setiap tab yang tersedia.

Gunakan Tab Analisis Sensitivitas untuk memahami dampak perubahan variabel.

Lihat Tab Panduan & Teori jika memerlukan penjelasan lebih lanjut.
