import streamlit as st


st.set_page_config(layout="wide")

st.sidebar.title("User Status Analyzer")


# Filters shared by all the pages TODO
st.sidebar.header('Date & Time Interval')

st.sidebar.subheader('Start')
st.sidebar.date_input("Date", key="date_start", label_visibility="collapsed")
st.sidebar.time_input("Time", key="time_start", label_visibility="collapsed")

st.sidebar.subheader('End')
st.sidebar.date_input("Date", key="date_end", label_visibility="collapsed")
st.sidebar.time_input("Time", key="time_end", label_visibility="collapsed")

st.sidebar.header('Intercations Threshold')
st.sidebar.slider("Threshold", 0, 100, 10, label_visibility="collapsed")

st.sidebar.button('🔄 Refresh', type="primary", use_container_width=True)

pg = st.navigation(
    [
        st.Page('graph.py', title="Graph"),
        st.Page('statistics.py', title="Statistics"),
        st.Page('users.py', title="Users"),
    ]
)


pg.run()
