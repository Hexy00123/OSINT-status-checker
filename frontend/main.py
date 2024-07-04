import streamlit as st


st.set_page_config(layout="wide")

st.sidebar.title("User Status Analyzer")


# Filters shared by all the pages TODO
st.sidebar.selectbox("Foo", ["A", "B", "C"], key="foo")
st.sidebar.checkbox("Bar", key="bar")
st.sidebar.button('Refresh', use_container_width=True)

pg = st.navigation(
    [
        st.Page('graph.py', title="Graph"),
        st.Page('statistics.py', title="Statistics"),
        st.Page('users.py', title="Users"),
    ]
)

pg.run()
