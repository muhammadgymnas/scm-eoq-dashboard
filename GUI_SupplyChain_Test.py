import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

# Page configuration
st.set_page_config(
    page_title="Supply Chain Management - Pengukuran Ongkos",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME SELECTION AND DYNAMIC CSS ---
st.sidebar.header("🎨 Pengaturan Tampilan")
theme = st.sidebar.radio("Pilih Tema Aplikasi:", ('Light', 'Dark'), key='theme')

def get_themed_css(theme):
    """
    Generates CSS styles based on the selected theme (Light/Dark).
    Fixes visibility for metric cards and inactive tabs.
    """
    if theme == 'Dark':
        # --- DARK MODE CSS ---
        return """
        <style>
            /* General Dark Theme */
            .stApp {
                background-color: #0E1117;
                color: #FAFAFA;
            }
            .main-header {
                font-size: 2.5rem; font-weight: bold; color: #58a6ff; text-align: center;
                margin-bottom: 2rem; padding: 1rem; background: linear-gradient(90deg, #1e2a38, #2c3e50);
                border-radius: 10px;
            }
            .sub-header {
                font-size: 1.5rem; font-weight: bold; color: #c9d1d9; margin-top: 2rem;
                margin-bottom: 1rem; padding: 0.5rem; background-color: #161b22;
                border-left: 4px solid #58a6ff; border-radius: 5px;
            }
            .metric-card {
                background: linear-gradient(135deg, #3a3f7c 0%, #4a2e5d 100%);
                color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
            .metric-card h2, .metric-card h3 {
                color: white !important;
            }
            .formula-box {
                background-color: #262730; border: 2px solid #3c4049; border-radius: 8px;
                padding: 1rem; margin: 1rem 0; font-family: 'Courier New', monospace;
                font-size: 1.1rem; color: #FAFAFA;
            }
            .warning-box {
                background-color: #4d3800; border: 1px solid #997404; border-radius: 8px;
                padding: 1rem; margin: 1rem 0; color: #ffda77;
            }
            .info-box {
                background-color: #033a4a; border: 1px solid #06607a; border-radius: 8px;
                padding: 1rem; margin: 1rem 0; color: #9eeaf9;
            }
            /* IMPROVED: Style for inactive tabs to improve contrast */
            button[data-baseweb="tab"][aria-selected="false"] {
                color: #a0a0a0 !important;
                background-color: transparent;
            }
        </style>
        """
    else:
        # --- LIGHT MODE CSS ---
        return """
        <style>
            /* General Light Theme */
            .stApp { background-color: #FFFFFF; color: #000000; }
            .main-header {
                font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center;
                margin-bottom: 2rem; padding: 1rem; background: linear-gradient(90deg, #e3f2fd, #bbdefb);
                border-radius: 10px;
            }
            .sub-header {
                font-size: 1.5rem; font-weight: bold; color: #2c3e50; margin-top: 2rem;
                margin-bottom: 1rem; padding: 0.5rem; background-color: #f8f9fa;
                border-left: 4px solid #1f77b4; border-radius: 5px;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .metric-card h2, .metric-card h3 {
                color: white !important;
            }
            .formula-box {
                background-color: #f8f9fa; border: 2px solid #dee2e6; border-radius: 8px;
                padding: 1rem; margin: 1rem 0; font-family: 'Courier New', monospace;
                font-size: 1.1rem; color: #333;
            }
            .warning-box {
                background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px;
                padding: 1rem; margin: 1rem 0; color: #856404;
            }
            .info-box {
                background-color: #d1ecf1; border: 1px solid #bee5eb; border-radius: 8px;
                padding: 1rem; margin: 1rem 0; color: #0c5460;
            }
            /* IMPROVED: Style for inactive tabs to improve contrast */
            button[data-baseweb="tab"][aria-selected="false"] {
                color: #555555 !important;
                background-color: transparent;
            }
        </style>
        """

# Inject the chosen CSS into the app
st.markdown(get_themed_css(theme), unsafe_allow_html=True)
plotly_template = 'plotly_dark' if theme == 'Dark' else 'plotly_white'

# --- END OF THEME SECTION ---


# Main title
st.markdown('<div class="main-header">📦 Supply Chain Management<br>Pengukuran Ongkos (Cost Measurement)</div>', unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("🔧 Parameter Input")
st.sidebar.markdown("---")

# Input parameters
st.sidebar.subheader("📊 Parameter Dasar")
D = st.sidebar.number_input("D - Permintaan Tahunan (unit/tahun)",
                            min_value=1, value=1000, step=1,
                            help="Total permintaan produk dalam satu tahun")

C = st.sidebar.number_input("C - Harga Beli per Unit (Rp)",
                            min_value=0.01, value=10000.0, step=100.0,
                            help="Biaya pembelian per unit produk")

A = st.sidebar.number_input("A - Ongkos Tetap per Pemesanan (Rp)",
                            min_value=0.01, value=50000.0, step=1000.0,
                            help="Biaya tetap setiap kali melakukan pemesanan")

h = st.sidebar.number_input("h - Ongkos Penyimpanan per Unit per Tahun (Rp)",
                            min_value=0.01, value=2000.0, step=100.0,
                            help="Biaya penyimpanan per unit per tahun")

L = st.sidebar.number_input("L - Lead Time (tahun)",
                            min_value=0.001, value=0.1, step=0.01, format="%.3f",
                            help="Waktu tunggu dari pemesanan hingga barang diterima. Contoh: 2 minggu = 14/365 = 0.038")

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Opsi Analisis")
show_sensitivity = st.sidebar.checkbox("Tampilkan Analisis Sensitivitas", value=True)
show_comparison = st.sidebar.checkbox("Tampilkan Perbandingan Model", value=True)

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Perhitungan Utama", "📊 Analisis Grafik", "🔍 Sensitivitas", "📋 Ringkasan", "📖 Panduan & Teori"])

# --- Calculations ---
if D > 0 and h > 0: # Avoid division by zero
    R = D * L
    Q_optimal = math.sqrt((2 * D * A) / h)
    T_optimal = Q_optimal / D if D > 0 else 0
    condition_met = L < T_optimal
    OB = D * C
    OP_optimal = (D / Q_optimal) * A if Q_optimal > 0 else 0
    OS_optimal = (Q_optimal / 2) * h
    OT_optimal = OB + OP_optimal + OS_optimal
    frequency = D / Q_optimal if Q_optimal > 0 else 0
else: # Default values if inputs are invalid
    R, Q_optimal, T_optimal, condition_met, OB, OP_optimal, OS_optimal, OT_optimal, frequency = (0,0,0,False,0,0,0,0,0)


with tab1:
    # Restored two-column layout with detailed calculations
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sub-header">🧮 Perhitungan Model Dasar</div>', unsafe_allow_html=True)
        st.markdown('<div class="formula-box">🔄 <strong>Reorder Point (R)</strong><br>R = D × L<br>R = {} × {} = <strong>{:.2f} unit</strong></div>'.format(D, L, R), unsafe_allow_html=True)
        st.markdown('<div class="formula-box">📦 <strong>Ukuran Pesanan Optimal (Q*)</strong><br>Q* = √(2DA/h)<br>Q* = √(2×{}×{}/{}) = <strong>{:.2f} unit</strong></div>'.format(D, A, h, Q_optimal), unsafe_allow_html=True)
        st.markdown('<div class="formula-box">⏰ <strong>Siklus Waktu Optimal (T)</strong><br>T = Q/D<br>T = {:.2f}/{} = <strong>{:.4f} tahun</strong></div>'.format(Q_optimal, D, T_optimal), unsafe_allow_html=True)
        if condition_met:
            st.markdown('<div class="info-box">✅ <strong>Kondisi L < T Terpenuhi</strong><br>L ({:.4f}) < T ({:.4f})<br>Model dapat digunakan dengan aman.</div>'.format(L, T_optimal), unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ <strong>Kondisi L ≥ T</strong><br>L ({:.4f}) ≥ T ({:.4f})<br>Perlu pertimbangan Safety Stock!</div>'.format(L, T_optimal), unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sub-header">💰 Analisis Biaya</div>', unsafe_allow_html=True)
        st.markdown('<div class="formula-box">🛒 <strong>Ongkos Pembelian (OB)</strong><br>OB = D × C<br>OB = {} × {} = <strong>Rp {:,.2f}</strong></div>'.format(D, C, OB), unsafe_allow_html=True)
        st.markdown('<div class="formula-box">📋 <strong>Ongkos Pemesanan (OP)</strong><br>OP = (D/Q) × A<br>OP = ({}/{:.2f}) × {} = <strong>Rp {:,.2f}</strong></div>'.format(D, Q_optimal, A, OP_optimal), unsafe_allow_html=True)
        st.markdown('<div class="formula-box">🏪 <strong>Ongkos Penyimpanan (OS)</strong><br>OS = (Q/2) × h<br>OS = ({:.2f}/2) × {} = <strong>Rp {:,.2f}</strong></div>'.format(Q_optimal, h, OS_optimal), unsafe_allow_html=True)
        st.markdown('<div class="formula-box" style="background-color: #4CAF50; color: white;">💸 <strong>Total Ongkos (OT)</strong><br>OT = OB+OP+OS<br>OT = <strong>Rp {:,.2f}</strong></div>'.format(OT_optimal), unsafe_allow_html=True)
        st.markdown('<div class="info-box">🔄 <strong>Frekuensi Pemesanan</strong><br>{:.2f} kali per tahun<br>(Setiap {:.1f} hari sekali)</div>'.format(frequency, 365/frequency if frequency > 0 else 0), unsafe_allow_html=True)

    st.markdown('<div class="sub-header">📊 Ringkasan Hasil Utama</div>', unsafe_allow_html=True)
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.markdown(f'<div class="metric-card"><h3>Q* Optimal</h3><h2>{Q_optimal:.0f} unit</h2></div>', unsafe_allow_html=True)
    m_col2.markdown(f'<div class="metric-card"><h3>Reorder Point (R)</h3><h2>{R:.0f} unit</h2></div>', unsafe_allow_html=True)
    m_col3.markdown(f'<div class="metric-card"><h3>Total Ongkos (OT)</h3><h2>Rp {OT_optimal:,.0f}</h2></div>', unsafe_allow_html=True)
    m_col4.markdown(f'<div class="metric-card"><h3>Frekuensi</h3><h2>{frequency:.1f}x / tahun</h2></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="sub-header">📊 Visualisasi Analisis Biaya</div>', unsafe_allow_html=True)
    Q_range = np.linspace(max(1, Q_optimal * 0.2), Q_optimal * 3, 100)
    OP_range = (D / Q_range) * A
    OS_range = (Q_range / 2) * h
    Total_Variable_Cost_range = OP_range + OS_range
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Q_range, y=OP_range, mode='lines', name='Ongkos Pemesanan (OP)'))
    fig.add_trace(go.Scatter(x=Q_range, y=OS_range, mode='lines', name='Ongkos Penyimpanan (OS)'))
    fig.add_trace(go.Scatter(x=Q_range, y=Total_Variable_Cost_range, mode='lines', name='Total Ongkos Variabel (OP+OS)', line=dict(width=4)))
    fig.add_vline(x=Q_optimal, line_width=2, line_dash="dash", line_color="red", annotation_text=f"Q* Optimal: {Q_optimal:.0f}")
    
    fig.update_layout(title='Kurva Biaya Variabel vs Ukuran Pesanan', xaxis_title='Ukuran Pesanan (Q)', yaxis_title='Biaya (Rp)', hovermode='x unified', template=plotly_template)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        cost_data = ['Ongkos Pembelian', 'Ongkos Pemesanan', 'Ongkos Penyimpanan']
        cost_values = [OB, OP_optimal, OS_optimal]
        fig_pie = px.pie(values=cost_values, names=cost_data, title='Komposisi Biaya Total', template=plotly_template)
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.info("""
        **Analisis Kurva Biaya:**
        - **Ongkos Pemesanan (OP)** menurun seiring Q membesar (karena makin jarang memesan).
        - **Ongkos Penyimpanan (OS)** naik seiring Q membesar (karena rata-rata stok lebih banyak).
        - **Titik Optimal (Q\*)** tercapai saat kurva OP dan OS berpotongan, menghasilkan total ongkos variabel terendah.
        """)

