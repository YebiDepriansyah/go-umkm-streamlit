import streamlit as st
import pandas as pd
import requests

# Load UMKM data
umkm_df = pd.read_csv("umkm_data (2).csv")

st.set_page_config(page_title="Go-UMKM Explorer", page_icon="🏪", layout="wide")

st.title("🏪 Daftar UMKM")
st.markdown("Pilih satu UMKM untuk melihat UMKM lain yang direkomendasikan untuknya.")

# Dropdown UMKM
umkm_names = umkm_df["nama"].tolist() if "nama" in umkm_df.columns else umkm_df["user_id"].tolist()
selected_umkm_name = st.selectbox("Pilih UMKM", umkm_names)

# Ambil user_id dari UMKM
selected_umkm = umkm_df[umkm_df["nama"] == selected_umkm_name].iloc[0] if "nama" in umkm_df.columns else umkm_df[umkm_df["user_id"] == selected_umkm_name].iloc[0]
umkm_user_id = selected_umkm["user_id"]

# Tombol untuk tampilkan rekomendasi
if st.button("🎯 Tampilkan UMKM Rekomendasi"):
    with st.spinner("Mengambil rekomendasi..."):
        url = f"https://umkm-fastapi-heroku-496b36a59a51.herokuapp.com/recommend/{umkm_user_id}?k=5"
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            st.subheader("📌 UMKM Rekomendasi:")
            for i, rec in enumerate(data["recommendations"], 1):
                umkm_detail = umkm_df[umkm_df["user_id"] == rec["user_id"]].iloc[0] if "user_id" in umkm_df.columns else {}
                st.markdown(f"### {i}. {rec['kategori']} ({rec['model_bisnis']})")
                st.write(f"- Nama UMKM: {umkm_detail.get('nama', '-')}")
                st.write(f"- Skala: {rec['skala']}")
                st.write(f"- Jangkauan: {rec['jangkauan']}")
                st.write(f"- Similarity Score: `{rec['similarity_score']:.3f}`")
                st.markdown("---")
        else:
            st.error("Gagal mendapatkan rekomendasi.")

# Tampilan tabel UMKM lengkap di bawah
st.subheader("📋 Semua Data UMKM")
st.dataframe(umkm_df)
