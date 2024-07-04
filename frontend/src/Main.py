import streamlit as st
from streamlit_agraph import agraph
from graph_utils import preprocess_data, init_graph_with_sliding_window, make_graph
from requests import get
from config import API_URL, init_app


class MainPage():

    PAGE_NAME = 'Graph'

    def __init__(self):
        init_app(self.PAGE_NAME)
        st.title(self.PAGE_NAME)

        st.sidebar.header('Date & Time Interval')

        st.sidebar.subheader('Start')
        self.date_start = st.sidebar.date_input(
            "Date", key="date_start", label_visibility="collapsed")
        self.time_start = st.sidebar.time_input(
            "Time", key="time_start", label_visibility="collapsed")

        st.sidebar.subheader('End')
        self.date_end = st.sidebar.date_input(
            "Date", key="date_end", label_visibility="collapsed")
        self.time_end = st.sidebar.time_input(
            "Time", key="time_end", label_visibility="collapsed")

        st.sidebar.header('Intercations Threshold')
        interactions_threshold = st.sidebar.slider(
            "Threshold", 0, 100, 10, label_visibility="collapsed") / 100

        st.sidebar.subheader('Physics')
        physics = st.sidebar.checkbox('Physics')

        self.show_graph(
            interactions_threshold=interactions_threshold, physics=physics)

    def show_graph(self, interactions_threshold, physics):
        with st.spinner():
            raw_data = get(API_URL + "/status").json()
            data = preprocess_data(raw_data)
            graph = init_graph_with_sliding_window(
                data, time_period_seconds=20)

            st.session_state.nodes, st.session_state.edges, st.session_state.config = make_graph(graph,
                                                                                                 interactions_threshold=interactions_threshold,
                                                                                                 physics=physics)

            agraph(nodes=st.session_state.nodes,
                   edges=st.session_state.edges,
                   config=st.session_state.config)


if __name__ == '__main__':
    MainPage()
