import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from folium.plugins import MarkerCluster, MiniMap, Fullscreen, MeasureControl, MousePosition
from streamlit_folium import st_folium
from datetime import date, timedelta
from html import escape

st.set_page_config(page_title='CAPTRACE | Coastal Intelligence', layout='wide', initial_sidebar_state='expanded')
G='#078F78'; NAVY='#12394A'; CYAN='#0BA6C6'; GOLD='#D7A84A'; MUTED='#607A82'

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html,body,.stApp,[data-testid="stAppViewContainer"]{background:#F1F7F8!important;color:#143947!important;font-family:'DM Sans',sans-serif!important}
[data-testid="stHeader"]{background:rgba(241,247,248,.88)!important}
[data-testid="stSidebar"]{background:linear-gradient(170deg,#093E43,#092D40)!important;border-right:1px solid #14636A}
[data-testid="stSidebar"] *{color:#F1FFFF!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:9px 12px;border-radius:11px;margin:3px 0}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:#176B68!important}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;color:#12394A!important;letter-spacing:-.035em!important}
h1{font-size:2.5rem!important}h2{font-size:1.55rem!important}
[data-testid="stMetric"]{background:#fff;border:1px solid #DDEBED;border-radius:17px;padding:19px;box-shadow:0 9px 27px #0A48510A}
[data-testid="stMetricLabel"]{font-weight:700;color:#57717A!important}
[data-testid="stMetricValue"]{font-family:'Space Grotesk';color:#0C655D!important;font-size:2rem!important}
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"]{background:white;border:1px solid #DDEBED;border-radius:17px;padding:8px}
.stButton button[kind="primary"], .stDownloadButton button{background:#087D70;color:white;border:0;border-radius:11px}
.stTabs [data-baseweb="tab"]{font-weight:700}
.hero{background:linear-gradient(118deg,#063D46,#087D77 64%,#0C91A7);border-radius:22px;padding:32px 35px;color:#fff;position:relative;overflow:hidden;margin-bottom:24px;box-shadow:0 16px 34px #0B5D6220}
.hero:after{content:'';position:absolute;width:320px;height:320px;border:1px solid #FFFFFF40;border-radius:50%;right:-75px;top:-150px;box-shadow:0 0 0 40px #FFFFFF0B,0 0 0 85px #FFFFFF08;pointer-events:none}
.hero .eyebrow{font-size:11px;letter-spacing:2.4px;color:#B6F4EA;font-weight:800}
.hero .title{font:700 38px 'Space Grotesk',sans-serif;letter-spacing:-1.5px;color:white;margin:10px 0}
.hero .desc{font-size:14px;color:#D8F5F3;max-width:720px}
.panel{background:white;border:1px solid #DCEAEC;border-radius:17px;padding:21px;margin:8px 0 18px;box-shadow:0 8px 28px #0A485109}
.panel-title{font:700 17px 'Space Grotesk',sans-serif;color:#164653;margin-bottom:8px}
.panel-text{font-size:13px;line-height:1.7;color:#5B7680}
.badge{display:inline-block;padding:5px 10px;background:#E0F5F0;color:#086A5C;border-radius:20px;font-size:11px;font-weight:800;letter-spacing:.7px}
.step{display:inline-block;border:1px solid #CBE7E4;background:#F6FBFA;border-radius:12px;padding:13px;margin:5px;color:#174D54;font-weight:700}
small{color:#5B7580}
@media(max-width:700px){.hero{padding:23px}.hero .title{font-size:27px}}
</style>''',unsafe_allow_html=True)

@st.cache_data
def make_data():
    r=np.random.default_rng(2026)
    zones=['Z1 | Seaward','Z2 | Transition','Z3 | Landward']
    species=['Avicennia marina','Avicennia alba','Rhizophora mucronata','Rhizophora apiculata','Sonneratia alba']
    sensors=pd.DataFrame({'Sensor ID':[f'AJR-{i:03}' for i in range(1,37)],'Zone':r.choice(zones,36),'Temperature (°C)':r.uniform(27,34,36).round(1),'Salinity (ppt)':r.uniform(9,34,36).round(1),'pH':r.uniform(6.3,8.4,36).round(2),'Moisture (%)':r.uniform(48,91,36).round(1),'Latitude':-6.94+r.uniform(-.023,.023,36),'Longitude':110.48+r.uniform(-.03,.03,36)})
    capsules=pd.DataFrame({'Capsule ID':[f'CAP-{i:04}' for i in range(1,301)],'Zone':r.choice(zones,300),'Species':r.choice(species,300),'Stage':r.choice(['Distributed','Observed','Established','Requires Review'],300,p=[.35,.31,.23,.11]),'Deployment Date':pd.to_datetime('2026-08-01')+pd.to_timedelta(r.integers(0,85,300),unit='D'),'Latitude':-6.94+r.uniform(-.026,.026,300),'Longitude':110.48+r.uniform(-.035,.035,300)})
    days=pd.date_range('2026-10-01',periods=42)
    history=pd.DataFrame({'Date':days,'Health Index':np.clip(50+np.arange(42)*.42+r.normal(0,2,42),0,100),'Establishment (%)':np.clip(29+np.arange(42)*.55+r.normal(0,2.2,42),0,100),'Coverage (ha)':np.clip(12+np.arange(42)*.32+r.normal(0,.8,42),0,None)})
    return sensors,capsules,history
sensors,capsules,history=make_data()

PLOT=dict(template='plotly_white',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='DM Sans',color='#244957'),margin=dict(l=12,r=12,t=22,b=20),hovermode='x unified')
def chart(fig,height=340):
    fig.update_layout(**PLOT,height=height)
    st.plotly_chart(fig,use_container_width=True,config={'displaylogo':False})
def section(title,subtitle=None):
    st.subheader(title)
    if subtitle: st.caption(subtitle)
def card(title,description,tag='CAPTRACE'):
    st.markdown(f'<div class="panel"><span class="badge">{escape(tag)}</span><div class="panel-title" style="margin-top:12px">{escape(title)}</div><div class="panel-text">{escape(description)}</div></div>',unsafe_allow_html=True)

def real_map(show_sensors=True,show_capsules=True,show_zones=True,basemap='OpenStreetMap',cluster=True):
    # Real-world map tiles. Point locations are intentionally generated demonstration coordinates.
    tile={'OpenStreetMap':'OpenStreetMap','Light':'CartoDB positron','Satellite':'Esri.WorldImagery'}[basemap]
    if tile=='Esri.WorldImagery':
        m=folium.Map(location=[-6.94,110.48],zoom_start=12,tiles=None,control_scale=True)
        folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr='Tiles © Esri and contributors',name='Esri satellite').add_to(m)
    else: m=folium.Map(location=[-6.94,110.48],zoom_start=12,tiles=tile,control_scale=True)
    if show_zones:
        fg=folium.FeatureGroup(name='Conceptual zones')
        for name,lat,lon,radius,color in [('Z1 | Seaward',-6.927,110.476,650,'#0BA6C6'),('Z2 | Transition',-6.941,110.481,750,'#D7A84A'),('Z3 | Landward',-6.955,110.485,650,'#078F78')]:
            folium.Circle([lat,lon],radius=radius,color=color,fill=True,fill_opacity=.12,tooltip=name+' | schematic area').add_to(fg)
        fg.add_to(m)
    if show_sensors:
        fg=folium.FeatureGroup(name='Smart Ajir points (illustrative)')
        parent=MarkerCluster().add_to(fg) if cluster else fg
        for _,row in sensors.iterrows():
            folium.CircleMarker([row['Latitude'],row['Longitude']],radius=6,color='#047D70',fill=True,fill_color='#14B8A6',fill_opacity=.9,tooltip=row['Sensor ID'],popup=f"{row['Sensor ID']} | {row['Zone']} | pH {row['pH']}").add_to(parent)
        fg.add_to(m)
    if show_capsules:
        fg=folium.FeatureGroup(name='Capsule points (illustrative)')
        parent=MarkerCluster().add_to(fg) if cluster else fg
        for _,row in capsules.head(120).iterrows():
            folium.CircleMarker([row['Latitude'],row['Longitude']],radius=4,color='#147DB7',fill=True,fill_color='#24B5D2',fill_opacity=.8,tooltip=row['Capsule ID'],popup=f"{row['Capsule ID']} | {row['Species']}").add_to(parent)
        fg.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    Fullscreen().add_to(m); MiniMap(toggle_display=True).add_to(m); MeasureControl(primary_length_unit='meters').add_to(m)
    MousePosition(position='bottomright',separator=' | ',prefix='Coordinates').add_to(m)
    return m

def show_map(key,height=480):
    basemap=st.selectbox('Basemap',['OpenStreetMap','Light','Satellite'],key=f'base_{key}')
    layers=st.multiselect('Visible layers',['Smart Ajir','Capsules','Conceptual zones'],default=['Smart Ajir','Capsules','Conceptual zones'],key=f'layers_{key}')
    st_folium(real_map('Smart Ajir' in layers,'Capsules' in layers,'Conceptual zones' in layers,basemap),height=height,width=None,returned_objects=[],key=f'map_{key}')
    st.caption('Real basemap of the Sayung area. Device markers and zone overlays are illustrative placements, not verified field coordinates.')

pages=['Command Center','UAV Intelligence','Capsule Tracking','Smart Ajir Network','Geospatial Explorer','Restoration Analysis','Conservation Analytics','CPS Integration','Jaga Mangrove']
with st.sidebar:
    st.markdown('<div style="font:700 32px Space Grotesk;color:white;letter-spacing:-1px;padding:10px 0">CAPTRACE<span style="color:#5BE0CE">.</span></div><div style="font-size:10px;letter-spacing:2px;color:#A4E6E2;margin-bottom:20px">COASTAL INTELLIGENCE SYSTEM</div>',unsafe_allow_html=True)
    page=st.radio('NAVIGATION',pages,label_visibility='collapsed')
    st.divider()
    st.markdown('**REGION**  \\nSayung, Demak, Central Java')
    st.caption('UAV · CAPSULE · SMART AJIR · CPS 5C')

st.markdown(f'<div class="hero"><div class="eyebrow">CAPTRACE / COASTAL RESTORATION SYSTEM</div><div class="title">{escape(page)}</div><div class="desc">Integrated mangrove intelligence, traceability, geospatial exploration and community-based maritime ecotourism.</div></div>',unsafe_allow_html=True)

if page=='Command Center':
    section('Environmental Intelligence Overview','Explore monitoring indicators, interactive layers and restoration trends.')
    a,b,c,d=st.columns(4)
    a.metric('Vegetation index',f"{history['Health Index'].iloc[-1]:.1f}",'+4.2')
    b.metric('Smart Ajir nodes',len(sensors))
    c.metric('Capsule registry',len(capsules))
    d.metric('Planning zones','03')
    left,right=st.columns([1.5,1])
    with left:
        section('Restoration trends')
        f=go.Figure()
        for col,color in [('Health Index',G),('Establishment (%)',CYAN)]: f.add_trace(go.Scatter(x=history.Date,y=history[col],name=col,mode='lines',line=dict(color=color,width=3),fill='tozeroy' if col=='Health Index' else None,fillcolor='rgba(7,143,120,.06)'))
        chart(f)
    with right:
        section('Capsule stage distribution')
        counts=capsules.Stage.value_counts()
        f=go.Figure(go.Pie(labels=counts.index,values=counts.values,hole=.7,marker_colors=[G,CYAN,GOLD,'#B2C9CE']))
        chart(f)
    section('Live map explorer interface')
    show_map('home',430)
    section('Recent registry')
    st.dataframe(capsules[['Capsule ID','Zone','Species','Stage']].tail(12),hide_index=True,use_container_width=True)

elif page=='UAV Intelligence':
    section('UAV Flight Mission Designer','Configure a conceptual mission and inspect its route geometry.')
    a,b,c=st.columns(3)
    mission=a.selectbox('Mission',['Vegetation mapping','Capsule distribution','Environmental observation'])
    altitude=b.slider('Flight altitude (m)',20,150,65)
    area=c.slider('Coverage (ha)',1,100,24)
    overlap=st.slider('Image overlap (%)',50,90,75)
    segments=max(2,int(np.ceil(area/6)))
    a,b,c=st.columns(3);a.metric('Mission legs',segments);b.metric('Altitude',f'{altitude} m');c.metric('Overlap',f'{overlap}%')
    f=go.Figure()
    xs=[];ys=[]
    for i in range(segments):
        xs.extend([0,10,None] if i%2==0 else [10,0,None]);ys.extend([i,i,None])
    f.add_trace(go.Scatter(x=xs,y=ys,mode='lines+markers',line=dict(color=G,width=4),name='Flight path'))
    f.update_layout(xaxis_title='Relative east-west distance',yaxis_title='Flight leg',showlegend=False)
    chart(f,370)
    card('Mission configuration',f'{mission} | {area} ha | {altitude} m altitude | {overlap}% overlap. Flight path is schematic, not a validated aviation plan.','MISSION PLANNER')
    st.download_button('Export mission parameters',pd.DataFrame([{'Mission':mission,'Altitude (m)':altitude,'Area (ha)':area,'Overlap (%)':overlap,'Segments':segments}]).to_csv(index=False),'captrace_mission.csv','text/csv')

elif page=='Capsule Tracking':
    section('Capsule Traceability Registry','Search, filter and inspect individual restoration capsules.')
    a,b,c=st.columns(3)
    q=a.text_input('Capsule ID search',placeholder='CAP-0001')
    zone=b.selectbox('Zone',['All']+sorted(capsules.Zone.unique()))
    stage=c.selectbox('Stage',['All']+sorted(capsules.Stage.unique()))
    df=capsules.copy()
    if q:df=df[df['Capsule ID'].str.contains(q,case=False,regex=False)]
    if zone!='All':df=df[df.Zone==zone]
    if stage!='All':df=df[df.Stage==stage]
    a,b,c=st.columns(3);a.metric('Matching records',len(df));b.metric('Species',df.Species.nunique());c.metric('Zones',df.Zone.nunique())
    st.dataframe(df[['Capsule ID','Zone','Species','Stage','Deployment Date']],hide_index=True,use_container_width=True)
    st.download_button('Export filtered capsules',df.to_csv(index=False),'captrace_capsule_registry.csv','text/csv')
    if len(df):
        chosen=st.selectbox('Inspect capsule',df['Capsule ID'])
        row=df[df['Capsule ID']==chosen].iloc[0]
        card(chosen,f"Species: {row['Species']} | Zone: {row['Zone']} | Stage: {row['Stage']} | Registered date: {row['Deployment Date'].date()}",'TRACEABILITY RECORD')
    section('Distribution by species')
    species_count=df.Species.value_counts().reset_index();species_count.columns=['Species','Count']
    if len(species_count):chart(px.bar(species_count,x='Count',y='Species',orientation='h',color='Count',color_continuous_scale=['#C6F0E5',G]),330)

elif page=='Smart Ajir Network':
    section('Smart Ajir Digital Twin','Inspect environmental parameters for each virtual sensor node.')
    sid=st.selectbox('Select Smart Ajir',sensors['Sensor ID'])
    row=sensors[sensors['Sensor ID']==sid].iloc[0]
    a,b,c,d=st.columns(4)
    for col,label,unit in [(a,'Temperature (°C)','°C'),(b,'Salinity (ppt)',' ppt'),(c,'pH',''),(d,'Moisture (%)','%')]:
        col.metric(label,f'{row[label]}{unit}')
    days=pd.date_range('2026-10-01',periods=30)
    r=np.random.default_rng(int(sid[-3:]))
    metric=st.selectbox('Trend parameter',['Temperature (°C)','Salinity (ppt)','pH','Moisture (%)'])
    trend=row[metric]+r.normal(0,{'Temperature (°C)':.8,'Salinity (ppt)':1.7,'pH':.18,'Moisture (%)':3.2}[metric],len(days))
    f=go.Figure(go.Scatter(x=days,y=trend,mode='lines+markers',line=dict(color=G,width=3),fill='tozeroy',fillcolor='rgba(7,143,120,.08)'))
    chart(f,380)
    section('Sensor comparison')
    col=st.selectbox('Compare network parameter',['Temperature (°C)','Salinity (ppt)','pH','Moisture (%)'],key='sensor_compare')
    chart(px.box(sensors,x='Zone',y=col,color='Zone'),360)
    st.dataframe(sensors.drop(columns=['Latitude','Longitude']),hide_index=True,use_container_width=True)

elif page=='Geospatial Explorer':
    section('Sayung Geospatial Explorer','Explore real geographic basemaps, map tools and selectable restoration layers.')
    show_map('geo',620)
    st.markdown('**Map tools:** zoom, full screen, measurement, mini map, coordinates, layer visibility and marker popups.')
    card('Geographic accuracy','OpenStreetMap / Esri tiles display real geographic imagery or cartography. Planning circles and device markers are conceptual and must be replaced with surveyed GPS data before field use.','MAP DATA')

elif page=='Restoration Analysis':
    section('Restoration Decision Support','Adjust environmental parameters and compare indicative site conditions.')
    a,b=st.columns(2)
    with a:
        sal=st.slider('Salinity (ppt)',0,45,20)
        ph=st.slider('Soil pH',3.,10.,7.,.1)
        substrate=st.selectbox('Substrate',['Mud','Sandy mud','Sand'])
    with b:
        temp=st.slider('Temperature (°C)',20,40,29)
        flood=st.selectbox('Tidal inundation',['Low','Moderate','High'])
        exposure=st.selectbox('Wave exposure',['Sheltered','Moderate','Exposed'])
    score=(25 if 10<=sal<=30 else 8)+(20 if 6<=ph<=8.5 else 5)+(15 if 25<=temp<=33 else 5)+(15 if substrate=='Mud' else 10 if substrate=='Sandy mud' else 3)+(15 if flood=='Moderate' else 8)+(10 if exposure=='Sheltered' else 6 if exposure=='Moderate' else 2)
    a,b=st.columns([1,2]);a.metric('Indicative suitability',f'{score}/100')
    with b:
        fig=go.Figure(go.Indicator(mode='gauge+number',value=score,gauge={'axis':{'range':[0,100]},'bar':{'color':G},'steps':[{'range':[0,45],'color':'#FCE8E6'},{'range':[45,75],'color':'#FFF2D8'},{'range':[75,100],'color':'#D9F4EA'}]}))
        chart(fig,260)
    section('Species screening')
    # Demonstrative logic only: no claim of validated ecological species thresholds.
    suggestions={'Mud':['Avicennia marina','Rhizophora mucronata'],'Sandy mud':['Avicennia alba','Sonneratia alba'],'Sand':['Site-specific substrate assessment needed']}
    for sp in suggestions[substrate]:card(sp,'Candidate for further site-specific ecological assessment; verify tidal position, hydrology and local species records.','SCREENING')
    st.caption('This decision aid uses illustrative rules, not validated species suitability or field measurements.')

elif page=='Conservation Analytics':
    section('Conservation Analytics Studio','Compare indicators, inspect distributions and export selected records.')
    a,b=st.columns(2)
    metric=a.selectbox('Indicator',['Health Index','Establishment (%)','Coverage (ha)'])
    view=b.selectbox('Visualization',['Area trend','Bar trend','Rolling average'])
    values=history[metric].rolling(7,min_periods=1).mean() if view=='Rolling average' else history[metric]
    f=go.Figure()
    if view=='Bar trend':f.add_trace(go.Bar(x=history.Date,y=values,marker_color=G))
    else:f.add_trace(go.Scatter(x=history.Date,y=values,mode='lines+markers',line=dict(color=G,width=3),fill='tozeroy' if view=='Area trend' else None,fillcolor='rgba(7,143,120,.1)'))
    chart(f,430)
    a,b=st.columns(2)
    with a:
        section('Capsule stages by zone')
        cross=pd.crosstab(capsules.Zone,capsules.Stage).reset_index()
        chart(px.bar(cross,x='Zone',y=[x for x in cross.columns if x!='Zone'],barmode='stack'),350)
    with b:
        section('Environmental parameter relationships')
        chart(px.scatter(sensors,x='Salinity (ppt)',y='pH',color='Zone',hover_name='Sensor ID',size='Moisture (%)'),350)
    st.download_button('Export analytics dataset',history.to_csv(index=False),'captrace_analytics.csv','text/csv')

elif page=='CPS Integration':
    section('Cyber-Physical System Architecture','Explore the CAPTRACE 5C integration pathway.')
    steps=[('01','Connection','UAV imagery, Smart Ajir sensing, capsule identifiers and connectivity.'),('02','Conversion','Transform measurements and imagery into structured environmental indicators.'),('03','Cyber','Store linked spatial records and capsule traceability histories.'),('04','Cognition','Support interpretation, visualization and restoration decisions.'),('05','Configuration','Translate evidence into adaptive field management actions.')]
    selected=st.select_slider('Select CPS layer',options=[s[1] for s in steps])
    st.markdown(''.join(f'<span class="step">{escape(n)} · {escape(name)}</span>' for n,name,_ in steps),unsafe_allow_html=True)
    for n,name,desc in steps:
        if name==selected:card(name,desc,'CPS '+n)
    section('Technology relationship')
    flow=go.Figure(go.Sankey(node=dict(label=['UAV','Capsules','Smart Ajir','Data platform','Decision support','Field action'],pad=20,thickness=19,color=[CYAN,G,GOLD,NAVY,G,CYAN]),link=dict(source=[0,1,2,3,4],target=[3,3,3,4,5],value=[3,2,3,8,8],color=['rgba(11,166,198,.25)','rgba(7,143,120,.25)','rgba(215,168,74,.3)','rgba(18,57,74,.2)','rgba(7,143,120,.25)'])))
    chart(flow,380)

elif page=='Jaga Mangrove':
    section('Jaga Mangrove | Maritime Ecotourism','Integrating conservation, community enterprise, technology and coastal culture.')
    tabs=st.tabs(['Experience builder','Community business','Interpretation','Conservation'])
    with tabs[0]:
        activity=st.multiselect('Choose activities',['Mangrove interpretation walk','Capsule traceability discovery','Smart Ajir learning station','Local coastal culinary experience','Community restoration workshop'],default=['Mangrove interpretation walk','Smart Ajir learning station'])
        people=st.number_input('Participants',1,50,10)
        duration=st.slider('Duration (hours)',1,8,3)
        st.metric('Selected activities',len(activity));st.metric('Participant-hours',people*duration)
        st.dataframe(pd.DataFrame({'Selected experience':activity}),hide_index=True,use_container_width=True)
    with tabs[1]:
        for title,desc in [('Local guides','Community-managed ecological guiding and interpretation.'),('Microenterprise','Local food, handicrafts and responsible visitor services.'),('Community reinvestment','Transparent allocation for community activities and conservation support.')]:card(title,desc,'COMMUNITY BUSINESS')
    with tabs[2]:
        topic=st.selectbox('Learning module',['Mangrove ecology','UAV and restoration capsules','Smart Ajir environmental monitoring','CPS 5C traceability'])
        card(topic,'Use this module as an interactive educational station during guided maritime ecotourism experiences.','DIGITAL INTERPRETATION')
    with tabs[3]:
        for title,desc in [('Citizen monitoring','Community participation in observation and ecological reporting.'),('Restoration stewardship','Joint maintenance and follow-up monitoring of restoration areas.'),('Cultural interpretation','Connect local coastal livelihoods and cultural narratives with conservation education.')]:card(title,desc,'CONSERVATION')

st.divider()
with st.expander('Data provenance and methodology'):
    st.write('CAPTRACE interface demonstration. Sensor readings, capsule registries, performance trends, markers and zone circles are generated illustrative records. The map baselayers themselves use real-world OpenStreetMap or Esri geographic tiles. Replace demonstration data with validated field observations for operational use.')
st.caption('CAPTRACE  |  SAYUNG COASTAL INTELLIGENCE  |  UAV · CAPSULE · SMART AJIR · CPS')
