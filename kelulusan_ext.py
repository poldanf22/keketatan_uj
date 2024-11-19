import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def show_kelulusan_ext():

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
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1m2ZTZ1sLSap9fkbfDrItjJdH7P4z3y7Vi_7AkbajoWQ"
    # Mengakses sheet pertama
    sheet = client.open_by_url(spreadsheet_url).sheet1

    # Ambil semua data dari sheet dan konversikan ke DataFrame
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # # Menampilkan judul aplikasi
    # st.title("Data dari Google Spreadsheet")

    # # Menampilkan DataFrame
    # if not df.empty:
    #     st.write("Berikut adalah data yang diambil dari Google Spreadsheet:")
    #     st.dataframe(df)  # Menggunakan st.dataframe untuk tampilan interaktif
    # else:
    #     st.write("Data tidak ditemukan atau kosong.")

    # Input nilai rata-rata
    st.subheader("Filter Data Berdasarkan Rata-Rata")
    nilai_rata_rata = st.number_input(
        "Masukkan nilai rata-rata:", min_value=0.0, max_value=100.0, step=0.1)

    # Pilihan filter antara PTN atau Kelompok Prodi
    st.subheader("Pilih Filter Data")
    pilihan_filter = st.radio("Filter berdasarkan:", ("PTN", "Kelompok Prodi"))

    # Input untuk filter PTN atau Kelompok Prodi
    if pilihan_filter == "PTN":
        ptn_terpilih = st.text_input("Masukkan nama PTN:")
    else:
        kelompok_terpilih = st.text_input("Masukkan nama Kelompok Prodi:")

    # Kolom yang tidak ingin ditampilkan
    columns_to_exclude = ['No', 'NAMA', '%', 'NAIK/TURUN']

    # Filter DataFrame berdasarkan input nilai rata-rata dan pilihan filter
    if not df.empty:
        if 'Rata-Rata' in df.columns:  # Pastikan kolom 'Rata-Rata' ada di DataFrame
            # Filter berdasarkan nilai rata-rata
            filtered_df = df[df['Rata-Rata'] <= nilai_rata_rata]

            if pilihan_filter == "PTN" and 'Diterima di PTN' in df.columns:
                filtered_df = filtered_df[filtered_df['Diterima di PTN'].str.contains(
                    ptn_terpilih, na=False, case=False)]
            elif pilihan_filter == "Kelompok Prodi" and 'Kelompok' in df.columns:
                filtered_df = filtered_df[filtered_df['Kelompok'].str.contains(
                    kelompok_terpilih, na=False, case=False)]

            # Hapus kolom yang tidak ingin ditampilkan
            filtered_df = filtered_df.drop(columns=[
                                           col for col in columns_to_exclude if col in filtered_df.columns], errors='ignore')

            st.write(
                f"Data dengan kolom 'Rata-Rata' di bawah atau sama dengan {nilai_rata_rata}:")
            st.dataframe(filtered_df)
        else:
            st.write("Kolom 'Rata-Rata' tidak ditemukan di dalam data.")
    else:
        st.write("Data tidak ditemukan atau kosong.")

    # Pastikan kolom yang dibutuhkan ada di DataFrame
    st.subheader("Filter Data Berdasarkan Nama Sekolah")
    required_columns = ['Sekolah', 'Diterima di PTN', 'TAHUN']

    if not all(col in df.columns for col in required_columns):
        st.error(
            f"DataFrame tidak memiliki kolom yang dibutuhkan: {', '.join(required_columns)}")
    else:
        # Dropdown untuk memilih sekolah secara unik
        unique_schools = df['Sekolah'].dropna().unique()
        selected_school = st.selectbox(
            "Pilih Sekolah:", options=unique_schools)

        if selected_school:
            # Filter data berdasarkan sekolah yang dipilih
            filtered_df = df[df['Sekolah'] == selected_school]

            # Hitung jumlah PTN berdasarkan kolom 'Diterima di PTN' dan 'TAHUN'
            ptn_count = (
                filtered_df.groupby(['TAHUN', 'Diterima di PTN'])
                .size()
                .reset_index(name='Jumlah')
            )

            # Tampilkan tabel hasil
            st.write(
                f"Jumlah PTN yang diterima dari Sekolah '{selected_school}' berdasarkan tahun:")
            st.dataframe(ptn_count)
