import streamlit as st
import matplotlib.pyplot as plt
from statistics_utils import preprocess_data
from config import API_URL, init_app
from requests import get


class StatisticsPage:

    PAGE_NAME = 'Statistics'

    def __init__(self):
        init_app(self.PAGE_NAME)
        st.title(self.PAGE_NAME)

        st.sidebar.header('Plot Settings')

        st.sidebar.subheader('Width')
        width = st.sidebar.slider(
            "plot width", 1, 25, 16, label_visibility="collapsed")
        st.sidebar.subheader('Height')
        height = st.sidebar.slider(
            "plot height", 1, 25, 9, label_visibility="collapsed")

        self.fig, self.ax = plt.subplots(figsize=(width, height))
        self.show_plot()

    def show_plot(self):
        with st.spinner():
            raw_data = get(API_URL + '/status').json()
            data = preprocess_data(raw_data)
            self.ax.hist(data)
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('# of users with aggregated online time')
            plt.title('Online statistic distribution')
            self.ax.legend()
            st.pyplot(self.fig)


if __name__ == '__main__':
    StatisticsPage()
