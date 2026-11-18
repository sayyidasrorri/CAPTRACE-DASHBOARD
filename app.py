
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="CAPTRACE Digital Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 CAPTRACE")
st.subheader("Mangrove Conservation Intelligence Dashboard")

st.caption("📍 Sayung, Demak, Jawa Tengah")
st.warning("DEMO — Seluruh angka merupakan data simulasi, bukan hasil pemantauan aktual.")

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌿 Mangrove Sehat", "68%")
col2.metric("📡 Smart Ajir", "24")
col3.metric("🌱 Kapsul Terdistribusi", "1.250")
col4.metric("⚠️ Area Prioritas", "12")

st.divider()

st.header("📊 Klasifikasi Kondisi Mangrove")

data = pd.DataFrame({
    "Kondisi": [
        "Healthy Mangrove",
        "Degraded Mangrove",
        "Open Area",
        "Priority Restoration Area"
    ],
    "Persentase": [68, 17, 10, 5]
})

fig = px.bar(
    data,
    x="Kondisi",
    y="Persentase",
    color="Kondisi",
    title="Distribusi Kondisi Mangrove (Simulasi)"
)

st.plotly_chart(fig, use_container_width=True)

st.header("📡 Smart Ajir Monitoring")

sensor = pd.DataFrame({
    "Parameter": ["Suhu", "Salinitas", "pH", "Kelembapan"],
    "Nilai": [29.5, 22, 7.2, 78],
    "Satuan": ["°C", "ppt", "pH", "%"]
})

st.dataframe(sensor, use_container_width=True)

st.success("CAPTRACE Digital Monitoring System — Prototype")

import folium
from streamlit_folium import st_folium

st.divider()

st.header("🗺️ CAPTRACE Restoration Monitoring Map")

st.info(
    "Peta demonstrasi. Koordinat perangkat dan titik restorasi "
    "merupakan ilustrasi, bukan data lapangan."
)

# Titik pusat ilustratif kawasan Sayung, Demak
pusat = [-6.93, 110.49]

peta = folium.Map(
    location=pusat,
    zoom_start=12,
    tiles="OpenStreetMap"
)

# Lokasi Smart Ajir simulasi
folium.Marker(
    location=[-6.925, 110.485],
    popup="Smart Ajir 01 — Monitoring Lingkungan (Simulasi)",
    tooltip="Smart Ajir 01",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(peta)

folium.Marker(
    location=[-6.935, 110.495],
    popup="Smart Ajir 02 — Monitoring Substrat (Simulasi)",
    tooltip="Smart Ajir 02",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(peta)

# Titik distribusi kapsul simulasi
folium.Marker(
    location=[-6.928, 110.500],
    popup="Capsule Distribution Point 01 (Simulasi)",
    tooltip="Capsule 01",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(peta)

# Area prioritas restorasi ilustratif
folium.Circle(
    location=[-6.940, 110.480],
    radius=450,
    color="red",
    fill=True,
    fill_opacity=0.25,
    popup="Priority Restoration Area (Ilustrasi)"
).add_to(peta)

# Tampilkan peta
st_folium(
    peta,
    width=None,
    height=500,
    returned_objects=[]
)
