import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium

# =====================================================
# CAPTRACE 4.0 — FUTURISTIC INTELLIGENCE COMMAND CENTER
# =====================================================

st.set_page_config(
    page_title="CAPTRACE | Intelligence Command Center",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# DESIGN SYSTEM
# =====================================================

GREEN = "#00A884"
DARK = "#063F3A"
NAVY = "#102D3C"
CYAN = "#00B8D9"
GOLD = "#E7B95B"
WHITE = "#FFFFFF"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(0,184,217,0.09),
            transparent 30%
        ),
        radial-gradient(
            circle at 10% 85%,
            rgba(0,168,132,0.07),
            transparent 35%
        ),
        #F4F9FA;
    color: #102D3C;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            165deg,
            #063F3A 0%,
            #082F35 55%,
            #071F2D 100%
        );
    border-right: 1px solid #155E58;
}

[data-testid="stSidebar"] * {
    color: #E9FFFA !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-weight: 600;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 5px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.09);
}

/* HEADINGS */

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #083D3A !important;
    letter-spacing: -0.8px;
}

h1 {
    font-size: 2.6rem !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.7rem !important;
}

p, label, span {
    font-family: 'Inter', sans-serif;
}

/* HEADER */

.hero {
    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(0,220,190,0.25),
            transparent 35%
        ),
        linear-gradient(
            115deg,
            #063F3A,
            #08675C,
            #087E76
        );
    border-radius: 24px;
    padding: 35px 40px;
    color: white;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 15px 35px rgba(6,63,58,0.15);
}

.hero::after {
    content: "";
    position: absolute;
    right: -60px;
    top: -100px;
    width: 320px;
    height: 320px;
    border: 1px solid rgba(255,255,255,0.17);
    border-radius: 50%;
    box-shadow:
        0 0 0 45px rgba(255,255,255,0.035),
        0 0 0 90px rgba(255,255,255,0.025);
    pointer-events: none;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1.5px;
    color: white;
}

.hero-subtitle {
    font-size: 15px;
    color: #C6F6EC;
    margin-top: 8px;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 30px;
    padding: 7px 15px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 16px;
    color: #FFFFFF;
}

/* METRIC CARDS */

[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F8FFFD
        );
    border: 1px solid #D9EAE6;
    border-radius: 20px;
    padding: 24px;
    box-shadow:
        0 8px 28px rgba(9,70,65,0.055);
    transition: transform 0.25s ease;
    min-height: 145px;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #00A884;
}

[data-testid="stMetricLabel"] {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.4px;
    color: #526E70;
}

[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 34px;
    font-weight: 700;
    color: #07584F;
}

[data-testid="stMetricDelta"] {
    font-size: 12px;
}

/* PANELS */

[data-testid="stPlotlyChart"] {
    background: white;
    border: 1px solid #E0ECE9;
    border-radius: 20px;
    padding: 12px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.025);
}

/* BUTTONS */

.stButton > button {
    background: linear-gradient(
        110deg,
        #087D70,
        #00A884
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(0,168,132,0.15);
}

.stButton > button:hover {
    background: #065F55;
    color: white;
    border: none;
}

/* INPUTS */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: white;
    border-radius: 12px;
    border-color: #D5E7E3;
}

/* TABS */

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 600;
}

/* CUSTOM COMPONENTS */

.section-label {
    color: #078C7B;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 7px;
}

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    color: #083D3A;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
}

.tech-panel {
    background: white;
    border: 1px solid #DDECE8;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.025);
}

.tech-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    color: #008F7A;
    font-weight: 700;
}

.tech-title {
    font-size: 15px;
    color: #173F43;
    font-weight: 700;
}

.tech-description {
    color: #587477;
    font-size: 13px;
    line-height: 1.8;
}

.status-pill {
    display: inline-block;
    background: #DDF8F0;
    color: #087B66;
    padding: 7px 14px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.7px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #DDECE8;
    border-radius: 15px;
    overflow: hidden;
}

hr {
    border-color: #DCEAE7 !important;
}

