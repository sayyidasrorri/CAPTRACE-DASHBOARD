import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="CAPTRACE | Conservation Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# DESIGN SYSTEM
# ==============================

GREEN = "#167D65"
DARK_GREEN = "#104D42"
BLUE = "#247BA0"
GOLD = "#D6A94B"
BG = "#F5F8F7"

st.markdown("""
<style>
.stApp {
    background-color: #F5F8F7;
    color: #173B35;
}
[data-testid="stSidebar"] {
    background: #EAF3EF;
}
[data-testid="stSidebar"] * {
    color: #173B35;
}
h1, h2, h3 {
    color: #104D42 !important;
    font-family: 'Arial', sans-serif;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E0EAE5;
    box-shadow: 0 3px 12px rgba(0,0,0,0.035);
}
div[data-testid="stMetricLabel"] {
    color: #56736B;
}
div[data-testid="stMetricValue"] {
    color: #104D42;
}
.stButton > button {
    background-color: #167D65;
    color: white;
    border-radius: 9px;
    border: none;
}
.stButton > button:hover {
    background-color: #104D42;
    color: white;
}
div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 14px;
}
[data-testid="stHeader"] {
    background-color: #F5F8F7;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# DATA PROTOTYPE
# ==============================

np.random.seed(42)

zones = ["Z1 - Coastal", "Z2 - Transition", "Z3 - Inland"]

sensor_data = pd.DataFrame({
    "Sensor ID": [f"AJR-{i:03d}" for i in range(1, 25)],
    "Zone": np.random.choice(zones, 24),
    "Temperature": np.round(np.random.uniform(27, 33, 24), 1),
    "Salinity": np.round(np.random.uniform(10, 32, 24), 1),
    "pH": np.round(np.random.uniform(6.5, 8.2, 24), 2),
    "Moisture": np.round(np.random.uniform(55, 90, 24), 1)
})

capsule_data = pd.DataFrame({
    "Capsule ID": [f"CAP-{i:04d}" for i in range(1, 101)],
    "Zone": np.random.choice(zones, 100),
    "Species": np.random.choice([
        "Rhizophora mucronata",
        "Rhizophora apiculata",
        "Avicennia marina",
        "Avicennia alba",
        "Sonneratia alba"
    ], 100),
    "Status": np.random.choice([
        "Distributed", "Monitoring", "Established"
    ], 100)
})

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:
    st.markdown("## CAPTRACE")
    st.caption("CONSERVATION INTELLIGENCE SYSTEM")
    st.divider()

    menu = st.radio(
        "NAVIGATION",
        [
            "Command Center",
            "UAV Intelligence",
            "Capsule Tracking",
            "Smart Ajir Network",
            "Geospatial Explorer",
            "Restoration Analysis",
            "Conservation Analytics",
            "CPS Integration",
            "Jaga Mangrove"
        ]
    )

    st.divider()
    st.caption("SAYUNG | DEMAK | INDONESIA")
    st.caption("PROTOTYPE MODE")

# ==============================
# HEADER
# ==============================

st.title("CAPTRACE")
st.markdown("### Mangrove Conservation Intelligence System")
st.caption("Integrated Restoration Monitoring & Traceability Platform")
st.divider()

# ==============================
# COMMAND CENTER
# ==============================

if menu == "Command Center":

    st.subheader("Conservation Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Mangrove Health Index", "68%", "+4.2%")
    c2.metric("Smart Ajir Network", "24", "Active")
    c3.metric("Capsule Distribution", "1,250", "+150")
    c4.metric("Restoration Zones", "3", "Monitored")

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("Restoration Performance")

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=months,
            y=[42, 47, 51, 56, 62, 68],
            mode="lines+markers",
            name="Mangrove Health",
            line=dict(color=GREEN, width=4)
        ))

        fig.update_layout(
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Vegetation Classification")

        fig = px.pie(
            names=["Healthy", "Moderate", "Degraded", "Open Area"],
            values=[68, 17, 10, 5],
            hole=0.6,
            color_discrete_sequence=[
                GREEN, GOLD, BLUE, "#DCE7E2"
            ]
        )

        fig.update_layout(
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Network Overview")
    st.dataframe(sensor_data.head(8), use_container_width=True)

# ==============================
# UAV INTELLIGENCE
# ==============================

elif menu == "UAV Intelligence":

    st.subheader("UAV Mission Control")

    a, b, c = st.columns(3)

    mission = a.selectbox(
        "Mission Type",
        ["Vegetation Mapping", "Capsule Distribution", "Monitoring"]
    )

    altitude = b.slider("Flight Altitude (m)", 20, 150, 60)
    coverage = c.slider("Coverage Area (ha)", 1, 100, 25)

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Flight Altitude", f"{altitude} m")
    c2.metric("Coverage Area", f"{coverage} ha")
    c3.metric("Mission Status", "Ready")

    st.subheader("Mission Configuration")

    st.write("Selected Mission:", mission)

    if st.button("Generate Mission Plan"):
        st.success("Mission configuration generated.")
        st.write("Estimated flight segments:", max(1, coverage // 5))
        st.write("Recommended altitude:", altitude, "meters")

# ==============================
# CAPSULE TRACKING
# ==============================

elif menu == "Capsule Tracking":

    st.subheader("Capsule Traceability System")

    c1, c2, c3 = st.columns(3)

    c1.metric("Registered Capsules", "1,250")
    c2.metric("Monitoring Records", "845")
    c3.metric("Restoration Zones", "3")

    st.divider()

    search = st.text_input(
        "Search Capsule ID",
        placeholder="Example: CAP-0001"
    )

    selected_zone = st.selectbox(
        "Filter by Zone",
        ["All Zones"] + zones
    )

    filtered = capsule_data.copy()

    if search:
        filtered = filtered[
            filtered["Capsule ID"].str.contains(
                search, case=False, regex=False
            )
        ]

    if selected_zone != "All Zones":
        filtered = filtered[filtered["Zone"] == selected_zone]

    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        "Export Capsule Records",
        filtered.to_csv(index=False),
        "capsule_records.csv",
        "text/csv"
    )

# ==============================
# SMART AJIR NETWORK
# ==============================

elif menu == "Smart Ajir Network":

    st.subheader("Environmental Sensor Network")

    sensor = st.selectbox(
        "Select Smart Ajir",
        sensor_data["Sensor ID"]
    )

    row = sensor_data[
        sensor_data["Sensor ID"] == sensor
    ].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Temperature", f"{row['Temperature']} °C")
    c2.metric("Salinity", f"{row['Salinity']} ppt")
    c3.metric("Soil pH", row["pH"])
    c4.metric("Moisture", f"{row['Moisture']}%")

    st.divider()

    st.subheader("Environmental Parameter Trends")

    days = pd.date_range("2026-11-01", periods=15)

    trend = pd.DataFrame({
        "Date": days,
        "Temperature": np.random.uniform(27, 33, 15),
        "Salinity": np.random.uniform(12, 30, 15)
    })

    fig = px.line(
        trend,
        x="Date",
        y=["Temperature", "Salinity"],
        color_discrete_sequence=[GREEN, BLUE]
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sensor Registry")
    st.dataframe(sensor_data, use_container_width=True)

# ==============================
# GEOSPATIAL EXPLORER
# ==============================

elif menu == "Geospatial Explorer":

    st.subheader("Mangrove Restoration Geospatial Explorer")

    layer = st.multiselect(
        "Map Layers",
        [
            "Smart Ajir",
            "Capsule Distribution",
            "Restoration Zones"
        ],
        default=[
            "Smart Ajir",
            "Capsule Distribution",
            "Restoration Zones"
        ]
    )

    m = folium.Map(
        location=[-6.94, 110.48],
        zoom_start=12,
        tiles="CartoDB positron"
    )

    if "Smart Ajir" in layer:
        for i in range(12):
            folium.CircleMarker(
                location=[
                    -6.94 + np.random.uniform(-0.015, 0.015),
                    110.48 + np.random.uniform(-0.015, 0.015)
                ],
                radius=6,
                color=GREEN,
                fill=True,
                popup=f"Smart Ajir {i+1}"
            ).add_to(m)

    if "Capsule Distribution" in layer:
        for i in range(15):
            folium.CircleMarker(
                location=[
                    -6.94 + np.random.uniform(-0.02, 0.02),
                    110.48 + np.random.uniform(-0.02, 0.02)
                ],
                radius=4,
                color=BLUE,
                fill=True,
                popup=f"Capsule Site {i+1}"
            ).add_to(m)

    if "Restoration Zones" in layer:
        folium.Circle(
            location=[-6.94, 110.48],
            radius=1100,
            color=GOLD,
            fill=True,
            fill_opacity=0.12,
            popup="Restoration Planning Area"
        ).add_to(m)

    st_folium(m, width=None, height=550)

# ==============================
# RESTORATION ANALYSIS
# ==============================

elif menu == "Restoration Analysis":

    st.subheader("Site Suitability Assessment")

    c1, c2 = st.columns(2)

    with c1:
        salinity = st.slider("Salinity (ppt)", 0, 45, 20)
        ph = st.slider("Soil pH", 3.0, 10.0, 7.0)

    with c2:
        temperature = st.slider("Temperature (°C)", 20, 40, 29)
        inundation = st.selectbox(
            "Inundation",
            ["Low", "Moderate", "High"]
        )

    score = 0

    if 10 <= salinity <= 30:
        score += 30

    if 6.0 <= ph <= 8.5:
        score += 25

    if 25 <= temperature <= 33:
        score += 25

    if inundation == "Moderate":
        score += 20
    elif inundation == "High":
        score += 10

    st.divider()

    st.metric("Site Suitability Score", f"{score}/100")

    st.progress(score / 100)

    if score >= 75:
        st.success("High suitability under the selected scenario.")
    elif score >= 50:
        st.info("Moderate suitability under the selected scenario.")
    else:
        st.warning("Further site assessment recommended.")

    st.caption(
        "Conceptual rule-based assessment. Species-specific "
        "suitability requires field validation."
    )

# ==============================
# CONSERVATION ANALYTICS
# ==============================

elif menu == "Conservation Analytics":

    st.subheader("Conservation Performance Analytics")

    metric = st.selectbox(
        "Select Indicator",
        [
            "Vegetation Health",
            "Capsule Establishment",
            "Restoration Coverage"
        ]
    )

    data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Vegetation Health": [42, 47, 51, 56, 62, 68],
        "Capsule Establishment": [20, 29, 38, 46, 53, 61],
        "Restoration Coverage": [15, 22, 34, 45, 58, 72]
    })

    fig = px.bar(
        data,
        x="Month",
        y=metric,
        color_discrete_sequence=[GREEN]
    )

    fig.update_layout(template="plotly_white", height=450)

    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download Analytics",
        data.to_csv(index=False),
        "conservation_analytics.csv",
        "text/csv"
    )

# ==============================
# CPS INTEGRATION
# ==============================

elif menu == "CPS Integration":

    st.subheader("Cyber-Physical System Architecture")

    stages = {
        "Connection": "UAV, Capsule, Smart Ajir and sensor connectivity.",
        "Conversion": "Environmental data processing and transformation.",
        "Cyber": "Centralized digital monitoring and traceability.",
        "Cognition": "Restoration analysis and decision support.",
        "Configuration": "Adaptive restoration planning and management."
    }

    selected = st.selectbox(
        "Explore CPS Layer",
        list(stages.keys())
    )

    st.info(stages[selected])

    st.divider()

    st.subheader("CAPTRACE Technology Integration")

    st.markdown("""
    **UAV Mapping and Distribution**

    ↓

    **Biodegradable Restoration Capsule**

    ↓

    **Smart Ajir Environmental Monitoring**

    ↓

    **Digital Data Integration**

    ↓

    **Restoration Decision Support**
    """)

# ==============================
# JAGA MANGROVE
# ==============================

elif menu == "Jaga Mangrove":

    st.subheader("Jaga Mangrove")

    st.markdown(
        "### Community Business Tourism & Maritime Ecotourism"
    )

    tabs = st.tabs([
        "Ecotourism",
        "Community Business",
        "Education",
        "Conservation"
    ])

    with tabs[0]:
        st.subheader("Mangrove Discovery Experience")
        st.write(
            "Interpretive mangrove trails, maritime landscape "
            "exploration and guided ecological experiences."
        )

    with tabs[1]:
        st.subheader("Community Enterprise")
        st.write(
            "Local guiding services, community-managed tourism "
            "products and conservation-based entrepreneurship."
        )

    with tabs[2]:
        st.subheader("Digital Conservation Education")
        st.write(
            "Interactive learning about mangrove ecology, "
            "CAPTRACE technology and coastal restoration."
        )

    with tabs[3]:
        st.subheader("Participatory Restoration")
        st.write(
            "Community involvement in mangrove restoration, "
            "monitoring and long-term ecosystem stewardship."
        )

# ==============================
# FOOTER
# ==============================

st.divider()

with st.expander("Data Information"):
    st.write(
        "This application is a conceptual CAPTRACE prototype. "
        "Displayed monitoring records and performance values "
        "are illustrative, not live field measurements."
    )

st.caption(
    "CAPTRACE | Mangrove Conservation Intelligence System"
)
