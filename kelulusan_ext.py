import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt


def show_kelulusan_ext():
    # Konfigurasi Google Sheets API
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Membuat objek Credentials dari secrets
    creds = Credentials.from_service_account_info(
        dict(st.secrets["google_credentials"]), scopes=scope
    )
    client = gspread.authorize(creds)

    # Buka Google Spreadsheet berdasarkan URL atau ID
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1m2ZTZ1sLSap9fkbfDrItjJdH7P4z3y7Vi_7AkbajoWQ"
    sheet = client.open_by_url(spreadsheet_url).sheet1

    # Ambil semua data dari sheet dan konversikan ke DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Pastikan kolom 'Rata-Rata' ada dan konversikan ke angka
    if 'Rata-Rata' in df.columns:
        df['Rata-Rata'] = pd.to_numeric(df['Rata-Rata'], errors='coerce').fillna(0)

    # Normalisasi kolom 'Kelompok' untuk konsistensi
    if 'Kelompok' in df.columns:
        df['Kelompok'] = df['Kelompok'].str.strip().str.upper()

    # Input nilai rata-rata
    st.subheader("Filter Data Berdasarkan Rata-Rata")
    nilai_rata_rata = st.number_input(
        "Masukkan nilai rata-rata:", min_value=0.0, max_value=100.0, step=0.1)

    # Pilihan filter antara PTN atau Kelompok Prodi
    st.subheader("Pilih Filter Data")
    pilihan_filter = st.radio("Filter berdasarkan:", ("PTN", "Kelompok Prodi"))

    if pilihan_filter == "PTN":
        ptn_terpilih = st.selectbox("Pilih Nama PTN:", df['Diterima di PTN'].dropna().unique())
        df_filtered = df[df['Diterima di PTN'] == ptn_terpilih]
    else:
        kelompok_terpilih = st.selectbox("Pilih Kelompok:", df['Kelompok'].dropna().unique()).strip().upper()
        df_filtered = df[df['Kelompok'].str.contains(kelompok_terpilih, na=False, regex=False)]

        # Jika 'Kelompok Prodi' dipilih, buat histogram berdasarkan 'Provinsi PTN'
        if not df_filtered.empty:
            # Filter data untuk rata-rata
            df_filtered = df_filtered[df_filtered['Rata-Rata'] <= nilai_rata_rata]

            # Tampilkan histogram jika kolom 'Provinsi PTN' ada
            if 'Provinsi PTN' in df_filtered.columns:
                st.subheader(f"Histogram Rata-Rata Kelompok '{kelompok_terpilih}' Berdasarkan Provinsi PTN")
                
                # Membuat histogram
                fig, ax = plt.subplots()
                df_filtered.groupby('Provinsi PTN')['Rata-Rata'].mean().plot(
                    kind='bar', ax=ax, color='skyblue', edgecolor='black'
                )
                ax.set_xlabel("Provinsi PTN")
                ax.set_ylabel("Rata-Rata")
                ax.set_title(f"Histogram Rata-Rata Berdasarkan Provinsi PTN untuk '{kelompok_terpilih}'")
                st.pyplot(fig)

    # Filter berdasarkan nama sekolah
    st.subheader("Filter Data Berdasarkan Nama Sekolah")
    if 'Sekolah' in df.columns and 'Diterima di PTN' in df.columns and 'TAHUN' in df.columns:
        unique_schools = df['Sekolah'].dropna().unique()
        selected_school = st.selectbox("Pilih Sekolah:", unique_schools)

        if selected_school:
            school_filtered_df = df[df['Sekolah'] == selected_school]

            # Hitung jumlah PTN berdasarkan kolom 'Diterima di PTN' dan 'TAHUN'
            ptn_count = (
                school_filtered_df.groupby(['TAHUN', 'Diterima di PTN'])
                .size()
                .reset_index(name='Jumlah')
                .pivot(index='Diterima di PTN', columns='TAHUN', values='Jumlah')
                .fillna(0)
                .astype(int)
            )

            st.write(f"Jumlah PTN yang diterima dari Sekolah '{selected_school}' berdasarkan tahun:")
            st.dataframe(ptn_count)
    else:
        st.error("Kolom yang dibutuhkan untuk filter nama sekolah tidak ditemukan.")
