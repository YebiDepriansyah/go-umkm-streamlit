import streamlit as st
import pandas as pd
import requests

# Load investor data
investor_df = pd.read_csv("investor_data.csv")
umkm_df = pd.read_csv("umkm_data.csv")

st.set_page_config(page_title="Go-UMKM Dashboard", page_icon="💼", layout="wide")

st.title("📊 Dashboard Rekomendasi UMKM untuk Investor")

# Dropdown untuk memilih investor
investor_names = investor_df["nama"].tolist() if "nama" in investor_df.columns else investor_df["user_id"].tolist()
selected_name = st.selectbox("Pilih Investor", investor_names)

# Dapatkan user_id dari nama yang dipilih
selected_investor = investor_df[investor_df["nama"] == selected_name].iloc[0] if "nama" in investor_df.columns else investor_df[investor_df["user_id"] == selected_name].iloc[0]
user_id = selected_investor["user_id"]

# Tombol ambil rekomendasi
if st.button("Tampilkan Rekomendasi UMKM"):
    with st.spinner("Mengambil rekomendasi..."):
        url = f"https://umkm-fastapi-heroku-496b36a59a51.herokuapp.com/recommend/{user_id}?k=5"
        res = requests.get(url)

        if res.status_code == 200:
            data = res.json()
            st.success(f"Rekomendasi untuk investor: {selected_name}")

            for i, rec in enumerate(data["recommendations"], 1):
                umkm_data = umkm_df[umkm_df["user_id"] == rec["user_id"]].iloc[0] if "user_id" in umkm_df.columns else {}
                st.markdown(f"### {i}. {rec['kategori']} ({rec['model_bisnis']})")
                st.write(f"- Skala: {rec['skala']}")
                st.write(f"- Jangkauan: {rec['jangkauan']}")
                st.write(f"- Similarity Score: `{rec['similarity_score']:.3f}`")
                if umkm_data is not None:
                    st.write(f"- Nama UMKM: {umkm_data.get('nama', '-')}")
                st.markdown("---")
        else:
            st.error("Gagal mengambil rekomendasi. Coba lagi.")
