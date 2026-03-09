import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Customer Happiness Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# FIXED CUSTOM CSS
# =========================
st.markdown("""
    <style>
    /* Mengatur kotak metric agar kontras di tema apapun */
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05); /* Transparan tipis */
        border: 1px solid rgba(151, 151, 151, 0.3);
        padding: 15px;
        border-radius: 10px;
        color: inherit; /* Mengikuti warna tema (hitam di light, putih di dark) */
    }
    
    /* Membuat label metric lebih jelas */
    [data-testid="stMetricLabel"] {
        font-weight: bold;
        color: #7d7d7d;
    }

    /* Styling tambahan untuk box biru di sebelah kanan */
    .logic-box {
        background-color: #1e3a8a;
        color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================
# HEADER SECTION
# =========================
# Menggunakan kolom untuk menyeimbangkan logo/judul jika perlu
col_title, col_logo = st.columns([4, 1])

with col_title:
    st.title("📦 Customer Happiness Prediction")
    st.markdown("""
    ### *Transforming Delivery Data into Actionable Satisfaction Insights*
    Platform analitik berbasis Machine Learning untuk memprediksi sentimen pelanggan 
    berdasarkan efisiensi logistik dan parameter transaksi.
    """)

st.divider()

# =========================
# KEY PERFORMANCE INDICATORS (KPI)
# =========================
# Mengganti 'Project Highlights' menjadi format dashboard yang lebih modern
st.subheader("🚀 Project Focus")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(label="Target Variable", value="Happy Customer", delta="Binary Class")
with c2:
    st.metric(label="Primary Algorithm", value="Logistic Regression", delta="High Accuracy")
with c3:
    st.metric(label="Data Points", value="5+ Features", delta="Optimized")
with c4:
    st.metric(label="Deployment", value="Streamlit Cloud", delta="Live")

st.write("") # Spacer

# =========================
# MODEL WORKFLOW & FEATURES
# =========================
# Menggunakan kontainer agar visual lebih terorganisir
with st.container():
    col_text, col_img = st.columns([2, 1])
    
    with col_text:
        st.header("🔍 Analisis Faktor Prediksi")
        st.write("""
        Model kami tidak hanya menebak, tetapi menganalisis pola perilaku logistik 
        untuk menentukan probabilitas kepuasan pelanggan:
        """)
        
        # Menggunakan kolom kecil untuk menampilkan fitur secara grid
        f1, f2 = st.columns(2)
        with f1:
            st.markdown("- **💰 Economic Factors**: Order Price & Delivery Charges.")
            st.markdown("- **📍 Geospatial Data**: Customer Location & Warehouse Distance.")
        with f2:
            st.markdown("- **📅 Temporal Data**: Order Date & Peak Season Analysis.")
            st.markdown("- **🚚 Logistic Efficiency**: Delivery Speed Estimation.")

    with col_img:
        # Menambahkan box info sebagai pengganti gambar jika tidak ada asset
        st.info("""
        **Model Logic:**
        Data Masuk → Preprocessing → Feature Engineering → Inference Engine → **Sentiment Result**
        """)

st.divider()

# =========================
# FOOTER / NAVIGATION
# =========================
# Membuat call-to-action yang lebih menonjol
st.success("### 💡 Siap mencoba?")
col_btn, col_empty = st.columns([1, 2])

with col_btn:
    if st.button("Buka Halaman Prediksi"):
        st.toast("Gunakan menu Sidebar di sebelah kiri!")

st.markdown("""
<div style="text-align: center; color: grey; font-size: 0.8em; margin-top: 50px;">
    © 2024 Data Science Team | Built with Streamlit & Machine Learning
</div>
""", unsafe_allow_html=True)