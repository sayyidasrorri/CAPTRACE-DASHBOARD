import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='CAPTRACE | Conservation Intelligence', page_icon=None, layout='wide', initial_sidebar_state='expanded')
G='#147D64'; NAVY='#173B40'; BLUE='#347EAB'; GOLD='#D8A956'; BG='#F5F8F7'
np.random.seed(18)

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp{font-family:'DM Sans',sans-serif!important;color:#173B40!important}
.stApp,[data-testid="stAppViewContainer"], [data-testid="stHeader"]{background:#F5F8F7!important}
[data-testid="stSidebar"]{background:#FFFFFF!important;border-right:1px solid #E3EBE8!important}
[data-testid="stSidebar"] *{color:#234841!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:8px 10px;border-radius:10px;margin:3px 0}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:#E5F3EC!important}
h1,h2,h3{font-family:'Manrope',sans-serif!important;color:#153E37!important;letter-spacing:-.035em!important}
h1{font-size:2.35rem!important;font-weight:800!important}h2{font-size:1.48rem!important;font-weight:800!important}h3{font-size:1.15rem!important;font-weight:750!important}
p,label,span,div[data-testid="stMarkdownContainer"]{line-height:1.5}
[data-testid="stMetric"]{background:white;border:1px solid #E2EBE6;border-radius:18px;padding:18px 20px;box-shadow:0 8px 28px rgba(16,77,66,.045)}
[data-testid="stMetricLabel"]{font-size:.85rem!important;font-weight:700!important;color:#527069!important}
[data-testid="stMetricValue"]{font-family:'Manrope',sans-serif!important;color:#164B3F!important;font-weight:800!important}
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"]{background:white;border:1px solid #E5EDE9;border-radius:18px;padding:10px}
.stButton>button[kind="primary"],.stDownloadButton>button{background:#147D64!important;color:white!important;border:0!important;border-radius:11px!important;font-weight:700!important}
.stButton>button{border-radius:11px!important}
[data-baseweb="select"]>div, [data-testid="stTextInput"] input{border-radius:11px!important;background:#FFFFFF!important}
[data-testid="stTabs"] button{font-weight:700!important}
.block-container{padding-top:2rem!important;max-width:1450px!important}
.hero{background:linear-gradient(115deg,#0E594D,#147D64 65%,#279B83);border-radius:24px;padding:30px 36px;color:white;margin-bottom:24px;position:relative;overflow:hidden}
.hero:after{content:'';position:absolute;width:290px;height:290px;border:1px solid rgba(255,255,255,.2);border-radius:50%;right:-50px;top:-110px;box-shadow:0 0 0 45px rgba(255,255,255,.045),0 0 0 100px rgba(255,255,255,.035)}
.hero .eyebrow{color:#BDEADB;letter-spacing:.2em;font-size:11px;font-weight:800}.hero h1{color:white!important;margin:7px 0!important;font-size:2.4rem!important}.hero p{color:#D7F2E7;font-size:15px;margin:0;max-width:700px}
.section-kicker{color:#147D64;font-size:12px;font-weight:800;letter-spacing:.14em;margin-top:16px}
.softcard{background:#fff;border:1px solid #E3EBE7;border-radius:18px;padding:22px;margin:8px 0 18px}
.softcard b{color:#164C41}.softcard small{color:#648078}
.pill{display:inline-block;background:#E8F4EE;color:#16715D;border-radius:100px;padding:5px 11px;font-size:12px;font-weight:800}
.step{background:white;border:1px solid #E3EBE7;border-left:4px solid #147D64;border-radius:12px;padding:16px 20px;margin:10px 0}
[data-testid="stAlert"]{border-radius:12px!important}
</style>''', unsafe_allow_html=True)

ZONES=['Z1 - Coastal','Z2 - Transition','Z3 - Inland']
SPECIES=['Avicennia marina','Avicennia alba','Rhizophora mucronata','Rhizophora apiculata','Sonneratia alba']
rng=np.random.default_rng(24)
sensors=pd.DataFrame({'Sensor ID':[f'AJR-{i:03}' for i in range(1,25)],'Zone':rng.choice(ZONES,24),'Temperature (°C)':np.round(rng.uniform(27,33,24),1),'Salinity (ppt)':np.round(rng.uniform(11,32,24),1),'pH':np.round(rng.uniform(6.4,8.3,24),2),'Moisture (%)':np.round(rng.uniform(56,89,24),1)})
capsules=pd.DataFrame({'Capsule ID':[f'CAP-{i:04}' for i in range(1,251)],'Zone':rng.choice(ZONES,250),'Species':rng.choice(SPECIES,250),'Stage':rng.choice(['Registered','Distributed','Monitoring','Established'],250)})

with st.sidebar:
    st.markdown('<div style="font-family:Manrope;font-size:26px;font-weight:800;color:#125E4F;letter-spacing:-1px">CAPTRACE<span style="color:#D5A34D">.</span></div><div style="font-size:11px;letter-spacing:.13em;color:#769188;margin-bottom:25px">CONSERVATION INTELLIGENCE</div>',unsafe_allow_html=True)
    menu=st.radio('WORKSPACE',['Overview','UAV Intelligence','Capsule Tracking','Smart Ajir Network','Geospatial Explorer','Restoration Analysis','Conservation Analytics','CPS Integration','Jaga Mangrove'],label_visibility='collapsed')
    st.divider()
    st.markdown('<span class="pill">SAYUNG · DEMAK</span>',unsafe_allow_html=True)
    st.caption('CAPTRACE | Integrated coastal restoration')

st.markdown(f'<div class="hero"><div class="eyebrow">MANGROVE CONSERVATION INTELLIGENCE</div><h1>{menu}</h1><p>CAPTRACE integrates coastal mapping, restoration capsules, environmental sensing and community-based maritime experiences.</p></div>',unsafe_allow_html=True)

def plot_style(fig,height=350):
    fig.update_layout(template='plotly_white',height=height,paper_bgcolor='white',plot_bgcolor='white',font=dict(family='DM Sans',color='#365D55'),margin=dict(l=18,r=18,t=35,b=15),legend=dict(orientation='h',y=-.22),hoverlabel=dict(bgcolor='white',font_color='#173B40'))
    fig.update_xaxes(showgrid=False,linecolor='#E5EEE9')
    fig.update_yaxes(gridcolor='#EAF0EC',zeroline=False)
    return fig

def title(label,heading):
    st.markdown(f'<div class="section-kicker">{label.upper()}</div>',unsafe_allow_html=True)
    st.subheader(heading)

if menu=='Overview':
    a,b,c,d=st.columns(4)
    a.metric('Mangrove Health Index','68%','+4.2 pp')
    b.metric('Smart Ajir Network','24','Devices')
    c.metric('Capsule Registry','1,250','+150')
    d.metric('Restoration Zones','03','Mapped')
    title('Environmental intelligence','Restoration at a glance')
    left,right=st.columns([1.65,1])
    with left:
        x=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=x,y=[39,43,46,51,55,59,64,68],name='Vegetation index',mode='lines+markers',line=dict(color=G,width=4,shape='spline'),fill='tozeroy',fillcolor='rgba(20,125,100,.10)'))
        fig.add_trace(go.Scatter(x=x,y=[29,32,37,41,45,49,54,60],name='Restoration progress',mode='lines+markers',line=dict(color=BLUE,width=3,shape='spline')))
        st.plotly_chart(plot_style(fig),use_container_width=True)
    with right:
        fig=go.Figure(go.Pie(labels=['Healthy','Moderate','Degraded','Open'],values=[68,17,10,5],hole=.72,marker=dict(colors=[G,'#A8D6B4',GOLD,'#DCE6E3']),textinfo='percent',hoverinfo='label+value'))
        fig.update_layout(annotations=[dict(text='<b>68%</b><br>Healthy',showarrow=False,font=dict(size=21,color=NAVY))],showlegend=True)
        st.plotly_chart(plot_style(fig),use_container_width=True)
    title('Operational modules','Explore the system')
    cols=st.columns(3)
    cards=[('01 / UAV','Vegetation mapping','Multispectral survey and capsule mission planning'),('02 / CAPSULE','Traceability registry','Species, restoration zone and deployment status'),('03 / SMART AJIR','Environmental network','Salinity, pH, temperature and moisture'),('04 / GIS','Geospatial explorer','Interactive location layers and restoration areas'),('05 / ANALYTICS','Restoration insights','Performance patterns and scenario exploration'),('06 / COMMUNITY','Jaga Mangrove','Local enterprise and maritime ecotourism')]
    for i,(n,h,t) in enumerate(cards):
        with cols[i%3]: st.markdown(f'<div class="softcard"><small>{n}</small><h3 style="margin:10px 0 5px">{h}</h3><div style="color:#607A72;font-size:14px">{t}</div></div>',unsafe_allow_html=True)

elif menu=='UAV Intelligence':
    title('Mission configuration','UAV planning console')
    a,b,c=st.columns(3)
    mission=a.selectbox('Mission objective',['Vegetation Mapping','Capsule Distribution','Environmental Survey'])
    altitude=b.slider('Flight altitude (m)',20,150,65)
    area=c.slider('Coverage (ha)',1,100,24)
    k1,k2,k3=st.columns(3)
    k1.metric('Altitude',f'{altitude} m');k2.metric('Coverage',f'{area} ha');k3.metric('Flight segments',str(max(1,int(np.ceil(area/6)))))
    title('Mission sequence','Survey and deployment workflow')
    for name,desc in [('01 — Reconnaissance','Identify coastal conditions and vegetation structure.'),('02 — Mapping','Collect visual and multispectral observations.'),('03 — Deployment','Plan capsule distribution by site suitability.'),('04 — Monitoring','Connect field observations to Smart Ajir records.')]:
        st.markdown(f'<div class="step"><b>{name}</b><br><span style="color:#678078">{desc}</span></div>',unsafe_allow_html=True)
    if st.button('Generate mission summary',type='primary'):
        st.success(f'{mission}: {area} ha coverage, {altitude} m altitude, {max(1,int(np.ceil(area/6)))} planned segments.')

elif menu=='Capsule Tracking':
    title('Restoration capsule network','Traceability registry')
    a,b,c=st.columns(3);a.metric('Capsules registered','1,250');b.metric('Species groups','05');c.metric('Planning zones','03')
    search=st.text_input('Search capsule ID',placeholder='CAP-0001')
    z=st.selectbox('Zone filter',['All zones']+ZONES)
    df=capsules[capsules['Capsule ID'].str.contains(search,case=False,regex=False)]
    if z!='All zones':df=df[df.Zone==z]
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button('Export capsule records',df.to_csv(index=False),'captrace_capsules.csv','text/csv')

elif menu=='Smart Ajir Network':
    title('Environmental telemetry','Smart Ajir monitoring')
    selected=st.selectbox('Select device',sensors['Sensor ID'])
    r=sensors.loc[sensors['Sensor ID']==selected].iloc[0]
    a,b,c,d=st.columns(4)
    a.metric('Temperature',f'{r["Temperature (°C)"]} °C');b.metric('Salinity',f'{r["Salinity (ppt)"]} ppt');c.metric('Soil pH',f'{r["pH"]}');d.metric('Moisture',f'{r["Moisture (%)"]}%')
    title('Parameter history','Environmental patterns')
    days=pd.date_range('2026-11-01',periods=21)
    v=rng.normal(r['Temperature (°C)'],.8,21)
    fig=go.Figure(go.Scatter(x=days,y=v,mode='lines+markers',line=dict(color=G,width=3),fill='tozeroy',fillcolor='rgba(20,125,100,.08)',name='Temperature'))
    st.plotly_chart(plot_style(fig),use_container_width=True)
    st.dataframe(sensors,use_container_width=True,hide_index=True)

elif menu=='Geospatial Explorer':
    title('Coastal landscape','Geospatial monitoring')
    layers=st.multiselect('Visible layers',['Smart Ajir','Capsule Sites','Restoration Area'],default=['Smart Ajir','Capsule Sites','Restoration Area'])
    base=st.selectbox('Map style',['Light map','Terrain map'])
    tiles='CartoDB positron' if base=='Light map' else 'OpenStreetMap'
    m=folium.Map(location=[-6.94,110.48],zoom_start=12,tiles=tiles,control_scale=True)
    if 'Smart Ajir' in layers:
        for i in range(12):
            folium.CircleMarker([-6.94+float(rng.uniform(-.013,.013)),110.48+float(rng.uniform(-.013,.013))],radius=6,color=G,fill=True,fill_color=G,fill_opacity=.9,tooltip=f'Smart Ajir {i+1}').add_to(m)
    if 'Capsule Sites' in layers:
        for i in range(15):
            folium.CircleMarker([-6.94+float(rng.uniform(-.018,.018)),110.48+float(rng.uniform(-.018,.018))],radius=4,color=BLUE,fill=True,fill_color=BLUE,tooltip=f'Capsule site {i+1}').add_to(m)
    if 'Restoration Area' in layers:
        folium.Circle([ -6.94,110.48],radius=1000,color=GOLD,fill=True,fill_color=GOLD,fill_opacity=.10,tooltip='Illustrative restoration area').add_to(m)
    st_folium(m,height=530,use_container_width=True,returned_objects=[])
    st.caption('Illustrative point locations. Replace with validated survey coordinates before operational use.')

elif menu=='Restoration Analysis':
    title('Decision support','Site suitability explorer')
    a,b=st.columns(2)
    with a:
        sal=a.slider('Salinity (ppt)',0,45,20);ph=a.slider('Soil pH',3.0,10.0,7.1)
    with b:
        temp=b.slider('Temperature (°C)',20,40,29);flood=b.selectbox('Inundation regime',['Low','Moderate','High'])
    score=(30 if 10<=sal<=30 else 0)+(25 if 6<=ph<=8.5 else 0)+(25 if 25<=temp<=33 else 0)+({'Low':0,'Moderate':20,'High':10}[flood])
    a,b=st.columns([1,2]);a.metric('Suitability index',f'{score}/100')
    with b:
        st.progress(score/100)
        st.markdown(f'<div class="softcard"><b>{"Higher" if score>=75 else "Moderate" if score>=50 else "Lower"} scenario suitability</b><br><small>Screening only. Species selection requires hydrological and substrate field assessment.</small></div>',unsafe_allow_html=True)
    fig=go.Figure(go.Bar(x=['Salinity','pH','Temperature','Inundation'],y=[30 if 10<=sal<=30 else 0,25 if 6<=ph<=8.5 else 0,25 if 25<=temp<=33 else 0,{'Low':0,'Moderate':20,'High':10}[flood]],marker_color=[G,BLUE,'#6CB8A3',GOLD]))
    st.plotly_chart(plot_style(fig,300),use_container_width=True)

elif menu=='Conservation Analytics':
    title('Performance intelligence','Conservation analytics')
    df=pd.DataFrame({'Month':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug'],'Vegetation health':[39,43,46,51,55,59,64,68],'Capsule establishment':[17,23,29,37,44,51,56,61],'Restoration coverage':[12,19,25,34,45,54,62,72]})
    metric=st.selectbox('Performance indicator',df.columns[1:].tolist())
    chart=st.radio('Visualization',['Area','Bar'],horizontal=True)
    fig=px.area(df,x='Month',y=metric,color_discrete_sequence=[G]) if chart=='Area' else px.bar(df,x='Month',y=metric,color_discrete_sequence=[G])
    st.plotly_chart(plot_style(fig,420),use_container_width=True)
    st.download_button('Download analytics',df.to_csv(index=False),'captrace_analytics.csv','text/csv')

elif menu=='CPS Integration':
    title('System architecture','5C cyber-physical integration')
    stages=[('01','Connection','UAV, Smart Ajir and field observations'),('02','Conversion','Transform observations into structured information'),('03','Cyber','Centralize traceability and geospatial records'),('04','Cognition','Interpret conditions and restoration priorities'),('05','Configuration','Support adaptive restoration decisions')]
    for n,name,desc in stages:
        st.markdown(f'<div class="step"><span class="pill">{n}</span> &nbsp; <b>{name}</b><br><span style="color:#668078;margin-left:49px">{desc}</span></div>',unsafe_allow_html=True)
    st.selectbox('Inspect integration component',['UAV mapping','Restoration capsules','Smart Ajir sensors','Digital monitoring','Restoration decisions'])

elif menu=='Jaga Mangrove':
    title('Community business tourism','Jaga Mangrove experience')
    a,b,c=st.columns(3)
    for col,name,desc in [(a,'Explore','Guided mangrove discovery and coastal interpretation.'),(b,'Learn','Digital education on restoration and maritime ecology.'),(c,'Contribute','Community-managed conservation and local enterprises.')]:
        with col:st.markdown(f'<div class="softcard"><h3>{name}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    tabs=st.tabs(['Eco-tourism','Local enterprise','Conservation learning'])
    with tabs[0]:st.write('Curated mangrove interpretation trails, coastal observation and guided ecological experiences.')
    with tabs[1]:st.write('Local guides, community-managed visitor services and conservation-oriented entrepreneurship.')
    with tabs[2]:st.write('Educational experiences connecting UAV mapping, restoration capsules, Smart Ajir and mangrove ecology.')

st.markdown('<div style="margin-top:32px;padding:20px 0;border-top:1px solid #DFE9E4;color:#6A827B;font-size:12px;display:flex;justify-content:space-between"><span>CAPTRACE / CONSERVATION INTELLIGENCE</span><span>Sayung, Demak · Indonesia</span></div>',unsafe_allow_html=True)
with st.expander('Data sources & methodology'):
    st.write('Illustrative dashboard records are used for interface demonstration. Operational monitoring requires verified field measurements and connected devices.')
