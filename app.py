import base64
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
EMERALD='#08A88A'; CYAN='#09C8DD'; INK='#092C37'; GOLD='#E5B85C'

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800;900&family=Rajdhani:wght@500;600;700&display=swap');
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

PAGES=['Command Center','UAV Intelligence','Capsule Tracking','Smart Ajir Network','Geospatial Explorer','Restoration Analysis','Conservation Analytics','CPS Integration','Jaga Mangrove']
with st.sidebar:
    if LOGO.exists(): st.image(str(LOGO),use_container_width=True)
    else: st.markdown('## CAPTRACE')
    st.markdown('<span class="pulse"></span><span style="font-size:11px;letter-spacing:2px">CONSERVATION INTELLIGENCE</span>',unsafe_allow_html=True)
    page=st.radio('NAVIGATION',PAGES,label_visibility='collapsed',key='page')
    st.divider()
    zone=st.selectbox('OPERATIONAL FOCUS',['All zones','Z1 | Coastal','Z2 | Transition','Z3 | Inland'])
    st.caption('SAYUNG · DEMAK · CENTRAL JAVA')

st.markdown(f'''<div class="hero"><div class="scanline"></div><div class="orbitlabel">EARTH<br>OBSERVATION</div><div class="eyebrow"><span class="pulse"></span>CAPTRACE / DIGITAL ECOSYSTEM</div><div class="title">{page.upper()}</div><div class="sub">Capsule-Based Traceability System · Mangrove restoration, geospatial intelligence and community-driven maritime ecotourism</div><div class="tags"><span>COASTAL INTELLIGENCE</span><span>CYBER-PHYSICAL SYSTEM</span><span>SAYUNG, DEMAK</span></div></div>''',unsafe_allow_html=True)

st.markdown('''<div class="mission-strip">
<div class="mission-chip"><b>MISSION REGION</b><span>SAYUNG · CENTRAL JAVA</span></div>
<div class="mission-chip"><b>COORDINATE REFERENCE</b><span>6.943° S / 110.481° E</span></div>
<div class="mission-chip"><b>PLATFORM MODULES</b><span>UAV / CAPSULE / IOT / CPS</span></div>
<div class="mission-chip"><b>DATA WORKSPACE</b><span>EXPLORATION & ANALYTICS</span></div>
</div>''',unsafe_allow_html=True)

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
st.caption('CAPTRACE 7.0  /  CAPSULE-BASED TRACEABILITY SYSTEM  /  SAYUNG COASTAL INTELLIGENCE')
