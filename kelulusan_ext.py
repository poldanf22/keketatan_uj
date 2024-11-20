import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


def show_kelulusan_ext():
    # Konfigurasi Google Sheets API
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Buat koneksi dengan kredensial
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

    # Input nilai rata-rata
    st.subheader("Filter Data Berdasarkan Rata-Rata")
    nilai_rata_rata = st.number_input(
        "Masukkan nilai rata-rata:", min_value=0.0, max_value=100.0, step=0.1)

    # Pilihan filter utama: PTN atau Kelompok Prodi
    st.subheader("Pilih Mode Filter Data")
    mode_filter = st.selectbox("Pilih mode filter:", ["PTN", "Kelompok Prodi"])

    # Filter berdasarkan PTN atau Kelompok Prodi
    if mode_filter == "PTN":
        if 'PTN' in df.columns:  # Pastikan kolom 'PTN' ada di DataFrame
            # Ambil nilai unik di kolom 'PTN'
            ptn_list = df['PTN'].dropna().unique()
            ptn_terpilih = st.selectbox("Pilih Nama PTN:", options=ptn_list)
            df_filtered = df[df['PTN'] == ptn_terpilih]
        else:
            st.error("Kolom 'PTN' tidak ditemukan di dalam data.")
    else:
        if 'Kelompok2' in df.columns:  # Pastikan kolom 'Kelompok2' ada di DataFrame
            # Ambil nilai unik di kolom 'Kelompok2'
            kelompok_list = df['Kelompok2'].dropna().unique()
            kelompok_terpilih = st.selectbox(
                "Pilih Kelompok Prodi:", options=kelompok_list)
            df_filtered = df[df['Kelompok2'] == kelompok_terpilih]
        else:
            st.error("Kolom 'Kelompok2' tidak ditemukan di dalam data.")

    # Filter data berdasarkan nilai rata-rata
    if 'Rata-Rata' in df.columns:
        df_filtered = df_filtered[df_filtered['Rata-Rata'] <= nilai_rata_rata]
        st.write(
            f"Data dengan kolom 'Rata-Rata' di bawah atau sama dengan {nilai_rata_rata}:")
        st.dataframe(df_filtered)
    else:
        st.error("Kolom 'Rata-Rata' tidak ditemukan di dalam data.")

    # Filter tambahan berdasarkan sekolah
    st.subheader("Filter Data Berdasarkan Nama Sekolah")
    if 'Sekolah' in df.columns:
        unique_schools = df['Sekolah'].dropna().unique()
        selected_school = st.selectbox(
            "Pilih Sekolah:", options=unique_schools)
        if selected_school:
            school_filtered_df = df[df['Sekolah'] == selected_school]
            st.write(f"Data untuk Sekolah '{selected_school}':")
            st.dataframe(school_filtered_df)
    else:
        st.error("Kolom 'Sekolah' tidak ditemukan di dalam data.")