@media (max-width: 768px) {
    .hero {
        padding: 24px;
    }
    .hero-title {
        font-size: 30px;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# DATA
# =====================================================

rng = np.random.default_rng(42)

zones = [
    "Z1 - Coastal",
    "Z2 - Transition",
    "Z3 - Inland"
]

species = [
    "Rhizophora mucronata",
    "Rhizophora apiculata",
    "Avicennia marina",
    "Avicennia alba",
    "Sonneratia alba"
]

sensor_data = pd.DataFrame({
    "Sensor ID": [f"AJR-{i:03d}" for i in range(1, 25)],
    "Zone": rng.choice(zones, 24),
    "Temperature": np.round(rng.uniform(27, 33, 24), 1),
    "Salinity": np.round(rng.uniform(10, 32, 24), 1),
    "pH": np.round(rng.uniform(6.5, 8.2, 24), 2),
    "Moisture": np.round(rng.uniform(55, 90, 24), 1)
})

capsule_data = pd.DataFrame({
    "Capsule ID": [f"CAP-{i:04d}" for i in range(1, 101)],
    "Zone": rng.choice(zones, 100),
    "Species": rng.choice(species, 100),
    "Status": rng.choice(
        ["Distributed", "Monitoring", "Established"],
        100
    )
})

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

performance = pd.DataFrame({
    "Month": months,
    "Vegetation Health": [42, 47, 51, 56, 62, 68],
    "Capsule Establishment": [20, 29, 38, 46, 53, 61],
    "Restoration Coverage": [15, 22, 34, 45, 58, 72]
})

# =====================================================
# FUNCTIONS
# =====================================================

def section(label, title):
    st.markdown(
        f"""
        <div class="section-label">{label}</div>
        <div class="section-heading">{title}</div>
        """,
        unsafe_allow_html=True
    )


def tech_card(number, title, description):
    st.markdown(
        f"""
        <div class="tech-panel">
            <div class="tech-number">{number}</div>
            <div class="tech-title">{title}</div>
            <div class="tech-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def chart_style(fig, height=350):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter",
            color="#294E53"
        ),
        margin=dict(l=25, r=25, t=30, b=25),
        legend=dict(
            orientation="h",
            y=-0.2
        ),
        hoverlabel=dict(
            bgcolor="#073F3A",
            font_color="white"
        )
    )
    return fig


def make_map(show_sensors=True, show_capsules=True, show_zones=True):

    m = folium.Map(
        location=[-6.94, 110.48],
        zoom_start=12,
        tiles="CartoDB positron"
    )

    if show_zones:
        folium.Circle(
            location=[-6.94, 110.48],
            radius=1100,
            color="#E7B95B",
            weight=2,
            fill=True,
            fill_color="#E7B95B",
            fill_opacity=0.10,
            tooltip="Restoration Planning Area"
        ).add_to(m)

    if show_sensors:
        for i in range(12):
            lat = -6.94 + rng.uniform(-0.015, 0.015)
            lon = 110.48 + rng.uniform(-0.015, 0.015)

            folium.CircleMarker(
                [lat, lon],
                radius=7,
                color="#008F7A",
                fill=True,
                fill_color="#00A884",
                fill_opacity=0.9,
                popup=f"Smart Ajir AJR-{i+1:03d}",
                tooltip=f"Smart Ajir {i+1}"
            ).add_to(m)

    if show_capsules:
        for i in range(15):
            lat = -6.94 + rng.uniform(-0.02, 0.02)
            lon = 110.48 + rng.uniform(-0.02, 0.02)

            folium.CircleMarker(
                [lat, lon],
                radius=5,
                color="#008DB0",
                fill=True,
                fill_color="#00B8D9",
                fill_opacity=0.85,
                popup=f"Capsule Site {i+1}",
                tooltip=f"Capsule Site {i+1}"
            ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="
        padding:18px 5px 22px 5px;
    ">
        <div style="
            font-family:'Space Grotesk';
            font-size:29px;
            font-weight:700;
            letter-spacing:1px;
            color:white;
        ">
            CAPTRACE
        </div>

        <div style="
            font-size:10px;
            letter-spacing:2px;
            color:#91D8C9;
            margin-top:5px;
        ">
            INTELLIGENCE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    menu = st.radio(
        "SYSTEM NAVIGATION",
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
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <div style="padding:15px 5px">
        <div style="
            font-size:11px;
            color:#8FD6C6;
            letter-spacing:1.5px;
        ">
            OPERATIONAL REGION
        </div>
        <div style="
            font-size:14px;
            font-weight:700;
            color:white;
            margin-top:7px;
        ">
            SAYUNG, DEMAK
        </div>
        <div style="
            font-size:11px;
            color:#A3D9D0;
            margin-top:4px;
        ">
            CENTRAL JAVA, INDONESIA
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# HERO
# =====================================================

st.markdown(f"""
<div class="hero">
    <div class="hero-tag">
        ENVIRONMENTAL INTELLIGENCE SYSTEM
    </div>
    <div class="hero-title">
        {menu}
    </div>
    <div class="hero-subtitle">
        CAPTRACE | Integrated Mangrove Restoration
        & Conservation Intelligence
    </div>
    <div style="margin-top:20px">
        <span style="
            background:rgba(255,255,255,0.12);
            border:1px solid rgba(255,255,255,0.25);
            border-radius:30px;
            padding:7px 14px;
            font-size:11px;
            color:white;
        ">
            SAYUNG COASTAL REGION
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# COMMAND CENTER
# =====================================================

if menu == "Command Center":

    section("SYSTEM OVERVIEW", "Conservation Intelligence Overview")

    a, b, c, d = st.columns(4)

    a.metric("MANGROVE HEALTH INDEX", "68%", "+4.2%")
    b.metric("SMART AJIR NETWORK", "24", "Registered")
    c.metric("CAPSULE DISTRIBUTION", "1,250", "+150")
    d.metric("RESTORATION ZONES", "03", "Monitored")

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:
        section("PERFORMANCE", "Restoration Development")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=months,
            y=performance["Vegetation Health"],
            mode="lines+markers",
            name="Vegetation Health",
            line=dict(color=GREEN, width=4),
            marker=dict(size=9),
            fill="tozeroy",
            fillcolor="rgba(0,168,132,0.08)"
        ))

        fig.add_trace(go.Scatter(
            x=months,
            y=performance["Capsule Establishment"],
            mode="lines+markers",
            name="Capsule Establishment",
            line=dict(color=CYAN, width=3),
            marker=dict(size=8)
        ))

        fig = chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        section("ECOSYSTEM STATUS", "Vegetation Classification")

        fig = go.Figure(data=[
            go.Pie(
                labels=[
                    "Healthy",
                    "Moderate",
                    "Degraded",
                    "Open Area"
                ],
                values=[68, 17, 10, 5],
                hole=0.72,
                marker=dict(
                    colors=[
                        GREEN,
                        GOLD,
                        CYAN,
                        "#DDE9E6"
                    ]
                ),
                textinfo="percent",
                textposition="outside"
            )
        ])

        fig = chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.write("")

    section("GEOSPATIAL INTELLIGENCE", "Coastal Restoration Network")

    st_folium(
        make_map(),
        width=None,
        height=430,
        returned_objects=[]
    )

    st.write("")

    section("NETWORK STATUS", "Smart Ajir Registry")

    st.dataframe(
        sensor_data.head(8),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# UAV INTELLIGENCE
# =====================================================

elif menu == "UAV Intelligence":

    section("AERIAL OPERATIONS", "UAV Mission Configuration")

    a, b, c = st.columns(3)

    mission = a.selectbox(
        "Mission Type",
        [
            "Vegetation Mapping",
            "Capsule Distribution",
            "Environmental Monitoring"
        ]
    )

    altitude = b.slider(
        "Flight Altitude (m)",
        20, 150, 60
    )

    coverage = c.slider(
        "Coverage Area (ha)",
        1, 100, 25
    )

    st.write("")

    x, y, z = st.columns(3)

    x.metric("FLIGHT ALTITUDE", f"{altitude} m")
    y.metric("TARGET COVERAGE", f"{coverage} ha")
    z.metric("MISSION SEGMENTS", max(1, coverage // 5))

    st.write("")

    section("MISSION INTELLIGENCE", "Flight Planning")

    if st.button("Generate Mission Configuration"):

        st.success("Mission configuration generated.")

        tech_card(
            "01",
            "Selected Mission",
            mission
        )

        tech_card(
            "02",
            "Flight Parameters",
            f"Altitude: {altitude} m | Coverage: {coverage} ha"
        )

        tech_card(
            "03",
            "Mission Planning",
            "Conceptual mission segments have been generated."
        )

# =====================================================
# CAPSULE TRACKING
# =====================================================

elif menu == "Capsule Tracking":

    section("TRACEABILITY NETWORK", "Capsule Distribution System")

    a, b, c = st.columns(3)

    a.metric("REGISTERED CAPSULES", "1,250")
    b.metric("MONITORING RECORDS", "845")
    c.metric("RESTORATION ZONES", "03")

    st.write("")

    left, right = st.columns([2, 1])

    with left:
        search = st.text_input(
            "Search Capsule ID",
            placeholder="CAP-0001"
        )

    with right:
        zone = st.selectbox(
            "Restoration Zone",
            ["All Zones"] + zones
        )

    filtered = capsule_data.copy()

    if search:
        filtered = filtered[
            filtered["Capsule ID"].str.contains(
                search,
                case=False,
                regex=False
            )
        ]

    if zone != "All Zones":
        filtered = filtered[
            filtered["Zone"] == zone
        ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Export Capsule Registry",
        filtered.to_csv(index=False),
        "captrace_capsules.csv",
        "text/csv"
    )

# =====================================================
# SMART AJIR
# =====================================================

elif menu == "Smart Ajir Network":

    section("SENSOR INTELLIGENCE", "Smart Ajir Monitoring Network")

    sensor = st.selectbox(
        "Select Sensor Node",
        sensor_data["Sensor ID"]
    )

    row = sensor_data[
        sensor_data["Sensor ID"] == sensor
    ].iloc[0]

    a, b, c, d = st.columns(4)

    a.metric("TEMPERATURE", f"{row['Temperature']} °C")
    b.metric("SALINITY", f"{row['Salinity']} ppt")
    c.metric("SOIL PH", f"{row['pH']}")
    d.metric("MOISTURE", f"{row['Moisture']}%")

    st.write("")

    section("ENVIRONMENTAL ANALYTICS", "Sensor Parameter Trends")

    days = pd.date_range("2026-11-01", periods=20)

    trend_rng = np.random.default_rng(100)

    trend = pd.DataFrame({
        "Date": days,
        "Temperature": trend_rng.uniform(27, 33, 20),
        "Salinity": trend_rng.uniform(12, 30, 20)
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=trend["Date"],
        y=trend["Temperature"],
        name="Temperature",
        mode="lines+markers",
        line=dict(color=GREEN, width=3)
    ))

    fig.add_trace(go.Scatter(
        x=trend["Date"],
        y=trend["Salinity"],
        name="Salinity",
        mode="lines+markers",
        line=dict(color=CYAN, width=3)
    ))

    st.plotly_chart(
        chart_style(fig, 420),
        use_container_width=True
    )

    section("SENSOR REGISTRY", "Environmental Monitoring Nodes")

    st.dataframe(
        sensor_data,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# GEOSPATIAL EXPLORER
# =====================================================

elif menu == "Geospatial Explorer":

    section("GEOSPATIAL INTELLIGENCE", "Restoration Mapping System")

    layers = st.multiselect(
        "Select Map Layers",
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

    st_folium(
        make_map(
            "Smart Ajir" in layers,
            "Capsule Distribution" in layers,
            "Restoration Zones" in layers
        ),
        width=None,
        height=600,
        returned_objects=[]
    )

# =====================================================
# RESTORATION ANALYSIS
# =====================================================

elif menu == "Restoration Analysis":

    section("DECISION INTELLIGENCE", "Site Suitability Assessment")

    left, right = st.columns(2)

    with left:
        salinity = st.slider(
            "Salinity (ppt)",
            0, 45, 20
        )

        ph = st.slider(
            "Soil pH",
            3.0, 10.0, 7.0
        )

    with right:
        temperature = st.slider(
            "Temperature (°C)",
            20, 40, 29
        )

        inundation = st.selectbox(
            "Inundation",
            ["Low", "Moderate", "High"]
        )

    score = 0

    if 10 <= salinity <= 30:
        score += 30

    if 6 <= ph <= 8.5:
        score += 25

    if 25 <= temperature <= 33:
        score += 25

    if inundation == "Moderate":
        score += 20
    elif inundation == "High":
        score += 10

    st.write("")

    section("ASSESSMENT RESULTS", "Restoration Suitability Index")

    a, b = st.columns([1, 2])

    with a:
        st.metric("SUITABILITY SCORE", f"{score}/100")

    with b:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number=dict(
                font=dict(
                    size=48,
                    color=DARK
                )
            ),
            gauge=dict(
                axis=dict(range=[0, 100]),
                bar=dict(color=GREEN),
                bgcolor="#E7F2EF",
                steps=[
                    dict(range=[0, 50], color="#FBE8E5"),
                    dict(range=[50, 75], color="#FFF4D7"),
                    dict(range=[75, 100], color="#DDF7ED")
                ]
            )
        ))

        fig = chart_style(fig, 280)
        st.plotly_chart(fig, use_container_width=True)

    if score >= 75:
        st.success("High suitability")
    elif score >= 50:
        st.info("Moderate suitability")
    else:
        st.warning("Additional site assessment required")

    st.caption(
        "Indicative rule-based scoring; ecological thresholds "
        "require site- and species-specific validation."
    )

# =====================================================
# CONSERVATION ANALYTICS
# =====================================================

elif menu == "Conservation Analytics":

    section("PERFORMANCE INTELLIGENCE", "Conservation Analytics")

    metric = st.selectbox(
        "Select Performance Indicator",
        [
            "Vegetation Health",
            "Capsule Establishment",
            "Restoration Coverage"
        ]
    )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=performance["Month"],
        y=performance[metric],
        marker=dict(
            color=performance[metric],
            colorscale=[
                [0, "#BDEDE0"],
                [1, "#008F7A"]
            ],
            line=dict(width=0)
        ),
        text=performance[metric],
        textposition="outside"
    ))

    fig = chart_style(fig, 450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.download_button(
        "Export Analytics",
        performance.to_csv(index=False),
        "captrace_analytics.csv",
        "text/csv"
    )

# =====================================================
# CPS INTEGRATION
# =====================================================

elif menu == "CPS Integration":

    section("SYSTEM ARCHITECTURE", "Cyber-Physical System Integration")

    stages = [
        (
            "01",
            "CONNECTION",
            "UAV, Smart Ajir, and restoration capsule connectivity."
        ),
        (
            "02",
            "CONVERSION",
            "Environmental data acquisition and transformation."
        ),
        (
            "03",
            "CYBER",
            "Digital data integration and traceability."
        ),
        (
            "04",
            "COGNITION",
            "Restoration intelligence and decision support."
        ),
        (
            "05",
            "CONFIGURATION",
            "Adaptive restoration planning and management."
        )
    ]

    for number, title, description in stages:
        tech_card(number, title, description)

# =====================================================
# JAGA MANGROVE
# =====================================================

elif menu == "Jaga Mangrove":

    section("MARITIME ECOTOURISM", "Jaga Mangrove Experience")

    tabs = st.tabs([
        "Ecotourism",
        "Community Business",
        "Digital Education",
        "Conservation"
    ])

    with tabs[0]:
        tech_card(
            "01",
            "Mangrove Discovery",
            "Guided ecological exploration and coastal interpretation."
        )

    with tabs[1]:
        tech_card(
            "02",
            "Community Business Tourism",
            "Community-led tourism enterprises and local value creation."
        )

    with tabs[2]:
        tech_card(
            "03",
            "Digital Interpretation",
            "Interactive education integrating mangrove ecology and CAPTRACE."
        )

    with tabs[3]:
        tech_card(
            "04",
            "Participatory Restoration",
            "Community participation in mangrove restoration and stewardship."
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

with st.expander("Data Sources & Methodology"):
    st.caption(
        "Dashboard indicators and mapped device locations currently "
        "use illustrative datasets. Live monitoring requires "
        "integration with field devices and validated observations."
    )

st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    color:#6C8988;
    font-size:11px;
    letter-spacing:1px;
">
    CAPTRACE | CONSERVATION INTELLIGENCE SYSTEM
    <br>
    SAYUNG COASTAL RESTORATION INITIATIVE
</div>
""", unsafe_allow_html=True)
