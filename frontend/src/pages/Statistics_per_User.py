import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from statistics_utils import preprocess_data_for_distribution
from users_utils import fetch_users
from config import API_URL, init_app
from requests import get
from datetime import datetime


class StatisticsPerUserPage:
    PAGE_NAME = 'Statistics per User'

    def __init__(self):
        init_app(self.PAGE_NAME)
        st.title(self.PAGE_NAME)

        st.sidebar.header('Date & Time Interval (UTC)')

        st.sidebar.subheader('Start')
        col1, col2 = st.sidebar.columns(2)
        date_start = col1.date_input(
            "Date", key="date_start", label_visibility="collapsed", value=None)
        time_start = col2.time_input(
            "Time", key="time_start", label_visibility="collapsed", value=None)
        self.start_ts = None
        if date_start is not None and time_start is not None:
            self.start_ts = datetime.timestamp(
                datetime.combine(date_start, time_start))

        st.sidebar.subheader('End')
        col3, col4 = st.sidebar.columns(2)
        date_end = col3.date_input(
            "Date", key="date_end", label_visibility="collapsed", value=None)
        time_end = col4.time_input(
            "Time", key="time_end", label_visibility="collapsed", value=None)
        self.end_ts = None
        if date_end is not None and time_end is not None:
            self.end_ts = datetime.timestamp(
                datetime.combine(date_end, time_end))

        st.sidebar.header('Plot Settings')

        st.sidebar.subheader('Bins')
        self.bins = st.sidebar.slider(
            "bins", 1, 50, 24, label_visibility="collapsed")
        st.sidebar.subheader('Width')
        self.plot_width = st.sidebar.slider(
            "plot width", 1, 25, 16, label_visibility="collapsed")
        st.sidebar.subheader('Height')
        self.plot_height = st.sidebar.slider(
            "plot height", 1, 25, 8, label_visibility="collapsed")

        col1, col2 = st.columns([4, 1])
        col1.subheader('User online distribution')

        with st.spinner():
            if 'users' not in st.session_state:
                st.session_state['users'] = fetch_users()
            usernames = [user['username']
                         for user in st.session_state['users']]
            self.selected_user = col2.selectbox(
                "Select User", usernames, index=None, placeholder="Select user", label_visibility="collapsed")

        self.show_plot()

    def show_plot(self):
        if self.selected_user is not None:
            with st.spinner():
                raw_data = get(API_URL + '/status/read-by', params={'username': self.selected_user,
                                                                    'start': self.start_ts,
                                                                    'end': self.end_ts}
                               ).json()
                data = preprocess_data_for_distribution(raw_data)
                if len(data) == 0:
                    st.warning('No data found')
                    return
                fig, ax = plt.subplots(
                    figsize=(self.plot_width, self.plot_height))

                sns.histplot(data, ax=ax, bins=self.bins,
                             alpha=0.25, color='blue', kde=True)
                ax.set_xlim(0, 24)
                ax.set_xticks(range(0, 25, 1))
                ax.set_xlabel('Day Time')
                ax.set_ylabel('Aggregated User Online')
                st.pyplot(fig)


if __name__ == '__main__':
    StatisticsPerUserPage()