with tab3:
    if show_sensitivity:
        st.markdown('<div class="sub-header">🔍 Analisis Sensitivitas</div>', unsafe_allow_html=True)
        st.write("Analisis ini menunjukkan bagaimana Ukuran Pesanan Optimal (Q*) dan Total Ongkos (OT) berubah ketika salah satu parameter input diubah.")
        
        param_choice = st.selectbox("Pilih parameter untuk dianalisis:", 
                                      ["Permintaan (D)", "Ongkos Pemesanan (A)", "Ongkos Penyimpanan (h)"])

        if param_choice == "Permintaan (D)":
            D_range = np.linspace(D * 0.5, D * 2, 20)
            Q_sens = [math.sqrt((2 * d * A) / h) for d in D_range]
            OT_sens = [d * C + (d / q) * A + (q / 2) * h for d, q in zip(D_range, Q_sens)]
            x_label, title_q, title_ot = "Permintaan (D)", "Q* vs Permintaan", "Total Cost vs Permintaan"
            x_range = D_range
        
        elif param_choice == "Ongkos Pemesanan (A)":
            A_range = np.linspace(A * 0.5, A * 2, 20)
            Q_sens = [math.sqrt((2 * D * a) / h) for a in A_range]
            OT_sens = [D * C + (D / q) * a + (q / 2) * h for a, q in zip(A_range, Q_sens)]
            x_label, title_q, title_ot = "Ongkos Pemesanan (A)", "Q* vs Ongkos Pemesanan", "Total Cost vs Ongkos Pemesanan"
            x_range = A_range
            
        else:  # Ongkos Penyimpanan (h)
            h_range = np.linspace(h * 0.5, h * 2, 20)
            Q_sens = [math.sqrt((2 * D * A) / h_val) for h_val in h_range]
            OT_sens = [D * C + (D / q) * A + (q / 2) * h_val for h_val, q in zip(h_range, Q_sens)]
            x_label, title_q, title_ot = "Ongkos Penyimpanan (h)", "Q* vs Ongkos Penyimpanan", "Total Cost vs Ongkos Penyimpanan"
            x_range = h_range

        fig_sens = make_subplots(rows=1, cols=2, subplot_titles=(title_q, title_ot))
        fig_sens.add_trace(go.Scatter(x=x_range, y=Q_sens, mode='lines+markers', name='Q*'), row=1, col=1)
        fig_sens.add_trace(go.Scatter(x=x_range, y=OT_sens, mode='lines+markers', name='Total Cost'), row=1, col=2)
        fig_sens.update_xaxes(title_text=x_label, row=1, col=1)
        fig_sens.update_xaxes(title_text=x_label, row=1, col=2)
        fig_sens.update_yaxes(title_text="Q* Optimal (unit)", row=1, col=1)
        fig_sens.update_yaxes(title_text="Total Ongkos (Rp)", row=1, col=2)
        
        fig_sens.update_layout(height=400, title_text=f"Analisis Sensitivitas Terhadap {param_choice}", template=plotly_template, showlegend=False)
        st.plotly_chart(fig_sens, use_container_width=True)

    else:
        st.info("Centang 'Tampilkan Analisis Sensitivitas' di sidebar untuk melihat konten tab ini.")

