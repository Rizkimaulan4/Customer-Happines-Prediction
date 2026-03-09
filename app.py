import streamlit as st
import joblib
import numpy as np
import pandas as pd
import math

# --- LOAD MODEL & SCALER ---
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# --- INITIALIZE SESSION STATE ---
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

# --- PAGE CONFIG ---
st.set_page_config(page_title="Happiness Analytics", page_icon="📦", layout="wide")

# --- CUSTOM CSS (FIXED COLOR ISSUE) ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
    
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #0068c9;
        color: white;
        font-weight: bold;
    }

    /* FIX TULISAN DI DALAM CARD AGAR TERLIHAT JELAS */
    .analysis-card {
        background-color: #ffffff !important;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #0068c9;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
    }

    /* Memaksa semua teks di dalam card berwarna hitam gelap */
    .analysis-card h4, 
    .analysis-card p, 
    .analysis-card b, 
    .analysis-card li,
    .analysis-card span {
        color: #1a1a1a !important;
        line-height: 1.6;
    }

    .analysis-card hr {
        border: 0;
        border-top: 1px solid #ddd;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("📊 Customer Happiness Prediction")
st.markdown("Analisis probabilitas kepuasan pelanggan berdasarkan parameter logistik dan transaksi.")
st.divider()

# --- HELPER FUNCTIONS ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_season(m):
    if m in [12,1,2]: return "Summer"
    elif m in [3,4,5]: return "Autumn"
    elif m in [6,7,8]: return "Winter"
    else: return "Spring"

# --- INPUT SECTION ---
with st.container():
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.subheader("📍 Geolocation & Time")
        areas = {
            "Melbourne CBD":(-37.8136,144.9631), "Carlton":(-37.8000,144.9660),
            "Richmond":(-37.8180,145.0010), "Footscray":(-37.7993,144.9000),
            "Box Hill":(-37.8184,145.1256), "Dandenong":(-37.9870,145.2140)
        }
        area = st.selectbox("Customer Area", list(areas.keys()))
        customer_lat, customer_long = areas[area]

        c_time1, c_time2 = st.columns(2)
        with c_time1:
            month = st.selectbox("Order Month", list(range(1,13)), index=0)
        with c_time2:
            day_map = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
            day = st.selectbox("Order Day", list(day_map.keys()))
        
        day_of_week = day_map[day]
        is_weekend = 1 if day_of_week >= 5 else 0
        season = get_season(month)

    with col_right:
        st.subheader("🛒 Transaction Details")
        c_inv1, c_inv2 = st.columns(2)
        with c_inv1:
            order_price = st.number_input("Order Price ($)", min_value=0, value=50)
            delivery_charges = st.number_input(
                "Delivery Fee ($)", 
                min_value=0, 
                value=None, 
                placeholder="min deliv charge 50...",
                help="Biaya pengiriman standar minimal adalah $50."
            )
            final_delivery_fee = float(delivery_charges) if delivery_charges is not None else 50.0
            coupon_discount = st.number_input("Discount ($)", min_value=0, value=0)
        with c_inv2:
            total_item_type = st.number_input("Item Categories", min_value=1, value=3)
            total_quantity = st.number_input("Total Quantity", min_value=1, value=5)
            expedited = st.selectbox("Expedited Shipping", ["No", "Yes"])
        
        is_expedited_delivery = 1 if expedited == "Yes" else 0

# --- LOGIC & CALCULATIONS ---
warehouses = {
    "Nickolson":(-37.818595,144.969551), "Thompson":(-37.812673,145.015144), "Bakers":(-37.809996,145.050911)
}
distances = {name: haversine(customer_lat, customer_long, lat, lon) for name, (lat, lon) in warehouses.items()}
nearest_warehouse = min(distances, key=distances.get)
distance = distances[nearest_warehouse]

season_Spring = 1 if season == "Spring" else 0
season_Summer = 1 if season == "Summer" else 0
season_Winter = 1 if season == "Winter" else 0
is_far_customer = 1 if distance > 15 else 0
is_remote_customer = 1 if distance > 30 else 0
nearest_warehouse_Nickolson = 1 if nearest_warehouse == "Nickolson" else 0
nearest_warehouse_Thompson = 1 if nearest_warehouse == "Thompson" else 0
cluster = 0

# --- PREDICTION INTERFACE ---
st.divider()
st.subheader("🚀 Operational Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Nearest Facility", nearest_warehouse)
m2.metric("Estimated Distance", f"{distance:.2f} km")
m3.metric("Service Season", season)

if st.button("Generate Prediction Report"):
    st.session_state.show_analysis = False 
    
    features = {
        "order_price": order_price, "delivery_charges": final_delivery_fee,
        "customer_lat": customer_lat, "customer_long": customer_long,
        "coupon_discount": coupon_discount, "is_expedited_delivery": is_expedited_delivery,
        "distance_to_nearest_warehouse": distance, "is_far_customer": is_far_customer,
        "is_remote_customer": is_remote_customer, "cluster": cluster, "month": month,
        "day_of_week": day_of_week, "is_weekend": is_weekend, "total_item_type": total_item_type,
        "total_quantity": total_quantity, "nearest_warehouse_Nickolson": nearest_warehouse_Nickolson,
        "nearest_warehouse_Thompson": nearest_warehouse_Thompson, "season_Spring": season_Spring,
        "season_Summer": season_Summer, "season_Winter": season_Winter
    }

    input_df = pd.DataFrame([features])
    input_df = input_df[scaler.feature_names_in_]
    input_scaled = scaler.transform(input_df)

    st.session_state.pred_val = model.predict(input_scaled)[0]
    probs = model.predict_proba(input_scaled)[0]
    st.session_state.p_not_happy, st.session_state.p_happy = probs[0], probs[1]
    st.session_state.has_predicted = True

if 'has_predicted' in st.session_state and st.session_state.has_predicted:
    st.write("### Result Analysis")
    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        if st.session_state.pred_val == 1:
            st.success(f"**Status: HAPPY**\n\nConfidence: {st.session_state.p_happy:.2%}")
        else:
            st.error(f"**Status: NOT HAPPY**\n\nConfidence: {st.session_state.p_not_happy:.2%}")

    with res_col2:
        st.write("Satisfaction Probability Distribution")
        st.progress(st.session_state.p_happy)
        st.caption(f"Happy: {st.session_state.p_happy:.1%} | Not Happy: {st.session_state.p_not_happy:.1%}")
    
    st.write("")
    if st.button("🔍 Lihat Analisis & Saran Bisnis"):
        st.session_state.show_analysis = True

if st.session_state.show_analysis:
    st.divider()
    st.subheader("💡 Analisis Mendalam & Strategi Bisnis")
    
    if st.session_state.pred_val == 1:
        st.markdown(f"""
        <div class="analysis-card">
            <h4>Kesimpulan Analisis (Customer Happy)</h4>
            <p>Model memprediksi tingkat kepuasan sebesar <b>{st.session_state.p_happy:.1%}</b>. Kombinasi antara biaya pengiriman, jarak tempuh, dan harga barang berada pada titik optimal bagi customer ini.</p>
            <hr>
            <b>Rekomendasi Tindakan:</b>
            <ul>
                <li><b>Loyalty Retention:</b> Berikan voucher diskon otomatis untuk transaksi berikutnya.</li>
                <li><b>Upselling Opportunity:</b> Profil customer ini terbuka untuk penawaran produk premium.</li>
                <li><b>Review Booster:</b> Ajak customer memberikan rating positif.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="analysis-card" style="border-left: 8px solid #ff4b4b;">
            <h4>Kesimpulan Analisis (Customer Not Happy)</h4>
            <p>Terdapat risiko ketidakpuasan sebesar <b>{st.session_state.p_not_happy:.1%}</b>. Faktor logistik seperti jarak <b>{distance:.2f} km</b> atau biaya pengiriman <b>${final_delivery_fee}</b> menjadi hambatan utama.</p>
            <hr>
            <b>Rekomendasi Tindakan:</b>
            <ul>
                <li><b>Delivery Subsidy:</b> Pertimbangkan potongan biaya kirim untuk area ini.</li>
                <li><b>Expedited Priority:</b> Gunakan jalur prioritas untuk pesanan ini.</li>
                <li><b>Service Recovery:</b> Siapkan tim CS untuk follow-up proaktif.</li>
                <li><b>Gifting:</b> Sertakan merchandise kecil sebagai bentuk apresiasi.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""--- <div style="text-align: center; color: gray;">Customer Happiness Analytics Dashboard v1.0</div>""", unsafe_allow_html=True)