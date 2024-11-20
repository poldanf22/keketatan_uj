import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ui_info import show_info_ui
from its_info import show_info_its
from itb_info import show_info_itb
from unpad_info import show_info_unpad
from ipb_info import show_info_ipb
from ugm_info import show_info_ugm
from ub_info import show_info_ub
from kelulusan_ext import show_kelulusan_ext

# Konfigurasi Google Sheets API
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Buat koneksi dengan kredensial
# creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
# Membuat objek Credentials dari secrets
creds = Credentials.from_service_account_info(
    dict(st.secrets["google_credentials"]), scopes=scope
)
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
st.markdown("<h1 class='main-title'>📊 Aplikasi Perbandingan Keketatan dan Informasi PTN</h1>",
            unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Data dari tahun 2015 sampai 2023 pada jalur Tes Tulis</p>",
            unsafe_allow_html=True)

# Menyisipkan animasi atau GIF (URL gambar online atau lokal)
st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <img src="https://media.giphy.com/media/fUQ4rhUZJYiQsas6WD/giphy.gif?cid=82a1493b8e1q6d0vxka501wvaykh9exz2rzjtbu4s9u60mkn&ep=v1_gifs_trending&rid=giphy.gif&ct=g"
        width="200">
    </div>
    """,
    unsafe_allow_html=True
)
# Tambahkan garis pemisah untuk membedakan konten dan footer
st.markdown("---")

# Sidebar menu options
menu = st.sidebar.radio(
    "Pilih Menu",
    ("Beranda", "Pembanding Keketatan", "Peringkat Keketatan", "Kelulusan Eksternal SNBP", "Info SNBP UI", "Info SNBP ITS",
     "Info SNBP ITB", "Info SNBP UGM", "Info SNBP UNPAD", "Info SNBP IPB")
)

# Display content based on menu selection
if menu == "Beranda":
    st.header("Selamat Datang")
    st.write("""
Aplikasi ini dirancang untuk membantu siswa yang ingin masuk Perguruan Tinggi Negeri (PTN) dalam memahami tingkat persaingan di program studi (prodi) yang mereka tuju. Dengan data daya tampung dan jumlah peminat dari tahun 2015 hingga 2023, pengguna dapat melihat keketatan berbagai prodi di PTN.

**Fitur aplikasi ini mencakup:**
- **Perbandingan Keketatan**: Bandingkan keketatan antara dua prodi secara langsung.
- **Peringkat Keketatan**: Lihat peringkat keketatan berdasarkan kampus atau kelompok prodi tertentu.
- **Informasi Seputar SNBP Kampus Terpilih**: Akses data SNBP, termasuk daya tampung dan jumlah peminat di kampus unggulan seperti UI, ITS, ITB, UGM, UNPAD, dan IPB.
- **Data Kelulusan Siswa Eksternal**: Jelajahi data kelulusan siswa dari sekolah lain untuk menambah wawasan mengenai persaingan di PTN.

**Tujuan dari aplikasi ini** adalah agar siswa lebih menyadari tingkat persaingan di prodi yang mereka pilih, sehingga dapat menghindari bias intelektual—persepsi bahwa mereka siap meskipun kemampuan mungkin perlu ditingkatkan.

