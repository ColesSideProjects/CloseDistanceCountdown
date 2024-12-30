import pandas as pd
import streamlit as st
from Dates import Dates
import plotly.express as px


df, stats = Dates.get_dfs()

fig = px.line(
    df,
    x="date2",
    y="moving average",
    title="Days Together vs. Apart",
    labels={"moving average": "Days Together vs. Apart", "date2": "Date"},
    hover_data={"name": True, "adjusted days": True}
)



st.title("Close Distance")

st.text(f'{int(stats["Days Together"])} days together')
st.text(f'{int(stats["Days Separated"])} days separated')
st.text(f'{int(stats["Days Till 1"])} days till we have been together more than apart')
st.plotly_chart(fig)




