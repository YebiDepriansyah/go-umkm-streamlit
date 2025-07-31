import streamlit as st
import requests

st.set_page_config(page_title="Go-UMKM Recommender", page_icon="🧠")

st.title("🤝 Go-UMKM Recommendation App")
st.markdown("Dapatkan rekomendasi UMKM dan investor berdasarkan profil pengguna.")

# Input
user_id = st.text_input("🔎 Masukkan User ID (UMKM atau Investor)")
k = st.slider("📊 Jumlah rekomendasi", 1, 10, 5)

# API URL
BASE_URL = "https://umkm-fastapi-heroku-496b36a59a51.herokuapp.com"

if st.button("🎯 Tampilkan Rekomendasi"):
    if user_id.strip():
        with st.spinner("Mengambil rekomendasi..."):
            url = f"{BASE_URL}/recommend/{user_id}?k={k}"
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                st.success("Rekomendasi ditemukan:")
                for i, rec in enumerate(data["recommendations"], 1):
                    st.markdown(f"### {i}. {rec['kategori']} ({rec['model_bisnis']})")
                    st.write(f"- Skala: {rec['skala']}")
                    st.write(f"- Jangkauan: {rec['jangkauan']}")
                    st.write(f"- Similarity Score: `{rec['similarity_score']}`")
                    st.markdown("---")
            else:
                st.error("Gagal mengambil data. Pastikan ID valid.")
    else:
        st.warning("Mohon masukkan User ID terlebih dahulu.")
