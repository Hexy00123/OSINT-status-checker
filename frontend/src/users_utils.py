import requests
from config import API_URL


def fetch_users():
    response = requests.get(API_URL + '/user')

    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch users.")
        return []


def add_user(username):
    response = requests.post(
        API_URL + '/user', json={"username": username, 'app': 'tg'})
    if response.status_code == 201:
        st.success("User added successfully.")
    else:
        st.error("Failed to add user.")
