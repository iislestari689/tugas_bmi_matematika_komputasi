import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Kalkulator BMI", page_icon="⚖️")

def hitung_bmi(berat, tinggi):
    bmi = berat / (tinggi ** 2)
    return bmi

def kategori_bmi(bmi):
    if bmi < 18.5:
        return "Kekurangan berat badan", "#3498db"
    elif 18.5 <= bmi < 24.9:
        return "Berat badan normal", "#2ecc71"
    elif 25 <= bmi < 29.9:
        return "Kelebihan berat badan", "#f39c12"
    else:
        return "Obesitas", "#e74c3c"

st.title("⚖️ Kalkulator BMI Sederhana")
st.write("Yuk cek kondisi berat badanmu dan pantau riwayatnya dalam grafik!")

# Input pengguna
col1, col2 = st.columns(2)
with col1:
    berat = st.number_input("Berat badan (kg):", min_value=1.0, step=0.1)
with col2:
    tinggi_cm = st.number_input("Tinggi badan (cm):", min_value=50.0, step=1.0)

if st.button("🔍 Hitung BMI", use_container_width=True):
    if tinggi_cm > 0:
        # Animasi loading sebelum hasil muncul
        with st.spinner("Menghitung BMI kamu..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.005)
                progress_bar.progress(i + 1)
            progress_bar.empty()

        tinggi_m = tinggi_cm / 100
        bmi = hitung_bmi(berat, tinggi_m)
        kategori, warna = kategori_bmi(bmi)
        waktu_cek = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Tampilkan hasil dengan efek animasi
        st.balloons()
        st.markdown(
            f"""
            <div style="background-color:{warna}22; padding:20px; border-radius:15px;
                        border-left:8px solid {warna}; animation: fadeIn 1s;">
                <h2 style="color:{warna}; margin:0;">BMI Anda: {bmi:.2f}</h2>
                <h4 style="color:{warna}; margin:5px 0 0 0;">{kategori}</h4>
                <p style="margin:5px 0 0 0; font-size:13px; color:gray;">📅 {waktu_cek}</p>
            </div>
            <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(-10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        # Simpan riwayat
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

# Grafik riwayat BMI
if "riwayat" in st.session_state and len(st.session_state.riwayat) > 0:
    st.write("---")
    st.subheader("📈 Grafik Riwayat BMI")

    df = pd.DataFrame(st.session_state.riwayat)
    df["urutan"] = range(1, len(df) + 1)

    fig = go.Figure()

    # Garis tren BMI
    fig.add_trace(go.Scatter(
        x=df["urutan"],
        y=df["bmi"],
        mode="lines+markers+text",
        text=df["bmi"],
        textposition="top center",
        line=dict(color="#6c5ce7", width=3, shape="spline"),
        marker=dict(size=12, color="#6c5ce7", line=dict(width=2, color="white")),
        name="BMI"
    ))

    # Garis batas kategori (referensi visual)
    fig.add_hline(y=18.5, line_dash="dot", line_color="#3498db", annotation_text="Batas Kurus")
    fig.add_hline(y=24.9, line_dash="dot", line_color="#2ecc71", annotation_text="Batas Normal")
    fig.add_hline(y=29.9, line_dash="dot", line_color="#f39c12", annotation_text="Batas Gemuk")

    fig.update_layout(
        xaxis_title="Pengecekan ke-",
        yaxis_title="Nilai BMI",
        template="plotly_white",
        transition_duration=500,
        height=420,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Tombol reset riwayat
    if st.button("🗑️ Hapus Riwayat"):
        st.session_state.riwayat = []
        st.rerun()
