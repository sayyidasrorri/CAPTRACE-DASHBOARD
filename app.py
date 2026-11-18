import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title='CAPTRACE | Conservation Intelligence', page_icon=None, layout='wide', initial_sidebar_state='expanded')
GREEN='#087F65'; NAVY='#153B42'; BLUE='#247DA4'; GOLD='#D6A54A'; BG='#F5F8F7'
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp {font-family:'DM Sans',sans-serif!important}
.stApp,[data-testid="stAppViewContainer"],.main {background:#F5F8F7!important;color:#153B42!important}
[data-testid="stHeader"]{background:#F5F8F7!important}
[data-testid="stSidebar"]{background:#E5F1EC!important;border-right:1px solid #CFDED7!important}
[data-testid="stSidebar"] *{color:#153B42!important}
[data-testid="stSidebar"] [role="radiogroup"] label{border-radius:10px;padding:7px 9px}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:#D5E9DF}
h1,h2,h3,h4,p,span,label{color:#153B42}
h1{font-size:2.6rem!important;font-weight:800!important;letter-spacing:-1.4px!important}
h2,h3{font-weight:800!important;letter-spacing:-.4px!important}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#294E54!important}
[data-testid="stMetric"]{background:#FFFFFF!important;border:1px solid #DCE8E3!important;border-radius:18px!important;padding:19px!important;box-shadow:0 8px 25px rgba(16,76,66,.06)}
[data-testid="stMetricLabel"] *{color:#52716F!important;font-weight:700!important}
[data-testid="stMetricValue"] *{color:#104D42!important;font-weight:800!important}
[data-testid="stMetricDelta"] *{color:#087F65!important}
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"]{border:1px solid #E0E9E5;border-radius:16px;overflow:hidden;background:white}
.stButton>button,.stDownloadButton>button{background:#087F65!important;color:#FFF!important;border:0!important;border-radius:10px!important;font-weight:700!important}
.stButton>button *,.stDownloadButton>button *{color:#FFF!important}
.stButton>button:hover,.stDownloadButton>button:hover{background:#075F4D!important}
[data-baseweb="select"]>div,[data-baseweb="input"]>div,input{background:#FFF!important;color:#153B42!important;border-color:#D1E1D9!important}
[data-baseweb="select"] *{color:#153B42!important}
[data-testid="stWidgetLabel"] *{color:#244D4B!important;font-weight:700!important}
[data-testid="stTabs"] button{color:#294E54!important;font-weight:700!important}
[data-testid="stAlert"]{border-radius:12px}
.hero{background:linear-gradient(120deg,#FFFFFF 0%,#E7F5EE 100%);padding:28px 32px;border:1px solid #D8E9E0;border-radius:22px;margin-bottom:24px;box-shadow:0 12px 35px rgba(18,79,63,.045)}
.eyebrow{color:#087F65!important;font-size:12px!important;font-weight:800!important;letter-spacing:2px!important}
.hero-title{color:#103E37!important;font-size:44px!important;font-weight:800!important;letter-spacing:-1.7px!important;margin:7px 0!important}
.hero-sub{color:#426862!important;font-size:16px!important;margin:0!important}
.mini-card{padding:18px;background:#FFF;border:1px solid #DDE9E3;border-radius:15px;min-height:110px}
.mini-card b{color:#104D42;font-size:16px}.mini-card p{font-size:13px;margin-top:8px}
hr{border-color:#D9E5DE!important}
</style>''',unsafe_allow_html=True)

@st.cache_data
def load_data():
    rng=np.random.default_rng(42)
    zones=['Z1 - Coastal','Z2 - Transition','Z3 - Inland']
    sensors=pd.DataFrame({'Sensor ID':[f'AJR-{i:03d}' for i in range(1,25)],'Zone':rng.choice(zones,24),'Temperature (°C)':rng.uniform(27,33,24).round(1),'Salinity (ppt)':rng.uniform(10,32,24).round(1),'pH':rng.uniform(6.5,8.2,24).round(2),'Moisture (%)':rng.uniform(55,90,24).round(1)})
    capsules=pd.DataFrame({'Capsule ID':[f'CAP-{i:04d}' for i in range(1,126)],'Zone':rng.choice(zones,125),'Species':rng.choice(['Rhizophora mucronata','Rhizophora apiculata','Avicennia marina','Avicennia alba','Sonneratia alba'],125),'Status':rng.choice(['Distributed','Monitoring','Established'],125)})
    return sensors,capsules
sensors,capsules=load_data()
zones=['Z1 - Coastal','Z2 - Transition','Z3 - Inland']

def chart_style(fig,height=350):
    fig.update_layout(template='plotly_white',height=height,paper_bgcolor='#FFFFFF',plot_bgcolor='#FFFFFF',font=dict(family='DM Sans',color='#244D4B',size=13),margin=dict(l=20,r=20,t=24,b=20),legend=dict(orientation='h',y=-.18))
    return fig

with st.sidebar:
    st.markdown('## CAPTRACE')
    st.caption('CONSERVATION INTELLIGENCE')
    st.divider()
    menu=st.radio('WORKSPACE',['Command Center','UAV Intelligence','Capsule Tracking','Smart Ajir Network','Geospatial Explorer','Restoration Analysis','Conservation Analytics','CPS Integration','Jaga Mangrove'],label_visibility='collapsed')
    st.divider()
    st.caption('SAYUNG · DEMAK · INDONESIA')

st.markdown('<div class="hero"><div class="eyebrow">MANGROVE CONSERVATION INTELLIGENCE</div><div class="hero-title">CAPTRACE</div><p class="hero-sub">Integrated restoration monitoring, environmental intelligence and traceability</p></div>',unsafe_allow_html=True)

if menu=='Command Center':
    st.subheader('Conservation Overview')
    a,b,c,d=st.columns(4)
    a.metric('Mangrove Health Index','68%','+4.2%')
    b.metric('Smart Ajir Network','24','Registered')
    c.metric('Capsule Distribution','1,250','+150')
    d.metric('Restoration Zones','3','Mapped')
    st.write('')
    l,r=st.columns([1.45,1])
    with l:
        st.subheader('Restoration Performance')
        fig=go.Figure(go.Scatter(x=['Jan','Feb','Mar','Apr','May','Jun'],y=[42,47,51,56,62,68],mode='lines+markers',line=dict(color=GREEN,width=4),marker=dict(size=9),fill='tozeroy',fillcolor='rgba(8,127,101,.08)',name='Health index'))
        st.plotly_chart(chart_style(fig),use_container_width=True)
    with r:
        st.subheader('Vegetation Classification')
        fig=px.pie(names=['Healthy','Moderate','Degraded','Open Area'],values=[68,17,10,5],hole=.64,color_discrete_sequence=[GREEN,GOLD,BLUE,'#C8DAD3'])
        st.plotly_chart(chart_style(fig),use_container_width=True)
    st.subheader('Sensor Network Overview')
    st.dataframe(sensors.head(8),use_container_width=True,hide_index=True)

elif menu=='UAV Intelligence':
    st.subheader('UAV Mission Control')
    a,b,c=st.columns(3)
    mission=a.selectbox('Mission type',['Vegetation Mapping','Capsule Distribution','Environmental Monitoring'])
    altitude=b.slider('Flight altitude (m)',20,150,60)
    coverage=c.slider('Coverage area (ha)',1,100,25)
    x,y,z=st.columns(3)
    x.metric('Flight Altitude',f'{altitude} m')
    y.metric('Coverage Area',f'{coverage} ha')
    z.metric('Flight Segments',str(max(1,int(np.ceil(coverage/5)))))
    st.markdown('### Mission Configuration')
    st.write(f'**Selected mission:** {mission}')
    if st.button('Generate Mission Plan'):
        st.success(f'Mission plan prepared: {mission} · {altitude} m · {coverage} ha')

elif menu=='Capsule Tracking':
    st.subheader('Capsule Traceability')
    a,b,c=st.columns(3)
    a.metric('Registered Capsules','1,250')
    b.metric('Tracking Records',len(capsules))
    c.metric('Restoration Zones','3')
    search=st.text_input('Search Capsule ID',placeholder='CAP-0001')
    zone=st.selectbox('Filter zone',['All Zones']+zones)
    filtered=capsules[capsules['Capsule ID'].str.contains(search,case=False,regex=False)]
    if zone!='All Zones':filtered=filtered[filtered['Zone']==zone]
    st.dataframe(filtered,use_container_width=True,hide_index=True)
    st.download_button('Export Capsule Records',filtered.to_csv(index=False),'capsule_records.csv','text/csv')

elif menu=='Smart Ajir Network':
    st.subheader('Environmental Sensor Network')
    sensor=st.selectbox('Select Smart Ajir',sensors['Sensor ID'])
    row=sensors.loc[sensors['Sensor ID']==sensor].iloc[0]
    a,b,c,d=st.columns(4)
    a.metric('Temperature',f'{row["Temperature (°C)"]} °C')
    b.metric('Salinity',f'{row["Salinity (ppt)"]} ppt')
    c.metric('Soil pH',f'{row["pH"]}')
    d.metric('Moisture',f'{row["Moisture (%)"]}%')
    st.subheader('Environmental Parameter Trends')
    days=pd.date_range('2026-11-01',periods=15)
    phase=np.linspace(0,2*np.pi,15)
    trend=pd.DataFrame({'Date':days,'Temperature':row['Temperature (°C)']+np.sin(phase)*.9,'Salinity':row['Salinity (ppt)']+np.cos(phase)*1.8})
    fig=px.line(trend,x='Date',y=['Temperature','Salinity'],color_discrete_sequence=[GREEN,BLUE])
    st.plotly_chart(chart_style(fig,390),use_container_width=True)
    st.subheader('Sensor Registry')
    st.dataframe(sensors,use_container_width=True,hide_index=True)

elif menu=='Geospatial Explorer':
    st.subheader('Mangrove Geospatial Explorer')
    layers=st.multiselect('Visible map layers',['Smart Ajir','Capsule Distribution','Restoration Zones'],default=['Smart Ajir','Capsule Distribution','Restoration Zones'])
    m=folium.Map(location=[-6.94,110.48],zoom_start=12,tiles='CartoDB positron')
    rng=np.random.default_rng(20)
    if 'Smart Ajir' in layers:
        for i in range(12):folium.CircleMarker([-6.94+rng.uniform(-.015,.015),110.48+rng.uniform(-.015,.015)],radius=6,color=GREEN,fill=True,fill_opacity=.85,popup=f'Smart Ajir AJR-{i+1:03d}').add_to(m)
    if 'Capsule Distribution' in layers:
        for i in range(15):folium.CircleMarker([-6.94+rng.uniform(-.02,.02),110.48+rng.uniform(-.02,.02)],radius=4,color=BLUE,fill=True,fill_opacity=.85,popup=f'Capsule site {i+1}').add_to(m)
    if 'Restoration Zones' in layers:folium.Circle([-6.94,110.48],radius=1100,color=GOLD,fill=True,fill_opacity=.12,popup='Restoration planning area').add_to(m)
    st_folium(m,width=None,height=570,returned_objects=[])

elif menu=='Restoration Analysis':
    st.subheader('Site Suitability Assessment')
    a,b=st.columns(2)
    with a:
        salinity=st.slider('Salinity (ppt)',0,45,20)
        ph=st.slider('Soil pH',3.,10.,7.)
    with b:
        temp=st.slider('Temperature (°C)',20,40,29)
        inundation=st.selectbox('Inundation',['Low','Moderate','High'])
    score=(30 if 10<=salinity<=30 else 0)+(25 if 6<=ph<=8.5 else 0)+(25 if 25<=temp<=33 else 0)+(20 if inundation=='Moderate' else 10 if inundation=='High' else 0)
    st.metric('Site Suitability Score',f'{score}/100')
    st.progress(score/100)
    st.markdown('### Assessment Result')
    st.write('High suitability' if score>=75 else 'Moderate suitability' if score>=50 else 'Further site assessment recommended')

elif menu=='Conservation Analytics':
    st.subheader('Conservation Performance Analytics')
    data=pd.DataFrame({'Month':['Jan','Feb','Mar','Apr','May','Jun'],'Vegetation Health':[42,47,51,56,62,68],'Capsule Establishment':[20,29,38,46,53,61],'Restoration Coverage':[15,22,34,45,58,72]})
    metric=st.selectbox('Indicator',list(data.columns[1:]))
    fig=px.bar(data,x='Month',y=metric,color_discrete_sequence=[GREEN])
    st.plotly_chart(chart_style(fig,450),use_container_width=True)
    st.download_button('Download Analytics',data.to_csv(index=False),'conservation_analytics.csv','text/csv')

elif menu=='CPS Integration':
    st.subheader('Cyber-Physical System Architecture')
    stages={'Connection':'UAV, capsule and Smart Ajir connectivity.','Conversion':'Environmental data processing and transformation.','Cyber':'Centralized monitoring and traceability.','Cognition':'Restoration analysis and decision support.','Configuration':'Adaptive restoration planning and management.'}
    selected=st.selectbox('Explore CPS layer',list(stages))
    st.markdown(f'<div class="mini-card"><b>{selected}</b><p>{stages[selected]}</p></div>',unsafe_allow_html=True)
    st.write('')
    st.subheader('Technology Integration')
    cols=st.columns(5)
    for col,title in zip(cols,['UAV','Capsule','Smart Ajir','Digital Platform','Decision Support']):
        col.markdown(f'<div class="mini-card"><b>{title}</b></div>',unsafe_allow_html=True)

elif menu=='Jaga Mangrove':
    st.subheader('Jaga Mangrove')
    st.markdown('### Community Business Tourism & Maritime Ecotourism')
    tabs=st.tabs(['Ecotourism','Community Business','Education','Conservation'])
    content=[('Mangrove Discovery Experience','Guided ecological trails, maritime landscape exploration and local cultural interpretation.'),('Community Enterprise','Community-led guiding, local products and conservation-based tourism businesses.'),('Digital Conservation Education','Interpretive experiences connecting mangrove ecology and CAPTRACE technology.'),('Participatory Restoration','Community participation in restoration, monitoring and ecosystem stewardship.')]
    for tab,(title,description) in zip(tabs,content):
        with tab:
            st.subheader(title)
            st.write(description)

st.divider()
with st.expander('Data sources & methodology'):
    st.write('Current dashboard indicators and mapped device points use scenario datasets for interface testing. Replace them with verified field records before operational use.')
st.caption('CAPTRACE  |  Mangrove Conservation Intelligence System')
