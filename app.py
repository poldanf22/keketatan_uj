import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi Google Sheets API
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Buat koneksi dengan kredensial
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Buka Google Spreadsheet berdasarkan URL atau ID
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1LuXdslowlr7mFDAVQcHZtEwYNJxs19GQiExl6OnmbEY"
sheet = client.open_by_url(spreadsheet_url).sheet1  # Mengakses sheet pertama

# Ambil semua data dari sheet dan konversikan ke DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Menambahkan gaya custom
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
    }
    .sub-title {
        font-size: 18px;
        text-align: center;
        color: #6c757d;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Konten utama aplikasi Streamlit Anda
st.markdown("<h1 class='main-title'>📊 Aplikasi Perbandingan Daya Tampung dan Jumlah Peminat PTN</h1>",
            unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Data dari tahun 2015 sampai 2023 pada jalur Tes Tulis</p>",
            unsafe_allow_html=True)

# Menyisipkan animasi atau GIF (URL gambar online atau lokal)
st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZHdtZGwxbm5xZjdpZ2FuYjM1ZjZidmQxbTUxbzFoa2EzcmZnenRzMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1hqYk0leUMddBBkAM7/giphy.gif"
        width="200">
    </div>
    """,
    unsafe_allow_html=True
)
# Tambahkan garis pemisah untuk membedakan konten dan footer
st.markdown("---")

# Halaman Utama
# 1. Pilih PTN untuk halaman utama
ptn_options = df['NamaPTN'].unique()
selected_ptn = st.selectbox("Pilih PTN:", ptn_options)

if selected_ptn:
    # Filter data berdasarkan PTN yang dipilih di halaman utama
    filtered_df_main = df[df['NamaPTN'] == selected_ptn]

    # 2. Pilih Jenjang untuk halaman utama
    jenjang_options_main = filtered_df_main['Jenjang'].unique()
    selected_jenjang = st.selectbox("Pilih Jenjang:", jenjang_options_main)

    if selected_jenjang:
        # Filter data lebih lanjut berdasarkan jenjang di halaman utama
        filtered_df_main = filtered_df_main[filtered_df_main['Jenjang']
                                            == selected_jenjang]

        # 3. Pilih Program Studi untuk halaman utama
        prodi_options_main = filtered_df_main['NamaProdi'].unique()
        selected_prodi = st.selectbox(
            "Pilih Program Studi:", prodi_options_main)

# Sidebar untuk Pilihan Pembanding
st.sidebar.title("Pembanding Program Studi")

# Sidebar - Pilih PTN kedua
selected_ptn_2 = st.sidebar.selectbox("Pilih PTN (Pembanding):", ptn_options)

if selected_ptn_2:
    # Filter data berdasarkan PTN yang dipilih di sidebar
    filtered_df_sidebar = df[df['NamaPTN'] == selected_ptn_2]

    # Sidebar - Pilih Jenjang kedua
    jenjang_options_sidebar = filtered_df_sidebar['Jenjang'].unique()
    selected_jenjang_2 = st.sidebar.selectbox(
        "Pilih Jenjang (Pembanding):", jenjang_options_sidebar)

    if selected_jenjang_2:
        # Filter data lebih lanjut berdasarkan jenjang di sidebar
        filtered_df_sidebar = filtered_df_sidebar[filtered_df_sidebar['Jenjang']
                                                  == selected_jenjang_2]

        # Sidebar - Pilih Program Studi Kedua
        prodi_options_2 = filtered_df_sidebar['NamaProdi'].unique()
        selected_prodi_2 = st.sidebar.selectbox(
            "Pilih Program Studi Kedua:", prodi_options_2)

# 4. Pilih Jenis Grafik
chart_type = st.selectbox("Pilih Jenis Grafik:", [
                          "Grafik Batang", "Scatter Plot"])

# Pastikan kedua program studi dipilih
if selected_prodi and selected_prodi_2:
    # Filter data berdasarkan Program Studi pertama
    filtered_df_1 = filtered_df_main[filtered_df_main['NamaProdi']
                                     == selected_prodi]

    # Filter data berdasarkan Program Studi kedua
    filtered_df_2 = filtered_df_sidebar[filtered_df_sidebar['NamaProdi']
                                        == selected_prodi_2]

    # Ambil data daya tampung (dt15 hingga dt23) dan jumlah peminat (jp15 hingga jp23)
    dt_columns = [f'dt{i}' for i in range(15, 24)]
    jp_columns = [f'jp{i}' for i in range(15, 24)]

    # Konversi kolom dt dan jp ke tipe numerik dan tangani NaN
    filtered_df_1[dt_columns] = filtered_df_1[dt_columns].apply(
        pd.to_numeric, errors='coerce').fillna(0)
    filtered_df_1[jp_columns] = filtered_df_1[jp_columns].apply(
        pd.to_numeric, errors='coerce').fillna(0)
    filtered_df_2[dt_columns] = filtered_df_2[dt_columns].apply(
        pd.to_numeric, errors='coerce').fillna(0)
    filtered_df_2[jp_columns] = filtered_df_2[jp_columns].apply(
        pd.to_numeric, errors='coerce').fillna(0)

    # Definisikan dt_values dan jp_values lebih awal untuk digunakan di berbagai bagian
    dt_values_1 = filtered_df_1[dt_columns].values[0]
    jp_values_1 = filtered_df_1[jp_columns].values[0]
    dt_values_2 = filtered_df_2[dt_columns].values[0]
    jp_values_2 = filtered_df_2[jp_columns].values[0]

    if chart_type == "Grafik Batang":
        # Plot Daya Tampung
        st.subheader(
            f"Daya Tampung ({selected_ptn} - {selected_prodi} vs {selected_ptn_2} - {selected_prodi_2})")
        fig, ax = plt.subplots()
        ax.bar(dt_columns, dt_values_1, color='skyblue',
               label=f"{selected_ptn} - {selected_prodi}")
        ax.bar(dt_columns, dt_values_2, color='lightgreen', alpha=0.7,
               label=f"{selected_ptn_2} - {selected_prodi_2}")
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Daya Tampung")
        ax.set_title("Daya Tampung per Tahun")
        ax.legend()
        st.pyplot(fig)

        # Plot Jumlah Peminat
        st.subheader(
            f"Jumlah Peminat ({selected_ptn} - {selected_prodi} vs {selected_ptn_2} - {selected_prodi_2})")
        fig, ax = plt.subplots()
        ax.bar(jp_columns, jp_values_1, color='salmon',
               label=f"{selected_ptn} - {selected_prodi}")
        ax.bar(jp_columns, jp_values_2, color='orange', alpha=0.7,
               label=f"{selected_ptn_2} - {selected_prodi_2}")
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Jumlah Peminat")
        ax.set_title("Jumlah Peminat per Tahun")
        ax.legend()
        st.pyplot(fig)

    elif chart_type == "Scatter Plot":
        # Plot Scatter antara Daya Tampung dan Jumlah Peminat dengan trend line
        st.subheader(
            f"Scatter Plot Daya Tampung vs Jumlah Peminat ({selected_ptn} - {selected_prodi} vs {selected_ptn_2} - {selected_prodi_2})")
        fig, ax = plt.subplots()

        # Scatter Plot for Prodi 1
        ax.scatter(dt_values_1, jp_values_1, color='purple',
                   label=f"{selected_ptn} - {selected_prodi}")

        if len(np.unique(dt_values_1)) > 1 and len(np.unique(jp_values_1)) > 1:
            m1, b1 = np.polyfit(dt_values_1, jp_values_1, 1)
            trend_line_1 = m1 * np.array(dt_values_1) + b1
            ax.plot(dt_values_1, trend_line_1, color='blue',
                    linestyle='--', label=f"Trend Line {selected_prodi}")
        else:
            st.write(
                f"Garis tren untuk {selected_ptn} - {selected_prodi} tidak dapat dihitung karena data kurang bervariasi.")

        ax.scatter(dt_values_2, jp_values_2, color='green',
                   label=f"{selected_ptn_2} - {selected_prodi_2}")

        if len(np.unique(dt_values_2)) > 1 and len(np.unique(jp_values_2)) > 1:
            m2, b2 = np.polyfit(dt_values_2, jp_values_2, 1)
            trend_line_2 = m2 * np.array(dt_values_2) + b2
            ax.plot(dt_values_2, trend_line_2, color='orange',
                    linestyle='--', label=f"Trend Line {selected_prodi_2}")
        else:
            st.write(
                f"Garis tren untuk {selected_ptn_2} - {selected_prodi_2} tidak dapat dihitung karena data kurang bervariasi.")

        ax.set_xlabel("Daya Tampung")
        ax.set_ylabel("Jumlah Peminat")
        ax.set_title("Scatter Plot antara Daya Tampung dan Jumlah Peminat")
        ax.legend()
        st.pyplot(fig)

    # Analisis Otomatis
    avg_dt_1, avg_jp_1 = np.mean(dt_values_1), np.mean(jp_values_1)
    avg_dt_2, avg_jp_2 = np.mean(dt_values_2), np.mean(jp_values_2)
    max_dt_1, max_jp_1 = np.max(dt_values_1), np.max(jp_values_1)
    max_dt_2, max_jp_2 = np.max(dt_values_2), np.max(jp_values_2)

    # Hitung rata-rata rasio keketatan
    if avg_dt_1 > 0:
        ratio_1 = avg_jp_1 / avg_dt_1
    else:
        ratio_1 = 0

    if avg_dt_2 > 0:
        ratio_2 = avg_jp_2 / avg_dt_2
    else:
        ratio_2 = 0

    st.write("### Analisis Otomatis:")
    st.write(f"**{selected_prodi} ({selected_ptn}):**")
    st.write(f"- Rata-rata daya tampung: {avg_dt_1:.2f}")
    st.write(f"- Rata-rata jumlah peminat: {avg_jp_1:.2f}")
    st.write(f"- Daya tampung maksimum: {max_dt_1}")
    st.write(f"- Jumlah peminat maksimum: {max_jp_1}")
    st.write(f"- Rasio keketatan: 1:{ratio_1:.0f}")

    st.write(f"**{selected_prodi_2} ({selected_ptn_2}):**")
    st.write(f"- Rata-rata daya tampung: {avg_dt_2:.2f}")
    st.write(f"- Rata-rata jumlah peminat: {avg_jp_2:.2f}")
    st.write(f"- Daya tampung maksimum: {max_dt_2}")
    st.write(f"- Jumlah peminat maksimum: {max_jp_2}")
    st.write(f"- Rasio keketatan: 1:{ratio_2:.0f}")

# Copyright footer menggunakan HTML dan CSS
footer = """
<style>
footer {
    visibility: hidden;
}

footer:after {
    content:'© 2024 - Especially for UJ from bang Iqbal.'; 
    visibility: visible;
    display: block;
    position: relative;
    color: #888;
    padding: 5px;
    top: 2px;
    text-align: center;
}
</style>
"""

st.markdown(footer, unsafe_allow_html=True)
