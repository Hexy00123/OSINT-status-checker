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

        st.sidebar.header('Intercations Threshold (%)')
        st.sidebar.caption(
            'The lower the number, the more connected users will be')
        interactions_threshold = st.sidebar.slider(
            "Threshold", 0, 100, 10, label_visibility="collapsed", format="%d%%") / 100

        st.sidebar.subheader('Physics')
        physics = st.sidebar.checkbox('Physics')

        self.show_graph(
            interactions_threshold=interactions_threshold, physics=physics)

    def show_graph(self, interactions_threshold, physics):
        st.subheader(
            'Possible users interactions graph')
        with st.spinner():
            raw_data = get(API_URL + '/status/read-by', params={'start': self.start_ts,
                                                                'end': self.end_ts}
                           ).json()
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
