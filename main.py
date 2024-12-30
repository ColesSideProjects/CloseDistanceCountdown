import pandas as pd
import streamlit as st
from Dates import Dates
import plotly.express as px
from datetime import date, datetime, timedelta

df, stats = Dates.get_dfs()

fig = px.line(
    df,
    x="date2",
    y="moving average",
    title="Our Timeline",
    labels={"moving average": "Our Timeline", "date2": "Date"},
    hover_data={"name": True, "adjusted days": True}
)

day_till_1_date = date.today() + timedelta(days=int(stats["Days Till 1"][0]))
day_365 = date.today() + timedelta(days=int(stats["Days Till One Year"][0]))

st.title("Close Distance Countdown")

st.text(f'{int(stats["Days Together"][0])} days together')
st.text(f'{int(stats["Days Separated"][0])} days separated')
st.text(f'{int(stats["Days Till 1"][0])} days till we have been together more than apart')
st.text("")
st.text("🎉 Upcoming Dates 🎉")
st.text(f'Day +1: {day_till_1_date} ')
st.text(f'365 days together: {day_365} ')
st.plotly_chart(fig)




