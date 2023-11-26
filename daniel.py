import pandas as pd
import streamlit as st
import plotly.express as px
from glob import glob
st.title("Primer streamlit Daniel")
listoffiles = glob('*.csv')
fileselected = st.selectbox('Select any file you want to study', listoffiles)
df = pd.read_csv(fileselected, skiprows = 4)
df0 = df.loc[:, ['time', 'ch0']]
df1 = df.loc[:, ['time', 'ch1']]
df0.columns = ['time', 'value']
df1.columns = ['time', 'value']
df0['channel'] = 'ch0'
df1['channel'] = 'ch1'
dftp = pd.concat([df0, df1])
fig = px.scatter(dftp, x='time', y='value', color = 'channel', title = 'grafica 1')
fig.update_traces(marker=dict(size=3))
st.plotly_chart(fig)
