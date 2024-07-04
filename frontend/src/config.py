import streamlit as st

APP_NAME = 'User Status Analyzer'
API_URL = 'http://158.160.101.116:8000'


def init_app(page_title):
    st.set_page_config(page_title=page_title, layout="wide",
                       initial_sidebar_state="expanded")
    st.sidebar.title(APP_NAME)