with tab4:
    if show_comparison:
        st.markdown('<div class="sub-header">📋 Ringkasan Lengkap Analisis</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Parameter Input")
            comparison_data = {
                'Parameter': ['Permintaan Tahunan (D)', 'Harga Beli per Unit (C)', 'Ongkos Pemesanan (A)',
                              'Ongkos Penyimpanan (h)', 'Lead Time (L)'],
                'Nilai': [f'{D:,.0f} unit', f'Rp {C:,.2f}', f'Rp {A:,.2f}', f'Rp {h:,.2f}', f'{L:.3f} tahun']
            }
            df_params = pd.DataFrame(comparison_data)
            st.dataframe(df_params.set_index('Parameter'), use_container_width=True)
            
        with col2:
            st.subheader("📈 Hasil Perhitungan")
            hasil_data = {
                'Metrik': ['Ukuran Pesanan Optimal (Q*)', 'Reorder Point (R)', 'Siklus Waktu (T)',
                           'Frekuensi Pemesanan', 'Ongkos Pembelian (OB)', 'Ongkos Pemesanan (OP)',
                           'Ongkos Penyimpanan (OS)', 'Total Ongkos (OT)'],
                'Nilai': [f'{Q_optimal:.2f} unit', f'{R:.2f} unit', f'{T_optimal:.4f} tahun',
                          f'{frequency:.2f} kali/tahun', f'Rp {OB:,.2f}', f'Rp {OP_optimal:,.2f}',
                          f'Rp {OS_optimal:,.2f}', f'Rp {OT_optimal:,.2f}'],
                'Formula': ['√(2DA/h)', 'D×L', 'Q/D', 'D/Q', 'D×C', '(D/Q)×A', '(Q/2)×h', 'OB+OP+OS']
            }
            df_results = pd.DataFrame(hasil_data)
            st.dataframe(df_results.set_index('Metrik'), use_container_width=True)
            
        st.markdown('<div class="sub-header">💡 Interpretasi dan Rekomendasi</div>', unsafe_allow_html=True)
        if condition_met:
            st.success(f"""
            ✅ **Model Valid**: Kondisi L < T terpenuhi ({L:.4f} < {T_optimal:.4f}).
            
            📋 **Rekomendasi Operasional**:
            - Pesan sebanyak **{Q_optimal:.0f} unit** setiap kali pemesanan.
            - Lakukan pemesanan ketika stok mencapai **{R:.0f} unit** (Reorder Point).
            - Frekuensi pemesanan: **{frequency:.1f} kali per tahun** (setiap **{365/frequency:.0f} hari**).
            - Total biaya tahunan yang diharapkan: **Rp {OT_optimal:,.0f}**.
            """)
        else:
            st.warning(f"""
            ⚠️ **Perhatian**: Lead Time ({L:.4f} tahun) ≥ Siklus Waktu ({T_optimal:.4f} tahun).
            
            🛡️ **Rekomendasi**:
            - Pertimbangkan menambah Safety Stock untuk menghindari kehabisan stok.
            - Evaluasi supplier untuk mencoba mengurangi Lead Time.
            - Monitor tingkat layanan dan risiko stockout dengan lebih ketat.
            """)
    else:
        st.info("Centang 'Tampilkan Perbandingan Model' di sidebar untuk melihat konten tab ini.")
        
with tab5:
    st.markdown('<div class="sub-header">📖 Panduan Penggunaan & Analisis Teori</div>', unsafe_allow_html=True)

    with st.expander("▶️ **Cara Penggunaan Aplikasi (Tutorial)**", expanded=True):
        st.markdown("""
        Aplikasi ini dirancang untuk menghitung ukuran pemesanan optimal dan biaya terkait dalam manajemen persediaan menggunakan model Economic Order Quantity (EOQ).

        **Langkah 1: Input Parameter di Sidebar (Bagian Kiri)**
        1.  **Pengaturan Tampilan**: Pilih tema `Light` atau `Dark`.
        2.  **Parameter Dasar**:
            * **D - Permintaan Tahunan**: Total unit produk yang dibutuhkan dalam satu tahun.
            * **C - Harga Beli per Unit**: Harga beli satu unit produk (dalam Rupiah).
            * **A - Ongkos Tetap per Pemesanan**: Biaya tetap setiap kali memesan (misal: biaya administrasi, telepon).
            * **h - Ongkos Penyimpanan per Unit per Tahun**: Biaya menyimpan satu unit produk selama satu tahun.
            * **L - Lead Time (tahun)**: Waktu tunggu dari pesan hingga barang datang (dalam satuan tahun).

        **Langkah 2: Memahami Hasil di Setiap Tab**
        * **📈 Perhitungan Utama**: Menampilkan hasil perhitungan inti (Q*, R, T) dan rincian semua biaya.
        * **📊 Analisis Grafik**: Visualisasi kurva biaya untuk menemukan titik optimal dan komposisi biaya.
        * **🔍 Sensitivitas**: Melihat bagaimana perubahan parameter input memengaruhi hasil.
        * **📋 Ringkasan**: Tabel ringkasan semua input dan output untuk pelaporan.
        """)

    with st.expander("▶️ **Analisis Kesesuaian dengan Teori (Model EOQ)**"):
        st.markdown("""
        Ya, aplikasi ini **sudah sangat sesuai** dengan teori manajemen persediaan, khususnya model **Economic Order Quantity (EOQ)**.

        1.  **Formula EOQ (Q\*)**: Perhitungan `Ukuran Pesanan Optimal (Q)` menggunakan formula standar EOQ: $Q^* = \\sqrt{\\frac{2DA}{h}}$. Ini adalah inti dari model yang bertujuan menyeimbangkan biaya pemesanan dan biaya penyimpanan.

        2.  **Keseimbangan Biaya**: Teori EOQ menyatakan bahwa titik optimal (biaya terendah) tercapai ketika total biaya pemesanan tahunan sama dengan total biaya penyimpanan tahunan. Anda bisa melihat ini pada **Tab Analisis Grafik**, di mana kurva `Ongkos Pemesanan (OP)` dan `Ongkos Penyimpanan (OS)` berpotongan tepat di titik Q* optimal.

        3.  **Reorder Point (R)**: Perhitungan $R = D \\times L$ adalah formula standar untuk menentukan titik pemesanan kembali dalam kondisi permintaan yang konstan dan diketahui, yang merupakan asumsi dasar model EOQ.

        4.  **Peringatan (L < T)**: Aplikasi ini memberikan analisis tambahan yang cerdas dengan memeriksa apakah `Lead Time (L)` lebih kecil dari `Siklus Waktu (T)`. Jika L ≥ T, artinya pesanan berikutnya belum akan datang saat persediaan sudah habis. Peringatan untuk mempertimbangkan **Safety Stock** ini adalah penerapan praktis yang sangat baik dari teori untuk kondisi dunia nyata.

        **Kesimpulan**: Aplikasi ini adalah alat analisis yang mengimplementasikan model EOQ secara akurat dan memberikan interpretasi yang relevan secara manajerial.
        """)


# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.9rem;'>📦 Supply Chain Management - Pengukuran Ongkos | Dibuat dengan Streamlit</div>", unsafe_allow_html=True)
