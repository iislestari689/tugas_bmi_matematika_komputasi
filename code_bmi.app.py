import streamlit as st
from datetime import datetime

def hitung_bmi(berat, tinggi):
    # Rumus BMI: berat (kg) / (tinggi (m) * tinggi (m))
    bmi = berat / (tinggi ** 2)
    return bmi

def kategori_bmi(bmi):
    if bmi < 18.5:
        return "Kekurangan berat badan"
    elif 18.5 <= bmi < 24.9:
        return "Berat badan normal"
    elif 25 <= bmi < 29.9:
        return "Kelebihan berat badan"
    else:
        return "Obesitas"

st.title("Kalkulator BMI Sederhana")

# Input pengguna
berat = st.number_input("Masukkan berat badan (kg):", min_value=1.0, step=0.1)
tinggi_cm = st.number_input("Masukkan tinggi badan (cm):", min_value=50.0, step=1.0)

if st.button("Hitung BMI"):
    if tinggi_cm > 0:
        tinggi_m = tinggi_cm / 100
        bmi = hitung_bmi(berat, tinggi_m)
        kategori = kategori_bmi(bmi)

        # Catat waktu pengecekan
        waktu_cek = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        st.write(f"### Hasil BMI Anda: {bmi:.2f}")
        st.write(f"### Kategori: {kategori}")
        st.write(f"📅 Waktu pengecekan: {waktu_cek}")

        # Opsional: simpan riwayat pengecekan dalam session
        if "riwayat" not in st.session_state:
            st.session_state.riwayat = []
        st.session_state.riwayat.append({
            "waktu": waktu_cek,
            "berat": berat,
            "tinggi_cm": tinggi_cm,
            "bmi": round(bmi, 2),
            "kategori": kategori
        })
    else:
        st.error("Tinggi badan harus lebih dari 0!")

# Tampilkan riwayat pengecekan jika ada
if "riwayat" in st.session_state and len(st.session_state.riwayat) > 0:
    st.write("---")
    st.write("### Riwayat Pengecekan")
    st.table(st.session_state.riwayat)
