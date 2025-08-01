import streamlit as st
import pandas as pd
import requests

# Load data UMKM (untuk Tab 2)
@st.cache_data
def load_umkm_data():
    return pd.read_csv("umkm_data.csv")

umkm_df = load_umkm_data()

# API Endpoint
API_BASE_URL = "https://umkm-fastapi-heroku-496b36a59a51.herokuapp.com"

# Fungsi untuk ambil rekomendasi dari API
def get_recommendations(user_id, k=5):
    try:
        url = f"{API_BASE_URL}/recommend/{user_id}?k={k}"
        res = requests.get(url)
        if res.status_code == 200:
            return res.json().get("recommendations", [])
        else:
            return f"❌ Error {res.status_code}: {res.text}"
    except Exception as e:
        return f"⚠️ Exception: {e}"

# UI
st.set_page_config(page_title="Go-UMKM Recommendation", layout="wide")
st.title("📊 Go-UMKM Recommendation App")

tab1, tab2 = st.tabs(["🔍 Rekomendasi Berdasarkan ID", "📋 Pilih UMKM dari Daftar"])

# Tab 1
with tab1:
    st.subheader("Masukkan ID UMKM untuk melihat rekomendasi")
    user_id_input = st.text_input("🆔 Masukkan ID UMKM (UUID format)")
    top_k = st.slider("Jumlah Rekomendasi", min_value=1, max_value=10, value=5)

    if st.button("Lihat Rekomendasi", type="primary"):
        if user_id_input:
            rekomendasi = get_recommendations(user_id_input, top_k)
            if isinstance(rekomendasi, str):
                st.error(rekomendasi)
            elif rekomendasi:
                st.success(f"{len(rekomendasi)} Rekomendasi ditemukan:")
                st.dataframe(pd.DataFrame(rekomendasi))
            else:
                st.warning("Tidak ada rekomendasi ditemukan.")
        else:
            st.warning("Silakan masukkan user ID terlebih dahulu.")

# Tab 2
with tab2:
    st.subheader("Pilih UMKM dari daftar")

    selected_umkm = st.selectbox(
        "🔽 Pilih UMKM", 
        options=umkm_df["user_id"].tolist(),
        format_func=lambda x: f"{x} | {umkm_df.loc[umkm_df['user_id'] == x, 'kategori'].values[0]}"
    )

top_k2 = st.slider("Jumlah Rekomendasi", min_value=1, max_value=10, value=5, key="slider2")

    if st.button("Tampilkan Rekomendasi untuk UMKM Terpilih", key="btn2"):
        rekomendasi2 = get_recommendations(selected_umkm, top_k2)
        if isinstance(rekomendasi2, str):
            st.error(rekomendasi2)
        elif rekomendasi2:
            st.success(f"{len(rekomendasi2)} Rekomendasi ditemukan:")
            st.dataframe(pd.DataFrame(rekomendasi2))
        else:
            st.warning("Tidak ada rekomendasi ditemukan.")
