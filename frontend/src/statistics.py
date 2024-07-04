import streamlit as st
import matplotlib.pyplot as plt

from config import API_URL
from requests import get
import datetime

st.title("Statistics")

data = get(API_URL + '/status').json()
statistic = []

for user in data:
    user['ts'] = user['ts'].split('.')[0]
    datetime_ts = datetime.datetime.strptime(user['ts'], '%Y-%m-%dT%H:%M:%S')
    statistic.append(float(f'{datetime_ts.hour}.{datetime_ts.minute}'))

width = st.sidebar.slider("plot width", 1, 25, 16)
height = st.sidebar.slider("plot height", 1, 25, 9)

fig, ax = plt.subplots(figsize=(width, height))
ax.hist(statistic)
ax.set_xlabel('Time')
ax.set_ylabel('# of users')
plt.title('Online statistic distribution')
ax.legend()
st.pyplot(fig)
