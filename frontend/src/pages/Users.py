import streamlit as st
import requests
from config import API_URL, init_app


class UsersPage:
    PAGE_NAME = 'Users'

    def __init__(self):
        # init_app(self.PAGE_NAME)
        st.title(self.PAGE_NAME)

        if 'users' not in st.session_state:
            st.session_state['users'] = self.fetch_users()
        users = st.session_state['users']

        col1, col2 = st.columns([5, 1])
        with col1:
            new_user_name = st.text_input("", label_visibility="collapsed")
        with col2:
            if st.button("Add User", use_container_width=True, type='primary'):
                self.add_user(new_user_name)
                st.experimental_rerun()
        st.divider()

        for user in users:
            st.text_input("", value=user['username'], label_visibility="collapsed")

        st.write(
            """<style>
            [data-testid="stHorizontalBlock"] {
                align-items: flex-end;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    def fetch_users(self):
        response = requests.get(API_URL + '/user')

        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch users.")
            return []

    def add_user(self, username):
        response = requests.post(API_URL + '/user', json={"username": username, 'app': 'tg'})
        if response.status_code == 201:
            st.success("User added successfully.")
        else:
            st.error("Failed to add user.")

    def update_user(self, user_id, username):
        response = requests.put(f"{API_URL}/{user_id}",
                                json={"username": username})
        if response.status_code == 200:
            st.success("User updated successfully.")
        else:
            st.error("Failed to update user.")

    def delete_user(self, user_id):
        response = requests.delete(f"{API_URL}/{user_id}")
        if response.status_code == 204:
            st.success("User deleted successfully.")
        else:
            st.error("Failed to delete user.")


if __name__ == '__main__':
    UsersPage()
