import base64
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import math
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='CAPTRACE | Digital Ecosystem', layout='wide', initial_sidebar_state='expanded')
ROOT = Path(__file__).resolve().parent
LOGO = ROOT / 'captrace_logo.png'
ASSETS = ROOT / 'captrace_assets'
EMERALD='#08A88A'; CYAN='#09C8DD'; INK='#092C37'; GOLD='#E5B85C'

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Oxanium:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {color-scheme:light} html,body,[class*="css"],.stApp{font-family:'Manrope',sans-serif!important}
.stApp{background:radial-gradient(ellipse at 90% 0%,#d6f9f5 0%,transparent 34%),radial-gradient(ellipse at 5% 65%,#e6f4ff 0%,transparent 40%),#f3f8fa;color:#123746}
.stApp:before{content:'';position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(#0b7f8410 1px,transparent 1px),linear-gradient(90deg,#0b7f8410 1px,transparent 1px);background-size:36px 36px;mask-image:linear-gradient(to bottom,#0007,transparent 80%)}
.block-container{padding-top:1.2rem;max-width:1540px}
[data-testid="stSidebar"]{background:linear-gradient(160deg,#062f35,#064f4c 55%,#072d3a);border-right:1px solid #19b8ac66}
[data-testid="stSidebar"] *{color:#eafff9!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{padding:9px 10px;border-radius:10px;transition:background .25s}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#ffffff18}
[data-testid="stSidebar"] [data-testid="stImage"]{background:white;border-radius:14px;padding:12px;margin:8px 0 18px}
h1,h2,h3{font-family:'Sora',sans-serif!important;letter-spacing:.2px;color:#073b41!important;font-weight:700!important}
[data-testid="stMetric"]{border:1px solid #b7e3df;background:linear-gradient(135deg,#ffffffed,#e9fffae6);border-radius:18px;padding:20px 18px;box-shadow:0 12px 32px #0a615414;transition:transform .25s,border-color .25s;min-height:140px}
[data-testid="stMetric"]:hover{transform:translateY(-5px);border-color:#0ec6a9}
[data-testid="stMetricLabel"]{color:#497077!important;font-size:12px!important;font-weight:700;letter-spacing:1px}
[data-testid="stMetricValue"]{color:#08645b!important;font-family:'Sora',sans-serif;font-size:38px!important;font-weight:700}
[data-testid="stPlotlyChart"]{background:#ffffffde;border:1px solid #d7eceb;border-radius:18px;padding:7px;box-shadow:0 8px 30px #164a4a0a}
.stButton button,.stDownloadButton button{background:linear-gradient(100deg,#076b66,#06ad96);border:0;color:white!important;border-radius:12px;padding:10px 22px;font-weight:700;box-shadow:0 5px 17px #009b8338;transition:transform .2s}
.stButton button:hover,.stDownloadButton button:hover{transform:translateY(-2px);background:#045a57}
[data-testid="stDataFrame"]{border:1px solid #d3e9e6;border-radius:14px;overflow:hidden}
.hero{position:relative;overflow:hidden;padding:30px 36px;margin-bottom:24px;background:linear-gradient(115deg,#063d40,#056b67 58%,#08a5a0);border-radius:24px;color:white;box-shadow:0 20px 44px #056f6a2d;isolation:isolate}
.hero:before{content:'';position:absolute;right:-80px;top:-150px;width:480px;height:480px;border-radius:50%;border:1px solid #ffffff70;box-shadow:0 0 0 42px #ffffff0c,0 0 0 85px #ffffff0b,0 0 0 128px #ffffff0a;animation:orbit 12s ease-in-out infinite alternate;z-index:-1}
.hero:after{content:'';position:absolute;right:12%;top:22%;height:8px;width:8px;background:#9dfff0;border-radius:50%;box-shadow:0 0 30px 10px #8affea8a;animation:beacon 2.5s infinite}
.hero .eyebrow{font-size:11px;letter-spacing:3px;font-weight:800;color:#a8fff1}
.hero .title{font-family:'Sora',sans-serif;font-size:clamp(34px,4.3vw,62px);font-weight:700;line-height:1.05;margin:9px 0;color:white}
.hero .sub{font-size:14px;color:#d6fffa;max-width:700px}
.hero .tags{display:flex;gap:9px;flex-wrap:wrap;margin-top:22px}
.hero .tags span{border:1px solid #b2fff66b;border-radius:99px;background:#ffffff17;padding:7px 12px;font-size:11px;font-weight:700;letter-spacing:1px}
.panel{border:1px solid #cce9e5;background:linear-gradient(140deg,#ffffffee,#f2fffc);border-radius:19px;padding:22px;margin:8px 0 20px;box-shadow:0 10px 30px #165e5612}
.panel h4{font-family:'Sora',sans-serif;font-size:24px;font-weight:700;color:#07544f;margin:0 0 8px}
.panel p{color:#52747b;font-size:13px;margin:0;line-height:1.7}
.kicker{font-size:11px;font-weight:800;letter-spacing:2.5px;color:#078b7c;margin:17px 0 2px}
.flow{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:14px 0 26px}
.flow .node{flex:1;min-width:145px;background:linear-gradient(140deg,#e4fff8,#fff);border:1px solid #a9e6dc;border-radius:14px;padding:15px;text-align:center;color:#075a58;font-family:'Sora';font-size:19px;font-weight:700;transition:transform .2s}
.flow .node:hover{transform:translateY(-5px)}
.flow .arrow{color:#08a88a;font-size:26px;font-weight:900}
.pulse{display:inline-block;width:8px;height:8px;background:#38ffcc;border-radius:50%;box-shadow:0 0 0 5px #38ffcc24;animation:beacon 2s infinite;margin-right:7px}
@keyframes orbit{to{transform:translate(-28px,30px) scale(1.09)}}@keyframes beacon{50%{opacity:.45;box-shadow:0 0 0 13px #38ffcc00}}
@media(prefers-reduced-motion:reduce){.hero:before,.hero:after,.pulse{animation:none!important}}
@media(max-width:700px){.hero{padding:23px 20px}.hero .title{font-size:34px}.flow .arrow{display:none}}

/* CAPTRACE 7.0 — Earth observation mission-control layer */
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 75% 2%,#b9e8f12b,transparent 27%),#f3f8fa}
[data-testid="stSidebar"]{box-shadow:inset -1px 0 #39e9d633}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:linear-gradient(100deg,#15d9b12c,#4feaff12);border-left:3px solid #49f2d1}
[data-testid="stMetric"]{position:relative;overflow:hidden}
[data-testid="stMetric"]:before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:linear-gradient(#2bf0cd,#098d8c)}
.hero{min-height:225px;background:radial-gradient(circle at 85% 40%,#0cb9b055,transparent 30%),linear-gradient(115deg,#062e40,#075e64 52%,#0b8e89)}
.hero .title{font-size:clamp(30px,3.4vw,52px);max-width:850px;letter-spacing:-1.5px}
.hero:before{animation:orbit 9s linear infinite alternate}
.hero .scanline{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,transparent 47%,#7cfff720 50%,transparent 53%);background-size:100% 190px;animation:scan 7s linear infinite}
.hero .orbitlabel{position:absolute;right:45px;bottom:25px;border:1px solid #9dffef5c;border-radius:50%;width:112px;height:112px;display:flex;align-items:center;justify-content:center;color:#d6fff5;font-size:10px;letter-spacing:2px;text-align:center;animation:spin 24s linear infinite}
.mission-strip{display:flex;flex-wrap:wrap;gap:8px;margin:-6px 0 22px}
.mission-chip{background:#fff;border:1px solid #d3ebe8;border-radius:10px;padding:10px 13px;flex:1;min-width:145px;box-shadow:0 3px 15px #0a5a5510}
.mission-chip b{display:block;font-size:10px;letter-spacing:1.5px;color:#557d80;margin-bottom:4px}
.mission-chip span{font-size:14px;font-weight:800;color:#0a5555}
.radar{height:265px;max-width:350px;aspect-ratio:1;margin:5px auto 15px;border-radius:50%;position:relative;overflow:hidden;background:repeating-radial-gradient(circle,#12ad9923 0 1px,transparent 2px 47px),linear-gradient(135deg,#073f46,#0a6667);border:2px solid #2fc9b1;box-shadow:inset 0 0 45px #001b22,0 14px 30px #0a67632b}
.radar:before{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,transparent 0deg,transparent 265deg,#4dffce12 285deg,#40ffd485 355deg,transparent 360deg);animation:spin 5s linear infinite}
.radar:after{content:"";position:absolute;inset:12%;border-radius:50%;border:1px dashed #70e9da65}
.radar-dot{position:absolute;width:9px;height:9px;background:#a3ffec;border-radius:50%;box-shadow:0 0 12px 5px #46f5cc77;z-index:2}
.radar-center{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:8px;height:8px;border-radius:50%;background:white;z-index:3}
.signal-card{border:1px solid #d1e9e6;border-radius:15px;background:#fff;padding:16px;margin:8px 0}
.signal-card strong{font-family:Sora,sans-serif;color:#0a4c51;font-size:16px}
.signal-card small{display:block;color:#5d7b80;margin-top:7px;line-height:1.6}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes scan{to{background-position:0 190px}}
@media(prefers-reduced-motion:reduce){.hero .scanline,.hero .orbitlabel,.radar:before{animation:none!important}}
@media(max-width:700px){.hero .orbitlabel{display:none}.mission-chip{min-width:130px}}

/* CAPTRACE 9.0 / VISION INTERFACE */
h1,h2,h3,.hero .title,.panel h4,.flow .node{font-family:'Oxanium',sans-serif!important}
.hero{background:radial-gradient(circle at 84% 44%,#1bead044,transparent 29%),linear-gradient(113deg,#041e2f 0%,#064a56 49%,#087c7b 100%);border:1px solid #35f0d35c;box-shadow:0 20px 65px #003f4d35,inset 0 0 55px #00d6bd18}
.hero .title{text-shadow:0 0 22px #2dffe84d;letter-spacing:1px}
.hero:before{border:2px dashed #64ffdd55;box-shadow:0 0 0 30px #17e0c311,0 0 0 70px #13e2c40a,0 0 0 115px #0df8dc08}
[data-testid="stMetric"]{background:linear-gradient(130deg,#ffffff,#e9fdfa);box-shadow:0 12px 35px #044f521a,inset 0 0 0 1px #ffffff}
[data-testid="stMetricValue"]{font-family:'Oxanium',sans-serif!important;letter-spacing:1px}
[data-testid="stSidebar"]{background:linear-gradient(165deg,#041b2c,#063c48 48%,#064e48);}
[data-testid="stSidebar"] [role="radiogroup"] label{font-family:'Space Grotesk',sans-serif;font-size:13px;letter-spacing:.15px}
[data-testid="stPlotlyChart"]{box-shadow:0 12px 36px #0a64621c;border:1px solid #a9dcd8}
.signal-card{background:linear-gradient(135deg,#faffff,#eafff9);border:1px solid #a8e4d9;box-shadow:0 7px 24px #005b5d12}
.vision-banner{padding:17px 22px;border-radius:14px;background:linear-gradient(105deg,#062d3d,#075b60);border:1px solid #25dfc58a;color:#eafffb;margin:8px 0 18px;position:relative;overflow:hidden}
.vision-banner:after{content:'';position:absolute;right:0;top:0;width:36%;height:100%;background:repeating-linear-gradient(90deg,transparent 0 15px,#6bffe914 16px 17px);pointer-events:none}
.vision-banner strong{font-family:Oxanium,sans-serif;font-size:19px;letter-spacing:1px;color:#b7ffed}
.vision-banner small{display:block;color:#c1e9e5;margin-top:5px;font-size:12px;line-height:1.6}
.vision-readout{display:flex;flex-wrap:wrap;gap:9px;margin:10px 0 18px}
.vision-readout span{background:#073b48;color:#a9fff1;border:1px solid #16bda6;border-radius:8px;padding:8px 13px;font:700 12px Oxanium,sans-serif;letter-spacing:1px}
@keyframes shimmer{from{background-position:200% 0}to{background-position:-200% 0}}
.mission-chip{background:linear-gradient(110deg,#fff 25%,#e8fffb 50%,#fff 75%);background-size:200% 100%;animation:shimmer 13s linear infinite}
@media(prefers-reduced-motion:reduce){.mission-chip{animation:none}}

/* CAPTRACE 10 — animated command-grid environment */
@import url('https://fonts.googleapis.com/css2?family=Oxanium:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
[data-testid="stAppViewContainer"]{position:relative;isolation:isolate;background:linear-gradient(130deg,#f2fbfc,#e9f5f6 45%,#f6fbfd)!important}
[data-testid="stAppViewContainer"]::before{
 content:"";position:fixed;inset:0;pointer-events:none;z-index:-1;
 background-image:linear-gradient(90deg,rgba(0,139,148,.12) 1px,transparent 1px),linear-gradient(rgba(0,139,148,.12) 1px,transparent 1px);
 background-size:62px 62px;animation:cap-grid-drift 24s linear infinite;
 mask-image:linear-gradient(110deg,#0009,#0003 75%);
}
[data-testid="stAppViewContainer"]::after{
 content:"";position:fixed;inset:-30%;pointer-events:none;z-index:-1;
 background:radial-gradient(ellipse at 22% 32%,rgba(18,204,184,.14),transparent 32%),radial-gradient(ellipse at 78% 65%,rgba(12,127,203,.12),transparent 34%);
 animation:cap-aurora 18s ease-in-out infinite alternate;
}
@keyframes cap-grid-drift{to{background-position:124px 62px}}
@keyframes cap-aurora{to{transform:translate(7%, -5%) rotate(5deg)}}
[data-testid="stSidebar"]{background:linear-gradient(155deg,#041d31,#073f4c 50%,#07534b)!important}
[data-testid="stSidebar"] [data-testid="stRadio"]{border:1px solid #7fffe21f;border-radius:13px;padding:7px;margin:7px 0 15px;background:#ffffff08}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:10px 11px!important;margin:3px 0;border-radius:10px;transition:background .25s,transform .25s}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:#20cbb52c;transform:translateX(3px)}
.nav-caption{font-family:Oxanium,sans-serif;color:#7cf7df;font-size:11px;font-weight:800;letter-spacing:2px;margin:15px 0 8px}
.hero{background:linear-gradient(110deg,#031c32,#06505d 55%,#087b79)!important}
.hero::before{animation:orbit 9s linear infinite alternate!important}
[data-testid="stMetric"]{backdrop-filter:blur(10px);transition:transform .3s,box-shadow .3s!important}
[data-testid="stMetric"]:hover{transform:translateY(-6px) scale(1.015);box-shadow:0 16px 40px #008f9b25}
@media(prefers-reduced-motion:reduce){[data-testid="stAppViewContainer"]::before,[data-testid="stAppViewContainer"]::after,.hero::before{animation:none!important}}
</style>''',unsafe_allow_html=True)

@st.cache_data
def dataset():
    rng=np.random.default_rng(91)
    z=['Z1 | Coastal','Z2 | Transition','Z3 | Inland']
    sp=['Rhizophora mucronata','Rhizophora apiculata','Avicennia marina','Avicennia alba','Sonneratia alba']
    sensors=pd.DataFrame({'Node':[f'AJR-{i:03d}' for i in range(1,49)],'Zone':rng.choice(z,48),'Temperature (°C)':rng.uniform(27,33,48).round(1),'Salinity (ppt)':rng.uniform(10,32,48).round(1),'pH':rng.uniform(6.4,8.3,48).round(2),'Moisture (%)':rng.uniform(52,93,48).round(1),'Battery (%)':rng.integers(32,100,48),'Status':rng.choice(['Online','Online','Online','Attention'],48)})
    capsules=pd.DataFrame({'Capsule ID':[f'CAP-{i:05d}' for i in range(1,501)],'Zone':rng.choice(z,500),'Species':rng.choice(sp,500),'Stage':rng.choice(['Prepared','Distributed','Monitoring','Established'],500),'Health score':rng.integers(35,99,500)})
    dates=pd.date_range('2026-08-01',periods=110)
    trend=pd.DataFrame({'Date':dates,'Health index':np.clip(43+np.linspace(0,23,110)+rng.normal(0,2,110),0,100),'Restoration coverage':np.clip(18+np.linspace(0,45,110)+rng.normal(0,2.4,110),0,100),'Establishment':np.clip(22+np.linspace(0,38,110)+rng.normal(0,2,110),0,100)})
    return sensors,capsules,trend
sensors,capsules,trend=dataset()

def chart(fig,h=360):
    fig.update_layout(template='plotly_white',height=h,margin=dict(l=20,r=20,t=35,b=20),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='Manrope',color='#31545a'),hoverlabel=dict(bgcolor='#063e42',font_color='white'),legend=dict(orientation='h',y=-.22),xaxis=dict(showgrid=False),yaxis=dict(gridcolor='#e5f1f0'))
    return fig

def section(a,b):
    st.markdown(f'<div class="kicker">{a.upper()}</div><h2 style="margin:0 0 12px">{b}</h2>',unsafe_allow_html=True)

def panel(title,body):
    st.markdown(f'<div class="panel"><h4>{title}</h4><p>{body}</p></div>',unsafe_allow_html=True)

def real_map(layers=None,basemap='OpenStreetMap',height=520):
    layers=layers or ['Sensor nodes','Capsule sites','Planning zones']
    tiles={'OpenStreetMap':'OpenStreetMap','Terrain':'CartoDB positron','Satellite':'Esri.WorldImagery'}
    m=folium.Map(location=[-6.943,110.481],zoom_start=12,tiles=None,control_scale=True)
    folium.TileLayer('OpenStreetMap',name='OpenStreetMap',show=basemap=='OpenStreetMap').add_to(m)
    folium.TileLayer('CartoDB positron',name='Terrain',show=basemap=='Terrain').add_to(m)
    folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr='Esri, Maxar, Earthstar Geographics',name='Satellite',show=basemap=='Satellite').add_to(m)
    # Reference coordinates for map visualization only, NOT measured installation locations.
    points=np.random.default_rng(11)
    if 'Planning zones' in layers:
        g=folium.FeatureGroup(name='Planning zones — illustrative')
        for i,(lat,lon) in enumerate([(-6.935,110.475),(-6.944,110.488),(-6.952,110.475)],1):
            folium.Circle([lat,lon],radius=650,color=['#08a88a','#0bb6d0','#e5b85c'][i-1],weight=2,fill=True,fill_opacity=.10,tooltip=f'Concept zone Z{i}').add_to(g)
        g.add_to(m)
    if 'Sensor nodes' in layers:
        g=folium.FeatureGroup(name='Sensor nodes — illustrative')
        for i in range(25):
            lat=-6.943+points.uniform(-.019,.019);lon=110.481+points.uniform(-.022,.022)
            folium.CircleMarker([lat,lon],radius=6,color='#04715e',fill=True,fill_color='#13d5a7',fill_opacity=.95,tooltip=f'AJR-{i+1:03d} | Concept location').add_to(g)
        g.add_to(m)
    if 'Capsule sites' in layers:
        g=folium.FeatureGroup(name='Capsule sites — illustrative')
        for i in range(36):
            lat=-6.943+points.uniform(-.022,.022);lon=110.481+points.uniform(-.025,.025)
            folium.CircleMarker([lat,lon],radius=4,color='#087ea3',fill=True,fill_color='#12c9ef',fill_opacity=.85,tooltip=f'Capsule reference {i+1}').add_to(g)
        g.add_to(m)
    from folium.plugins import MiniMap, Fullscreen, MeasureControl, MousePosition
    MiniMap(toggle_display=True, position='bottomright').add_to(m)
    Fullscreen(position='topleft').add_to(m)
    MeasureControl(position='topleft', primary_length_unit='meters').add_to(m)
    MousePosition(position='bottomleft', separator=' | ', prefix='Coordinates').add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    st_folium(m,height=height,width=None,returned_objects=[],key=f'map_{st.session_state.page}_{basemap}_{"_".join(layers)}')

PAGES=['Command Center','Drone Camera Studio','Aerial Image Lab','UAV Intelligence','Mission Replay','Capsule Tracking','Smart Ajir Network','Geospatial Explorer','Coastal Risk Monitor','Restoration Analysis','Species Atlas','Conservation Analytics','CPS Integration','Operations Log','Report Generator','Jaga Mangrove']

# Five primary groups; existing sixteen modules remain accessible.
NAV_GROUPS = {
    '01  MISSION CONTROL': ['Command Center', 'UAV Intelligence', 'Mission Replay', 'Operations Log'],
    '02  DRONE & IMAGING': ['Drone Camera Studio', 'Aerial Image Lab', 'Geospatial Explorer'],
    '03  RESTORATION NETWORK': ['Capsule Tracking', 'Smart Ajir Network', 'Restoration Analysis', 'Species Atlas'],
    '04  EARTH INTELLIGENCE': ['Coastal Risk Monitor', 'Conservation Analytics', 'CPS Integration'],
    '05  COMMUNITY & REPORTS': ['Jaga Mangrove', 'Report Generator'],
}

with st.sidebar:
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    else:
        st.markdown('## CAPTRACE')
    st.markdown('<span class="pulse"></span><span style="font-size:11px;letter-spacing:2px">CONSERVATION INTELLIGENCE</span>',unsafe_allow_html=True)
    st.markdown('<div class="nav-caption">PRIMARY SYSTEMS / 05</div>',unsafe_allow_html=True)
    group = st.radio('MAIN SYSTEMS', list(NAV_GROUPS), label_visibility='collapsed', key='nav_group')
    st.markdown('<div class="nav-caption">SELECT MODULE</div>',unsafe_allow_html=True)
    page = st.radio('SUBMODULES', NAV_GROUPS[group], label_visibility='collapsed', key=f'nav_sub_{list(NAV_GROUPS).index(group)}')
    # Preserve compatibility with all existing map and page functions.
    st.session_state['page'] = page
    st.divider()
    zone=st.selectbox('OPERATIONAL FOCUS',['All zones','Z1 | Coastal','Z2 | Transition','Z3 | Inland'])
    st.caption('SAYUNG · DEMAK · CENTRAL JAVA')
    st.caption('05 MAIN SYSTEMS  /  16 MODULES')

st.markdown(f'''<div class="hero"><div class="scanline"></div><div class="orbitlabel">EARTH<br>OBSERVATION</div><div class="eyebrow"><span class="pulse"></span>CAPTRACE / DIGITAL ECOSYSTEM</div><div class="title">{page.upper()}</div><div class="sub">Capsule-Based Traceability System · Mangrove restoration, geospatial intelligence and community-driven maritime ecotourism</div><div class="tags"><span>COASTAL INTELLIGENCE</span><span>CYBER-PHYSICAL SYSTEM</span><span>SAYUNG, DEMAK</span></div></div>''',unsafe_allow_html=True)

st.markdown('''<div class="mission-strip">
<div class="mission-chip"><b>MISSION REGION</b><span>SAYUNG · CENTRAL JAVA</span></div>
<div class="mission-chip"><b>COORDINATE REFERENCE</b><span>6.943° S / 110.481° E</span></div>
<div class="mission-chip"><b>PLATFORM MODULES</b><span>UAV / CAPSULE / IOT / CPS</span></div>
<div class="mission-chip"><b>DATA WORKSPACE</b><span>EXPLORATION & ANALYTICS</span></div>
</div>''',unsafe_allow_html=True)


# ================================================================
# CAPTRACE 8.0 — VISUAL OBSERVATION AND OPERATIONS EXTENSIONS
# ================================================================
def aerial_frame(index=1):
    path=ASSETS/f'aerial_scene_{index}.jpg'
    if path.exists(): return Image.open(path).convert('RGB')
    return Image.new('RGB',(1200,675),'#175c56')

def overlay_camera(img,frame=0,mode='RGB',grid=True):
    """Compose a high-contrast instrument HUD over illustrative or user-supplied imagery."""
    im=img.copy().convert('RGB').resize((1280,720))
    if mode=='Thermal palette':
        im=ImageOps.colorize(ImageOps.grayscale(im),black='#041a39',mid='#ed6d37',white='#fff3b1')
    elif mode=='Vegetation contrast':
        im=ImageEnhance.Color(im).enhance(1.85)
        im=ImageEnhance.Contrast(im).enhance(1.28)
    w,h=im.size
    d=ImageDraw.Draw(im,'RGBA')
    font_dir=Path('/usr/share/fonts/truetype/dejavu')
    def font(size,bold=False):
        p=font_dir/('DejaVuSansMono-Bold.ttf' if bold else 'DejaVuSansMono.ttf')
        try:return ImageFont.truetype(str(p),size)
        except:return ImageFont.load_default()
    sm=font(16);md=font(21,True);lg=font(31,True)
    mint=(102,255,220,240);white=(238,255,250,245);amber=(255,205,111,245)
    # Gradient edge treatment, dark glass command bars and film grain style lines
    d.rectangle((0,0,w,89),fill=(3,22,36,218))
    d.rectangle((0,h-92,w,h),fill=(3,22,36,224))
    d.rectangle((0,89,9,h-92),fill=(0,225,188,175))
    d.rectangle((w-9,89,w,h-92),fill=(0,225,188,175))
    for y in range(102,h-100,42):d.line((15,y,w-15,y),fill=(14,43,49,38),width=1)
    for x in range(28,w-28,70):d.line((x,95,x,h-98),fill=(14,43,49,26),width=1)
    d.text((28,18),'CAPTRACE  /  EARTH OBSERVATION',font=md,fill=white)
    d.text((28,51),'UAV-01  |  VISUAL INTELLIGENCE ARRAY',font=sm,fill=mint)
    d.text((w-335,18),f'FRAME {frame:04d}  /  {mode.upper()}',font=sm,fill=mint)
    d.text((w-335,52),'REPLAY FEED  /  NO LIVE LINK',font=sm,fill=amber)
    d.text((28,h-76),'6.940 S  /  110.480 E',font=md,fill=white)
    d.text((28,h-41),'SAYUNG COASTAL OBSERVATION',font=sm,fill=mint)
    d.text((w-355,h-76),'ALT 065 M   HDG 082 DEG',font=md,fill=white)
    d.text((w-355,h-41),'OPTICAL PAYLOAD  /  SIMULATED',font=sm,fill=amber)
    # targeting reticle with four articulated corners and circular acquisition zone
    cx=int(w/2+22*math.sin(frame/18));cy=int(h/2+14*math.cos(frame/20))
    if grid:
        for x in (w//3,2*w//3):d.line((x,95,x,h-96),fill=(162,255,226,74),width=2)
        for y in (h//3,2*h//3):d.line((13,y,w-13,y),fill=(162,255,226,74),width=2)
        d.ellipse((cx-84,cy-84,cx+84,cy+84),outline=mint,width=3)
        d.ellipse((cx-11,cy-11,cx+11,cy+11),outline=white,width=3)
        d.line((cx-126,cy,cx-28,cy),fill=mint,width=3)
        d.line((cx+28,cy,cx+126,cy),fill=mint,width=3)
        d.line((cx,cy-122,cx,cy-30),fill=mint,width=3)
        d.line((cx,cy+30,cx,cy+122),fill=mint,width=3)
        for x,y,dx,dy in [(52,126,1,1),(w-52,126,-1,1),(52,h-125,1,-1),(w-52,h-125,-1,-1)]:
            d.line((x,y,x+dx*60,y),fill=mint,width=5)
            d.line((x,y,x,y+dy*55),fill=mint,width=5)
    # diagnostic ruler, histogram and radar inset
    for k in range(12):
        y=155+k*30
        d.line((w-47,y,w-47-(22 if k%3==0 else 11),y),fill=mint,width=2)
    for k in range(24):
        bar=int(12+35*abs(math.sin(k*.41+frame*.035)))
        x=33+k*13
        d.rectangle((x,h-117-bar,x+7,h-117),fill=(54,235,196,160))
    rx,ry=110,174
    d.ellipse((rx-48,ry-48,rx+48,ry+48),outline=mint,width=2)
    d.ellipse((rx-24,ry-24,rx+24,ry+24),outline=(102,255,220,125),width=2)
    a=frame*.08
    d.line((rx,ry,rx+int(46*math.cos(a)),ry+int(46*math.sin(a))),fill=mint,width=3)
    d.ellipse((rx+14,ry-19,rx+19,ry-14),fill=amber)
    return im

def downloadable_image(im,name):
    b=BytesIO();im.save(b,format='PNG');st.download_button('Download camera frame (PNG)',b.getvalue(),name,'image/png')

if page=='Drone Camera Studio':
    section('Aerial observation / Camera station','UAV Visual Intelligence Studio')
    st.markdown('<div class="vision-banner"><strong>OPTICAL COMMAND / MULTI-SPECTRAL VIEWER</strong><small>Instrument overlay, target reticle, optical modes and replay timeline. Built-in scenes are generated visual references; upload real imagery in Aerial Image Lab.</small></div>',unsafe_allow_html=True)
    a,b,c,d=st.columns([1.2,1.2,1.2,1])
    scene=a.selectbox('Observation scene',['Coastal transect','Mangrove canopy','Estuary transition'])
    mode=b.selectbox('Camera visualization',['RGB','Vegetation contrast','Thermal palette'])
    zoom=c.slider('Digital zoom',1.0,2.5,1.0,.1)
    grid=d.toggle('Camera reticle',value=True)
    frame=st.slider('Replay frame',0,120,38)
    img=aerial_frame(['Coastal transect','Mangrove canopy','Estuary transition'].index(scene)+1)
    if zoom>1:
        w,h=img.size;nw=int(w/zoom);nh=int(h/zoom);cx=int(w/2+math.sin(frame/13)*45);cy=int(h/2+math.cos(frame/17)*25)
        x=max(0,min(w-nw,cx-nw//2));y=max(0,min(h-nh,cy-nh//2))
        img=img.crop((x,y,x+nw,y+nh)).resize((w,h))
    img=overlay_camera(img,frame,mode,grid)
    st.markdown('<div class="vision-readout"><span>OPTICAL ARRAY / CAM-A</span><span>ACQUISITION HUD</span><span>FRAME RECONSTRUCTION</span><span>GEO REFERENCE: SAYUNG</span></div>',unsafe_allow_html=True)
    st.image(img,use_container_width=True)
    m1,m2,m3,m4=st.columns(4)
    m1.metric('MISSION','UAV-01');m2.metric('ALTITUDE SETPOINT','65 m');m3.metric('CAMERA MODE',mode);m4.metric('REPLAY FRAME',f'{frame:03d}')
    downloadable_image(img,f'captrace_camera_{frame:03d}.png')
    section('Optical payload','Camera sensor specification')
    st.dataframe(pd.DataFrame({'Payload':['Visual RGB','Multispectral','Thermal','GNSS/IMU'], 'Use':['Habitat imagery','Vegetation-index mapping','Surface temperature screening','Georeferencing and orientation'], 'Availability':['Visual mock-up','Requires calibrated imagery','Palette preview only','Requires actual telemetry']}),hide_index=True,use_container_width=True)

elif page=='Aerial Image Lab':
    section('Computer vision / Image processing','Aerial Imagery Analysis Lab')
    uploaded=st.file_uploader('Upload your aerial photo (JPG/PNG)',type=['jpg','jpeg','png'])
    a,b=st.columns([1,1])
    with a:
        image=aerial_frame(2) if uploaded is None else Image.open(uploaded).convert('RGB')
        st.image(overlay_camera(image,16,'RGB',True),caption='Source imagery with acquisition interface',use_container_width=True)
    with b:
        method=st.selectbox('Visualization method',['RGB contrast','Green channel enhancement','Grayscale edge preview','False-color style'])
        strength=st.slider('Enhancement strength',1.0,3.0,1.5,.1)
        if method=='RGB contrast':out=ImageEnhance.Contrast(image).enhance(strength)
        elif method=='Green channel enhancement':
            arr=np.array(image).astype(float);arr[:,:,1]=np.clip(arr[:,:,1]*strength,0,255);out=Image.fromarray(arr.astype('uint8'))
        elif method=='Grayscale edge preview':out=image.convert('L').filter(ImageFilter.FIND_EDGES).convert('RGB')
        else:
            gray=ImageOps.grayscale(image);out=ImageOps.colorize(gray,'#0a3257','#4de0b2')
        st.image(overlay_camera(out,48,'Vegetation contrast' if method=='Green channel enhancement' else 'RGB',True),caption='Enhanced image with instrument interface',use_container_width=True)
    downloadable_image(out,'captrace_image_analysis.png')
    section('Interpretation','Image interpretation guide')
    panel('Scientific interpretation','RGB processing and false-color styling are visual enhancements only. True NDVI requires calibrated near-infrared and red bands; thermal measurement requires an actual thermal sensor.')
    x,y,z=st.columns(3)
    x.metric('IMAGE WIDTH',f'{image.width} px');y.metric('IMAGE HEIGHT',f'{image.height} px');z.metric('IMAGE TYPE','Uploaded' if uploaded else 'Generated')

elif page=='Mission Replay':
    section('Flight reconstruction','UAV Mission Replay & Telemetry')
    progress=st.slider('Mission timeline (%)',0,100,42)
    mission_type=st.selectbox('Replay scenario',['Coastal mapping','Capsule release','Environmental inspection'])
    t=np.linspace(0,100,101);alt=70*np.sin(np.pi*np.minimum(t,100)/100)**.35
    alt=np.maximum(0,alt)
    fig=go.Figure();fig.add_trace(go.Scatter(x=t,y=alt,name='Altitude',line=dict(color=EMERALD,width=4),fill='tozeroy',fillcolor='rgba(8,168,138,.1)'))
    fig.add_vline(x=progress,line_color=GOLD,line_dash='dash');fig.update_layout(xaxis_title='Mission completion (%)',yaxis_title='Altitude (m)')
    st.plotly_chart(chart(fig,340),use_container_width=True)
    a,b,c,d=st.columns(4);a.metric('MISSION PROGRESS',f'{progress}%');b.metric('ALTITUDE',f'{alt[progress]:.1f} m');c.metric('SIMULATED SPEED',f'{12+3*np.sin(progress/12):.1f} m/s');d.metric('MISSION TYPE',mission_type)
    st.markdown('<div class="vision-banner"><strong>FLIGHT RECONSTRUCTION / OPTICAL TELEMETRY</strong><small>Replay frames follow the selected mission progress. This is an interactive visualization, not a live video stream.</small></div>',unsafe_allow_html=True)
    st.image(overlay_camera(aerial_frame(1+min(2,progress//34)),progress,'RGB',True),use_container_width=True)
    panel('Flight replay','Telemetry curve and imagery are synchronized conceptual previews. No actual flight log, GNSS track or recorded video is connected.')

elif page=='Coastal Risk Monitor':
    section('Coastal intelligence','Shoreline & Habitat Risk Studio')
    erosion=st.slider('Illustrative shoreline retreat (m/year)',0.0,15.0,4.5,.5)
    exposure=st.select_slider('Wave exposure',['Low','Moderate','High'])
    vegetation=st.slider('Protective vegetation cover (%)',0,100,48)
    risk=min(100,round(erosion*4+{'Low':10,'Moderate':25,'High':40}[exposure]+(100-vegetation)*.3))
    a,b=st.columns([1,2]);a.metric('SCENARIO RISK INDEX',f'{risk}/100');a.progress(risk/100)
    fig=go.Figure(go.Indicator(mode='gauge+number',value=risk,gauge=dict(axis=dict(range=[0,100]),bar=dict(color='#d69b46'),steps=[dict(range=[0,35],color='#dcf6e9'),dict(range=[35,70],color='#fff0c9'),dict(range=[70,100],color='#f8d9d5')])))
    b.plotly_chart(chart(fig,280),use_container_width=True)
    section('Risk matrix','Planning priorities')
    st.dataframe(pd.DataFrame({'Factor':['Shoreline retreat','Wave exposure','Vegetation cover','Tidal connectivity'],'Scenario input':[f'{erosion} m/year',exposure,f'{vegetation}%','Field verification needed'],'Planning response':['Monitor shoreline profiles','Assess wave energy','Protect suitable vegetation','Verify natural hydrology']}),hide_index=True,use_container_width=True)
    panel('Scenario boundary','The risk index is a planning illustration, not a calibrated hazard forecast or a measured coastal erosion rate.')

elif page=='Species Atlas':
    section('Biodiversity intelligence','Mangrove Species Atlas')
    species_info={
        'Avicennia marina':('Api-api','Pioneer species; often tolerates saline coastal environments.','Inspect tidal elevation, substrate and local reference stands.'),
        'Avicennia alba':('Api-api putih','Frequently associated with seaward intertidal mangrove settings.','Evaluate sediment stability and wave exposure.'),
        'Rhizophora mucronata':('Bakau hitam','Prop-root mangrove often found in sheltered intertidal habitat.','Assess water exchange and muddy substrate.'),
        'Rhizophora apiculata':('Bakau minyak','Mangrove associated with suitable sheltered tidal areas.','Verify inundation regime and substrate.'),
        'Sonneratia alba':('Pidada','Often associated with tidal, sometimes seaward environments.','Assess inundation and sediment dynamics.')}
    chosen=st.selectbox('Explore species',list(species_info));local,ecology,site=species_info[chosen]
    a,b=st.columns([1,1.5])
    with a:
        st.markdown(f'<div class="panel"><h4>{chosen}</h4><p>Local name: {local}</p><p>{ecology}</p></div>',unsafe_allow_html=True)
        st.info(site)
    with b:
        fig=go.Figure(go.Bar(x=['Hydrology','Substrate','Salinity','Wave exposure','Local availability'],y=[5,4,4,3,5],marker_color=[EMERALD,CYAN,EMERALD,GOLD,EMERALD]));fig.update_layout(yaxis_range=[0,6],title='Example site-assessment checklist weights')
        st.plotly_chart(chart(fig,320),use_container_width=True)
    st.caption('Chart weights are illustrative checklists, not measured species tolerance or suitability scores.')

elif page=='Operations Log':
    section('Mission operations','Operations & Event Registry')
    if 'operation_events' not in st.session_state:
        st.session_state.operation_events=[{'Time':'2026-11-18 09:00','Subsystem':'UAV','Event':'Mapping plan drafted','Priority':'Normal'},{'Time':'2026-11-18 10:15','Subsystem':'CPS','Event':'Architecture review','Priority':'Normal'}]
    with st.form('event_form'):
        x,y=st.columns(2);subsystem=x.selectbox('Subsystem',['UAV','Capsule','Smart Ajir','Geospatial','CPS','Community']);priority=y.selectbox('Priority',['Normal','Review','High'])
        event=st.text_input('Event description',max_chars=120)
        submitted=st.form_submit_button('Add event')
    if submitted:
        if event.strip():
            from datetime import datetime
            st.session_state.operation_events.insert(0,{'Time':datetime.now().strftime('%Y-%m-%d %H:%M'),'Subsystem':subsystem,'Event':event.strip(),'Priority':priority})
            st.success('Event added to this browser session.')
        else:st.warning('Enter an event description.')
    logs=pd.DataFrame(st.session_state.operation_events)
    st.dataframe(logs,hide_index=True,use_container_width=True)
    st.download_button('Export operations log',logs.to_csv(index=False),'captrace_operations.csv','text/csv')
    st.caption('Entries are local session notes, not authenticated system telemetry.')

elif page=='Report Generator':
    section('Reporting intelligence','Conservation Brief Generator')
    title=st.text_input('Report title','CAPTRACE Conservation Intelligence Brief')
    selected=st.multiselect('Include sections',['Overview','Sensors','Capsules','Restoration indicators','Recommendations'],default=['Overview','Sensors','Capsules','Restoration indicators'])
    note=st.text_area('Executive note','Monitoring priorities: validate site conditions, sensor installations and restoration observations.')
    lines=[title,'','Location: Sayung, Demak','Source: CAPTRACE interactive workspace','',note,'']
    if 'Overview' in selected:lines+=['OVERVIEW','CAPTRACE integrates UAV, restoration capsules, Smart Ajir and CPS.','']
    if 'Sensors' in selected:lines+=['SENSOR REGISTRY',f'Illustrative sensor records: {len(sensors)}','']
    if 'Capsules' in selected:lines+=['CAPSULE REGISTRY',f'Illustrative capsule records: {len(capsules)}','']
    if 'Restoration indicators' in selected:lines+=['RESTORATION INDICATORS',f'Illustrative index at end of series: {trend["Health index"].iloc[-1]:.1f}','']
    if 'Recommendations' in selected:lines+=['RECOMMENDATIONS','Verify sensor calibration, coordinates, imagery and monitoring methodology before operational reporting.','']
    lines+=['DATA STATUS','This report is based on illustrative dashboard datasets unless replaced by verified field observations.']
    report='\n'.join(lines)
    st.text_area('Report preview',report,height=320)
    st.download_button('Download report (TXT)',report,'captrace_report.txt','text/plain')

if page=='Command Center':
    section('01 / Ecosystem overview','Environmental Intelligence Hub')
    a,b,c,d=st.columns(4)
    a.metric('HEALTH INDEX','68.4%','+4.2 pts');b.metric('SMART AJIR NODES','48','36 online');c.metric('CAPSULE REGISTRY','500','5 species');d.metric('RESTORATION ZONES','03','Z1–Z3')
    l,r=st.columns([1.6,1])
    with l:
        section('Live-style visual analytics','Restoration trajectory')
        fig=go.Figure()
        for col,color in [('Health index',EMERALD),('Restoration coverage',CYAN),('Establishment',GOLD)]:
            fig.add_trace(go.Scatter(x=trend.Date,y=trend[col],mode='lines',name=col,line=dict(color=color,width=3),hovertemplate='%{x|%d %b}: %{y:.1f}%<extra></extra>'))
        st.plotly_chart(chart(fig,390),use_container_width=True)
    with r:
        section('Habitat composition','Mangrove condition')
        fig=go.Figure(go.Pie(labels=['Healthy','Recovering','Degraded','Open'],values=[54,25,14,7],hole=.69,marker_colors=[EMERALD,CYAN,GOLD,'#c5d8d8']))
        st.plotly_chart(chart(fig,390),use_container_width=True)
    section('01B / Observation intelligence','Earth observation & environmental signals')
    tab_a,tab_b,tab_c=st.tabs(['Earth observation','Sensor fusion','Mission events'])
    with tab_a:
        la,ra=st.columns([1.6,1])
        with la:
            grid_rng=np.random.default_rng(210)
            xx=np.linspace(-3,3,55); yy=np.linspace(-3,3,45)
            xxg,yyg=np.meshgrid(xx,yy)
            surface=np.clip(.48+.27*np.exp(-((xxg+1.1)**2+(yyg-.7)**2)/2.4)-.18*np.exp(-((xxg-1.3)**2+(yyg+.7)**2)/1.6)+grid_rng.normal(0,.025,xxg.shape),0,1)
            heat=go.Figure(go.Heatmap(z=surface,x=xx,y=yy,colorscale=[[0,'#d9e8df'],[.3,'#a4d6c4'],[.65,'#4cb99c'],[1,'#075b4f']],colorbar=dict(title='Index'),hovertemplate='Grid X %{x:.1f}<br>Grid Y %{y:.1f}<br>Index %{z:.2f}<extra></extra>'))
            heat.update_layout(title='Conceptual vegetation-index raster · not satellite-derived',xaxis_title='Relative grid X',yaxis_title='Relative grid Y')
            st.plotly_chart(chart(heat,350),use_container_width=True)
        with ra:
            st.markdown('''<div class="signal-card"><strong>Vegetation condition</strong><small>Explore a synthetic raster-style vegetation surface. Connect verified multispectral imagery to calculate actual NDVI or NDRE.</small></div><div class="signal-card"><strong>Coastal change detection</strong><small>Compare shoreline and vegetation boundaries across validated satellite dates before interpreting erosion or recovery.</small></div><div class="signal-card"><strong>Observation pipeline</strong><small>Imagery → preprocessing → vegetation indices → field verification → conservation decision.</small></div>''',unsafe_allow_html=True)
    with tab_b:
        la,ra=st.columns([1,1.4])
        with la:
            st.markdown('''<div class="radar"><div class="radar-dot" style="left:25%;top:34%"></div><div class="radar-dot" style="left:71%;top:23%"></div><div class="radar-dot" style="left:63%;top:68%"></div><div class="radar-dot" style="left:35%;top:75%"></div><div class="radar-center"></div></div>''',unsafe_allow_html=True)
        with ra:
            section('Sensor fusion','Environmental telemetry distribution')
            metric=st.selectbox('Compare sensor parameter',['Temperature (°C)','Salinity (ppt)','pH','Moisture (%)'],key='fusion_metric')
            fig=px.violin(sensors,x='Zone',y=metric,color='Zone',box=True,points='all',color_discrete_sequence=[EMERALD,CYAN,GOLD])
            st.plotly_chart(chart(fig,320),use_container_width=True)
    with tab_c:
        events=pd.DataFrame({'Sequence':['EVT-101','EVT-102','EVT-103','EVT-104','EVT-105'], 'Subsystem':['UAV','Smart Ajir','Capsule','Geospatial','CPS'], 'Event':['Mission plan generated','Telemetry review','Capsule registry updated','Map layers configured','Scenario recalculated'], 'Workflow':['Planning','Monitoring','Traceability','Analysis','Decision support']})
        st.dataframe(events,use_container_width=True,hide_index=True)
        st.caption('Illustrative workflow event catalog; no real-time device connection is configured.')
    section('02 / Spatial command','Geospatial operations overview')
    real_map(height=390)
    section('03 / System activity','Network registry')
    st.dataframe(sensors.head(12),hide_index=True,use_container_width=True)

elif page=='UAV Intelligence':
    section('01 / Mission lab','UAV flight operations simulator')
    c1,c2,c3=st.columns(3)
    mission=c1.selectbox('Mission objective',['Multispectral mapping','Capsule deployment','Coastal inspection','Vegetation health survey'])
    altitude=c2.slider('Flight altitude (m)',20,150,65)
    area=c3.slider('Target coverage (ha)',1,120,30)
    a,b,c=st.columns(3);a.metric('FLIGHT ALTITUDE',f'{altitude} m');b.metric('COVERAGE',f'{area} ha');c.metric('PLANNING SEGMENTS',f'{max(1,int(np.ceil(area/6)))}')
    section('02 / Aerial telemetry','Mission profile visualizer')
    t=np.linspace(0,1,90);alt=altitude*(1-np.exp(-t*15))*(1-.25*np.maximum(0,(t-.8)/.2))
    fig=go.Figure(go.Scatter(x=t*100,y=alt,mode='lines',line=dict(color=EMERALD,width=4),fill='tozeroy',fillcolor='rgba(8,168,138,.12)'))
    fig.update_layout(xaxis_title='Mission progress (%)',yaxis_title='Altitude (m)');st.plotly_chart(chart(fig),use_container_width=True)
    l,r=st.columns([1.4,1]);
    with l: real_map(['Planning zones'],height=390)
    with r:
        panel('HYBRID VTOL UAV','Vertical take-off capability, fixed-wing cruise, visual/thermal/multispectral payload and restoration capsule carriage.')
        panel('Mission logic',f'{mission} · {area} hectares · target altitude {altitude} metres. Route is conceptual; no autonomous flight commands are issued.')
        if st.button('Generate mission summary'):st.success(f'Planning profile prepared: {max(1,int(np.ceil(area/6)))} conceptual segments.')

elif page=='Capsule Tracking':
    section('01 / Capsule intelligence','Traceability registry')
    a,b,c=st.columns(3);a.metric('REGISTERED',len(capsules));b.metric('SPECIES',capsules.Species.nunique());c.metric('ESTABLISHED',int((capsules.Stage=='Established').sum()))
    x,y,z=st.columns([2,1,1]);q=x.text_input('Find capsule','',placeholder='CAP-00001');stage=y.selectbox('Stage',['All']+sorted(capsules.Stage.unique()));species=z.selectbox('Species',['All']+sorted(capsules.Species.unique()))
    df=capsules[capsules['Capsule ID'].str.contains(q,case=False,regex=False)]
    if stage!='All':df=df[df.Stage==stage]
    if species!='All':df=df[df.Species==species]
    if zone!='All zones':df=df[df.Zone==zone]
    st.dataframe(df,use_container_width=True,hide_index=True,height=350)
    st.download_button('Export filtered registry',df.to_csv(index=False),'captrace_capsules.csv','text/csv')
    l,r=st.columns(2)
    with l:
        fig=px.histogram(df,x='Stage',color='Stage',color_discrete_sequence=[EMERALD,CYAN,GOLD,'#4d7183']);st.plotly_chart(chart(fig),use_container_width=True)
    with r:
        fig=px.histogram(df,x='Species',color_discrete_sequence=[EMERALD]);fig.update_xaxes(tickangle=-25);st.plotly_chart(chart(fig),use_container_width=True)
    section('02 / Capsule architecture','Biodegradable restoration capsule')
    for title,body in [('01 · Native propagule','Site-matched mangrove seed or propagule.'),('02 · Bioaugmentation','Conceptual biological support layer.'),('03 · Organic nutrients','Biodegradable nutrient carrier.'),('04 · Moisture retention','Hydrogel-based water management concept.'),('05 · Substrate recovery','Outer biodegradable protection and site interaction.')]:panel(title,body)

elif page=='Smart Ajir Network':
    section('01 / IoT operations','Environmental digital twin')
    sensor=st.selectbox('Select sensor node',sensors.Node)
    row=sensors[sensors.Node==sensor].iloc[0]
    a,b,c,d=st.columns(4);a.metric('TEMPERATURE',f'{row["Temperature (°C)"]} °C');b.metric('SALINITY',f'{row["Salinity (ppt)"]} ppt');c.metric('SOIL PH',f'{row.pH}');d.metric('MOISTURE',f'{row["Moisture (%)"]}%')
    section('02 / Telemetry','Parameter waveform')
    parameter=st.selectbox('Environmental parameter',['Temperature (°C)','Salinity (ppt)','pH','Moisture (%)'])
    baseline=float(row[parameter]);n=80;wave=np.random.default_rng(int(sensor[-3:])).normal(0,.45,n).cumsum()*.15+baseline
    fig=go.Figure(go.Scatter(x=pd.date_range('2026-11-18',periods=n,freq='15min'),y=wave,mode='lines',line=dict(color=CYAN,width=3),fill='tozeroy',fillcolor='rgba(9,200,221,.07)'))
    st.plotly_chart(chart(fig,380),use_container_width=True)
    section('03 / Network inventory','Sensor comparison')
    st.dataframe(sensors if zone=='All zones' else sensors[sensors.Zone==zone],use_container_width=True,hide_index=True)

elif page=='Geospatial Explorer':
    section('01 / Earth observation','Interactive geographic explorer')
    a,b=st.columns([1,2]);basemap=a.selectbox('Base map',['Satellite','OpenStreetMap','Terrain']);layers=b.multiselect('Map overlays',['Sensor nodes','Capsule sites','Planning zones'],default=['Sensor nodes','Capsule sites','Planning zones'])
    real_map(layers,basemap,height=610)
    st.caption('Map tools: satellite / street / terrain basemap, fullscreen, minimap, cursor coordinates and distance measurement.')
    panel('Geographic layer information','Basemap tiles show real-world geography. Device markers and zone circles are conceptual reference placements, not surveyed coordinates or official site boundaries.')
    section('02 / Spatial indicators','Site-zone distribution')
    zcount=capsules.groupby('Zone').size().reset_index(name='Capsules');fig=px.bar(zcount,x='Zone',y='Capsules',color='Zone',color_discrete_sequence=[EMERALD,CYAN,GOLD]);st.plotly_chart(chart(fig),use_container_width=True)

elif page=='Restoration Analysis':
    section('01 / Suitability engine','Mangrove site scenario analysis')
    l,r=st.columns(2)
    with l: sal=l.slider('Salinity (ppt)',0,45,20);ph=l.slider('Substrate pH',3.0,10.0,7.0)
    with r:temp=r.slider('Temperature (°C)',20,40,29);inund=r.select_slider('Inundation intensity',['Low','Moderate','High'])
    score=int(30*(10<=sal<=30)+25*(6<=ph<=8.5)+25*(25<=temp<=33)+({'Low':5,'Moderate':20,'High':10}[inund]))
    a,b=st.columns([1,2]);a.metric('SCENARIO SCORE',f'{score}/100');a.progress(score/100)
    fig=go.Figure(go.Indicator(mode='gauge+number',value=score,gauge=dict(axis=dict(range=[0,100]),bar=dict(color=EMERALD),steps=[dict(range=[0,50],color='#fbe8e1'),dict(range=[50,75],color='#fff2cd'),dict(range=[75,100],color='#d9faee')])))
    b.plotly_chart(chart(fig,300),use_container_width=True)
    section('02 / Species planning','Mangrove species exploration')
    sp=st.selectbox('Species',sorted(capsules.Species.unique()))
    notes={'Avicennia marina':'Pioneer candidate for exposed, saline coastal settings where local site conditions permit.','Avicennia alba':'Often associated with seaward mangrove environments; verify substrate and tidal exposure.','Rhizophora mucronata':'Consider protected muddy intertidal settings with appropriate inundation.','Rhizophora apiculata':'Consider suitable sheltered muddy intertidal habitat.','Sonneratia alba':'Candidate for some tidal and seaward environments with suitable hydrology.'}
    panel(sp,notes[sp]+' Final selection requires local hydrology, sediment, salinity and field verification.')

elif page=='Conservation Analytics':
    section('01 / Analytics workbench','Environmental performance intelligence')
    metric=st.multiselect('Compare metrics',['Health index','Restoration coverage','Establishment'],default=['Health index','Establishment'])
    window=st.slider('Observation window (days)',14,110,60)
    df=trend.tail(window)
    fig=go.Figure()
    for i,name in enumerate(metric):fig.add_trace(go.Scatter(x=df.Date,y=df[name],name=name,mode='lines',line=dict(width=3,color=[EMERALD,CYAN,GOLD][['Health index','Restoration coverage','Establishment'].index(name)])))
    st.plotly_chart(chart(fig,430),use_container_width=True)
    a,b=st.columns(2)
    with a:
        fig=px.box(sensors,x='Zone',y='Salinity (ppt)',color='Zone',color_discrete_sequence=[EMERALD,CYAN,GOLD]);st.plotly_chart(chart(fig),use_container_width=True)
    with b:
        fig=px.scatter(sensors,x='Salinity (ppt)',y='Moisture (%)',color='Zone',size='Battery (%)',hover_name='Node',color_discrete_sequence=[EMERALD,CYAN,GOLD]);st.plotly_chart(chart(fig),use_container_width=True)
    st.download_button('Export indicator series',df.to_csv(index=False),'captrace_timeseries.csv','text/csv')

elif page=='CPS Integration':
    section('01 / 5C architecture','Cyber-Physical Integration Pipeline')
    st.markdown('<div class="flow">'+''.join(f'<div class="node">{x}</div>'+('<div class="arrow">→</div>' if i<4 else '') for i,x in enumerate(['CONNECTION','CONVERSION','CYBER','COGNITION','CONFIGURATION']))+'</div>',unsafe_allow_html=True)
    stages={'Connection':'Smart Ajir environmental sensing, UAV payloads and capsule identity.','Conversion':'Transform measurements into structured ecological indicators.','Cyber':'Consolidated traceability, device registry and geospatial data.','Cognition':'Assess restoration patterns, suitability and conservation priorities.','Configuration':'Adapt restoration strategy and field monitoring decisions.'}
    stage=st.selectbox('Explore system layer',list(stages));panel(stage,stages[stage])
    section('02 / Technology matrix','Integrated CAPTRACE components')
    components=pd.DataFrame({'System':['UAV VTOL','Restoration capsule','Smart Ajir','Digital platform','Community interface'],'Role':['Aerial survey and distribution','Biodegradable propagule carrier','Environmental telemetry','Traceability and analysis','Education and enterprise'],'CPS':['Connection','Physical deployment','Connection','Cyber / Cognition','Configuration']})
    st.dataframe(components,hide_index=True,use_container_width=True)

elif page=='Jaga Mangrove':
    section('01 / Community business tourism','Jaga Mangrove Experience Studio')
    t1,t2,t3=st.tabs(['Experience builder','Community enterprise','Education & culture'])
    with t1:
        a,b=st.columns(2);activity=a.multiselect('Select experiences',['Mangrove discovery trail','Coastal ecology lab','Drone monitoring interpretation','Community culinary experience','Restoration learning session'],default=['Mangrove discovery trail','Coastal ecology lab']);guests=b.slider('Group size',1,30,10);rate=b.number_input('Illustrative package price / guest (IDR)',min_value=0,value=125000,step=25000)
        st.metric('ESTIMATED PACKAGE REVENUE',f'Rp {guests*rate:,.0f}'.replace(',','.'))
        for act in activity:panel(act,'Community-facilitated educational experience aligned with low-impact ecotourism.')
    with t2:
        section('Business ecosystem','Community-led value chain')
        for title,body in [('Local guides','Interpretation, visitor safety and conservation storytelling.'),('Community microenterprises','Local products, culinary services and responsible visitor experiences.'),('Restoration stewardship','Participatory monitoring and ecological education.')]:panel(title,body)
    with t3:
        section('Interpretation studio','Technology · conservation · culture')
        panel('Coastal living heritage','Connect local livelihoods and coastal knowledge with mangrove ecology and digital monitoring.')
        panel('Visitor learning journey','Discover coastal threats, explore mangrove species, interpret UAV and Smart Ajir data, and join guided restoration education.')

st.divider()
with st.expander('Data sources & methodology'):
    st.write('Basemap: OpenStreetMap / CartoDB / Esri World Imagery. Sensor readings, capsule records, performance series, map overlays and financial estimates are illustrative interface datasets. Replace with verified field data before operational use.')
st.caption('CAPTRACE 8.0  /  CAPSULE-BASED TRACEABILITY SYSTEM  /  SAYUNG COASTAL INTELLIGENCE')