Aplikasi ini dibuat pada tahun 2024 dan tersedia untuk umum. Kami mengajak pengguna untuk menggunakannya secara bijak demi perencanaan pendidikan yang lebih matang dan realistis.
""")

elif menu == "Pembanding Keketatan":
    # Halaman Utama
    st.markdown(
        "<small>Sumber: <a href='https://docs.google.com/spreadsheets/d/1LuXdslowlr7mFDAVQcHZtEwYNJxs19GQiExl6OnmbEY/edit?gid=0#gid=0' target='_blank'>Google Sheets</a></small>",
        unsafe_allow_html=True
    )
    # Buat dictionary mapping NamaPTN ke PTN untuk dropdown
    ptn_mapping = dict(zip(df['NamaPTN'], df['PTN']))
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
    selected_ptn_2 = st.sidebar.selectbox(
        "Pilih PTN (Pembanding):", ptn_options)

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

        # Definisikan dt_values dan jp_values untuk digunakan di berbagai bagian
        dt_values_1 = filtered_df_1[dt_columns].values[0]
        jp_values_1 = filtered_df_1[jp_columns].values[0]
        dt_values_2 = filtered_df_2[dt_columns].values[0]
        jp_values_2 = filtered_df_2[jp_columns].values[0]

        if chart_type == "Grafik Batang":
            # Plot Daya Tampung
            st.subheader(
                f"Daya Tampung ({ptn_mapping[selected_ptn]} - {selected_prodi} vs {ptn_mapping[selected_ptn_2]} - {selected_prodi_2})")
            fig, ax = plt.subplots()
            ax.bar(dt_columns, dt_values_1, color='skyblue',
                   label=f"{ptn_mapping[selected_ptn]} - {selected_prodi}")
            ax.bar(dt_columns, dt_values_2, color='lightgreen', alpha=0.7,
                   label=f"{ptn_mapping[selected_ptn_2]} - {selected_prodi_2}")
            ax.set_xlabel("Tahun")
            ax.set_ylabel("Daya Tampung")
            ax.set_title("Daya Tampung per Tahun")
            ax.legend()
            st.pyplot(fig)

            # Plot Jumlah Peminat
            st.subheader(
                f"Jumlah Peminat ({ptn_mapping[selected_ptn]} - {selected_prodi} vs {ptn_mapping[selected_ptn_2]} - {selected_prodi_2})")
            fig, ax = plt.subplots()
            ax.bar(jp_columns, jp_values_1, color='salmon',
                   label=f"{ptn_mapping[selected_ptn]} - {selected_prodi}")
            ax.bar(jp_columns, jp_values_2, color='orange', alpha=0.7,
                   label=f"{ptn_mapping[selected_ptn_2]} - {selected_prodi_2}")
            ax.set_xlabel("Tahun")
            ax.set_ylabel("Jumlah Peminat")
            ax.set_title("Jumlah Peminat per Tahun")
            ax.legend()
            st.pyplot(fig)

        elif chart_type == "Scatter Plot":
            # Plot Scatter antara Daya Tampung dan Jumlah Peminat dengan trendline
            st.subheader(
                f"Scatter Plot Daya Tampung vs Jumlah Peminat ({ptn_mapping[selected_ptn]} - {selected_prodi} vs {ptn_mapping[selected_ptn_2]} - {selected_prodi_2})"
            )
            fig, ax = plt.subplots()

            # Plot scatter untuk dataset pertama
            ax.scatter(dt_values_1, jp_values_1, color='purple',
                       label=f"{ptn_mapping[selected_ptn]} - {selected_prodi}")

            # Tambahkan trendline untuk dataset pertama
            z1 = np.polyfit(dt_values_1, jp_values_1, 1)  # Linear fit
            p1 = np.poly1d(z1)
            ax.plot(dt_values_1, p1(dt_values_1), color='purple',
                    linestyle='--', label=f"Trendline {ptn_mapping[selected_ptn]}")

            # Plot scatter untuk dataset kedua
            ax.scatter(dt_values_2, jp_values_2, color='green',
                       label=f"{ptn_mapping[selected_ptn_2]} - {selected_prodi_2}")

            # Tambahkan trendline untuk dataset kedua
            z2 = np.polyfit(dt_values_2, jp_values_2, 1)  # Linear fit
            p2 = np.poly1d(z2)
            ax.plot(dt_values_2, p2(dt_values_2), color='green',
                    linestyle='--', label=f"Trendline {ptn_mapping[selected_ptn_2]}")

            # Set label dan judul
            ax.set_xlabel("Daya Tampung")
            ax.set_ylabel("Jumlah Peminat")
            ax.set_title("Scatter Plot antara Daya Tampung dan Jumlah Peminat")
            ax.legend()

            # Tampilkan plot
            st.pyplot(fig)

        # Analisis Otomatis
        avg_dt_1, avg_jp_1 = np.mean(dt_values_1), np.mean(jp_values_1)
        avg_dt_2, avg_jp_2 = np.mean(dt_values_2), np.mean(jp_values_2)
        max_dt_1, max_jp_1 = np.max(dt_values_1), np.max(jp_values_1)
        max_dt_2, max_jp_2 = np.max(dt_values_2), np.max(jp_values_2)

        # Hitung rata-rata rasio keketatan
        ratio_1 = avg_jp_1 / avg_dt_1 if avg_dt_1 > 0 else 0
        ratio_2 = avg_jp_2 / avg_dt_2 if avg_dt_2 > 0 else 0

        st.write("### Analisis:")

        # Membuat dua kolom berdampingan untuk analisis perbandingan
        col1, col2 = st.columns(2)

        # Informasi Prodi 1 di Kolom 1
        with col1:
            st.write(f"**{selected_prodi} ({selected_ptn}):**")
            st.write(f"- Rata-rata daya tampung: {avg_dt_1:.2f}")
            st.write(f"- Rata-rata jumlah peminat: {avg_jp_1:.2f}")
            st.write(f"- Daya tampung maksimum: {max_dt_1}")
            st.write(f"- Jumlah peminat maksimum: {max_jp_1}")
            st.write(f"- Rasio keketatan: 1:{ratio_1:.0f}")

        # Informasi Prodi 2 di Kolom 2
        with col2:
            st.write(f"**{selected_prodi_2} ({selected_ptn_2}):**")
            st.write(f"- Rata-rata daya tampung: {avg_dt_2:.2f}")
            st.write(f"- Rata-rata jumlah peminat: {avg_jp_2:.2f}")
            st.write(f"- Daya tampung maksimum: {max_dt_2}")
            st.write(f"- Jumlah peminat maksimum: {max_jp_2}")
            st.write(f"- Rasio keketatan: 1:{ratio_2:.0f}")


elif menu == "Peringkat Keketatan":
    st.markdown(
        "<small>Sumber: <a href='https://docs.google.com/spreadsheets/d/1LuXdslowlr7mFDAVQcHZtEwYNJxs19GQiExl6OnmbEY/edit?gid=0#gid=0' target='_blank'>Google Sheets</a></small>",
        unsafe_allow_html=True
    )
    st.header("Peringkat Keketatan")

    # Tambahkan pilihan untuk sortir berdasarkan Kelompok atau NamaPTN
    sort_option = st.selectbox("Sortir berdasarkan:", ["Kelompok", "Nama PTN"])

    # Pilih opsi sortir
    if sort_option == "Kelompok":
        # Sortir berdasarkan Kelompok2
        selected_option = st.selectbox(
            "Pilih Kelompok:", df['Kelompok2'].unique())
        df_filtered = df[df['Kelompok2'] == selected_option]
    else:
        # Sortir berdasarkan NamaPTN
        selected_option = st.selectbox(
            "Pilih Nama PTN:", df['NamaPTN'].unique())
        df_filtered = df[df['NamaPTN'] == selected_option]

    # Periksa jika df_filtered kosong
    if df_filtered.empty:
        st.write("Tidak ada data yang sesuai dengan pilihan yang dipilih.")
    else:
        # Identifikasi kolom daya tampung (dt15, dt16, ..., dt23) dan jumlah peminat (jp15, jp16, ..., jp23)
        dt_columns = [f'dt{i}' for i in range(15, 24)]
        jp_columns = [f'jp{i}' for i in range(15, 24)]
        last_year_dt_column = 'dt23'  # Daya tampung untuk tahun terakhir

        # Pastikan kolom dt dan jp ditemukan
        if dt_columns and jp_columns and last_year_dt_column in df_filtered.columns:
            # Konversi kolom dt dan jp ke tipe numerik dan tangani NaN
            df_filtered[dt_columns] = df_filtered[dt_columns].apply(
                pd.to_numeric, errors='coerce').fillna(0)
            df_filtered[jp_columns] = df_filtered[jp_columns].apply(
                pd.to_numeric, errors='coerce').fillna(0)

            # Hitung rata-rata dan maksimum daya tampung dan jumlah peminat
            df_filtered['avg_dt'] = df_filtered[dt_columns].mean(axis=1)
            df_filtered['avg_jp'] = df_filtered[jp_columns].mean(axis=1)
            df_filtered['max_dt'] = df_filtered[dt_columns].max(axis=1)
            df_filtered['max_jp'] = df_filtered[jp_columns].max(axis=1)

            # Hitung rasio keketatan
            df_filtered['Rasio Keketatan'] = df_filtered.apply(
                lambda x: f"1:{x['avg_jp'] / x['avg_dt']:.0f}" if x['avg_dt'] > 0 else "Prodi Baru",
                axis=1
            )

            # Tambahkan kolom daya tampung tahun terakhir (dt23)
            df_filtered['Daya Tampung Terakhir'] = df_filtered[last_year_dt_column]

            # Filter kolom yang dibutuhkan dan urutkan berdasarkan Rasio Keketatan
            df_filtered = df_filtered[['NamaProdi', 'PTN', 'Jenjang', 'Akreditasi',
                                       'Propinsi', 'Rasio Keketatan', 'Daya Tampung Terakhir']]

            # Urutkan dengan ekstraksi nilai rasio keketatan numerik
            df_filtered = df_filtered.sort_values(
                by='Rasio Keketatan',
                key=lambda x: pd.to_numeric(x.str.extract(
                    ':(\d+)$')[0], errors='coerce').fillna(float('inf')),
                ascending=True
            )

            # Tambahkan nomor urut
            df_filtered.reset_index(drop=True, inplace=True)
            df_filtered.index += 1
            df_filtered.index.name = 'No'

            # Tampilkan tabel
            st.write(
                f"### Tabel Rata-rata Rasio Keketatan untuk {sort_option} {selected_option}")
            st.dataframe(df_filtered)
        else:
            st.write(
                "Kolom daya tampung atau jumlah peminat tidak ditemukan dalam data.")

elif menu == "Info SNBP UI":
    st.title("Informasi SNBP di UI")
    show_info_ui()

elif menu == "Info SNBP UGM":
    st.title("Informasi SNBP di UGM")
    show_info_ugm()

elif menu == "Info SNBP ITS":
    st.title("Informasi SNBP di ITS")
    show_info_its()

elif menu == "Info SNBP UNPAD":
    st.title("Informasi SNBP di UNPAD")
    show_info_unpad()

elif menu == "Info SNBP ITB":
    st.title("Informasi SNBP di ITB")
    show_info_itb()

elif menu == "Info SNBP IPB":
    st.title("Informasi SNBP di IPB")
    show_info_ipb()

elif menu == "Info SNBP UB":
    st.title("Informasi SNBP di UB")
    show_info_ub()

elif menu == "Kelulusan Eksternal SNBP":
    st.markdown(
        "<small>Sumber: <a href='https://docs.google.com/spreadsheets/d/1m2ZTZ1sLSap9fkbfDrItjJdH7P4z3y7Vi_7AkbajoWQ/edit?gid=0#gid=0' target='_blank'>Google Sheets</a></small>",
        unsafe_allow_html=True
    )
    st.title("Data Kelulusan SNBP")
    show_kelulusan_ext()

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
