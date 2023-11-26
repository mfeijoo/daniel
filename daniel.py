import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from glob import glob
st.title("Primer streamlit Daniel")
listoffiles = glob('*.csv')
fileselected = st.selectbox('Select any file you want to study', listoffiles)
df = pd.read_csv(fileselected, skiprows = 4)

#find Zeros
zeros = df.loc[df.time < 3, 'ch0':].mean()
dfzeros = df.loc[:, 'ch0':] - zeros
dfzeros.columns = ['ch0z', 'ch1z']
dfz = pd.concat([df, dfzeros], axis =1)
st.write(dfz.head())

#Find when the beam starts
timestarts = dfz.loc[dfz.ch0z > 0.5, 'time'].min()

#Find with the beam ends
timeends = dfz.loc[dfz.ch0z > 0.5, 'time'].max()

#Find shots
cutoff = st.slider('choose the optimal cutoff for finding shots', min_value=40, max_value=1000, value=80)
dfz['chunk'] = dfz.number // cutoff
dfg = dfz.groupby('chunk').agg({'time':np.median, 'ch0z':np.sum})
dfg['ch0diff'] = dfg.ch0z.diff()
dfstarttimes = dfg.loc[dfg.ch0diff > 80, 'time'].reset_index()
dfstarttimes['nextime'] = dfstarttimes.time.shift()
dfstarttimes['timediff'] = dfstarttimes.time.diff()
dfstarttimes['isdiff'] = dfstarttimes.timediff > 2
stss = [dfstarttimes.time[0]] + dfstarttimes.loc[dfstarttimes.isdiff, 'time'].to_list()
sts = [i - 0.5 for i in stss]
df0 = dfz.loc[:, ['time', 'ch0z']]
df1 = dfz.loc[:, ['time', 'ch1z']]
df0.columns = ['time', 'value']
df1.columns = ['time', 'value']
df0['channel'] = 'ch0'
df1['channel'] = 'ch1'
dftp = pd.concat([df0, df1])
fig = px.line(dftp, x='time', y='value', color = 'channel', title = 'grafica 1', markers = True)
fig.update_traces(marker=dict(size=5))
for t in sts:
    fig.add_vline(x=t, line_dash='dash', line_color = 'green', opacity = 0.5)
fig.add_vline(x=timeends, line_dash='dash', line_color = 'red', opacity = 0.5)
st.plotly_chart(fig)
