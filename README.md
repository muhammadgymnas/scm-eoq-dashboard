# 📦 Analisis Biaya Persediaan (EOQ Dashboard)

![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python)

Aplikasi web interaktif yang dibangun menggunakan **Streamlit** untuk menganalisis dan memvisualisasikan model **Economic Order Quantity (EOQ)** dalam manajemen rantai pasok. Aplikasi ini dirancang untuk membantu mahasiswa dan praktisi dalam memahami cara mengoptimalkan biaya persediaan dengan menentukan kuantitas pesanan yang paling ekonomis.

---

### Aplikasi Langsung

Anda bisa mencoba aplikasi ini secara langsung melalui link berikut:

**[➡️ Buka Aplikasi EOQ Dashboard](https://scm-eoq-dashboard.streamlit.app/)**

---

### 🖼️ Tampilan Aplikasi

| Mode Terang (Light Mode) | Mode Gelap (Dark Mode) |
| :---: | :---: |
| ![Light Mode Screenshot](https://ibb.co/ynLjMhtK) | ![Dark Mode Screenshot](https://ibb.co/fd0vLVC5) |

---

### ✨ Fitur Utama

-   **Kalkulator EOQ Interaktif**: Menghitung **Ukuran Pesanan Optimal (Q\*)**, **Reorder Point (R)**, dan **Siklus Waktu (T)** secara dinamis.
-   **Analisis Biaya Komprehensif**: Memberikan rincian **Ongkos Pembelian**, **Ongkos Pemesanan**, **Ongkos Penyimpanan**, dan **Total Ongkos** dengan uraian perhitungannya.
-   **Visualisasi Data Dinamis**: Grafik interaktif (Plotly) untuk menampilkan:
    -   Kurva Biaya untuk menemukan titik optimal EOQ.
    -   Komposisi total biaya dalam bentuk diagram lingkaran.
-   **Analisis Sensitivitas**: Memungkinkan pengguna untuk melihat dampak perubahan parameter kunci (permintaan, biaya pesan, biaya simpan) terhadap hasil.
-   **Panduan & Teori Terintegrasi**: Dilengkapi tab khusus berisi tutorial penggunaan dan penjelasan singkat teori EOQ.
-   **Tema Ganda**: Pilihan antara mode terang dan gelap untuk kenyamanan visual.
-   **Ringkasan Laporan**: Tabel ringkas parameter input dan hasil perhitungan yang mudah dibaca.

---

### 🛠️ Teknologi yang Digunakan

-   **Bahasa**: Python
-   **Framework Aplikasi**: Streamlit
-   **Library**:
    -   Pandas & NumPy untuk kalkulasi data.
    -   Plotly & Plotly Express untuk visualisasi data interaktif.

---

### ⚙️ Menjalankan Secara Lokal

Jika Anda ingin menjalankan aplikasi ini di komputer Anda sendiri, ikuti langkah-langkah berikut:

**1. Prasyarat**
-   Pastikan Anda sudah menginstal **Python 3.9** atau versi yang lebih baru.
-   Memiliki `pip` untuk menginstal library Python.

**2. Clone Repositori**
```bash
git clone https://github.com/muhammadgymnas/scm-eoq-dashboard.git
cd nama-repository

3. Buat File requirements.txt
Buat sebuah file bernama requirements.txt di dalam folder proyek Anda dan isi dengan library berikut:

streamlit
pandas
numpy
plotly

4. Instal Dependensi
Buka terminal di folder proyek Anda dan jalankan perintah berikut:

pip install -r requirements.txt

5. Jalankan Aplikasi Streamlit
Setelah instalasi selesai, jalankan aplikasi dengan perintah:

streamlit run GUI_SupplyChain_Test.py

Aplikasi akan otomatis terbuka di browser Anda.
