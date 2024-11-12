import streamlit as st
from datetime import datetime

# Title of the app
st.title("Sambutan Selamat Datang")

# Input form for user's name
name = st.text_input("Masukkan Nama Anda:", "")

# Check if name is entered
if name:
    # Display greeting
    st.subheader(f"Selamat datang, {name}!")

    # Show current date and time
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    st.write(f"Anda mengakses aplikasi ini pada {current_time}")

    # Additional welcome message
    st.write("Semoga harimu menyenangkan dan penuh semangat!")
else:
    st.write("Silakan masukkan nama Anda di atas untuk melanjutkan.")
