import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Terima Kasih", page_icon="🙏", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .thank-you-container {
        background-color: #1E1E1E;
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #333;
        margin-top: 50px;
    }
    .thank-you-title {
        color: #0068c9;
        font-size: 3em;
        font-weight: bold;
    }
    .thank-you-text {
        font-size: 1.2em;
        color: #FAFAFA;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #0068c9;
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENT ---
st.container()
st.markdown("""
    <div class="thank-you-container">
        <div class="thank-you-title">🙏 Terima Kasih!</div>
        <div class="thank-you-text">
            Aplikasi <b>Customer Happiness Prediction</b> ini telah selesai dijalankan. 
            <br><br>
            Terima kasih banyak sudah meluangkan waktu untuk mencoba dan menggunakan 
            dashboard berbasis <b>Streamlit</b> ini. Saya sangat menghargai dukungan Anda 
            dalam mengeksplorasi proyek analisis data ini.
        </div>
        <br>
        <p style="color: #888;">Semoga harimu menyenangkan dan sampai jumpa di proyek berikutnya!</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Tombol navigasi balik ke awal jika user mau coba lagi
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Kembali ke Halaman Utama"):
        st.switch_page("your_app_filename.py") # Ganti dengan nama file utama kamu

# --- FOOTER ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9em;">
        Final Project: Happiness Analytics Dashboard | Powered by Streamlit 2026
    </div>
    """, unsafe_allow_html=True)