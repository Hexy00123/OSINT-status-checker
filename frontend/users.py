import streamlit as st
import requests
from config import API_URL


def fetch_users():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch users.")
        return []


def add_user(username):
    response = requests.post(API_URL, json={"username": username})
    if response.status_code == 201:
        st.success("User added successfully.")
    else:
        st.error("Failed to add user.")


def update_user(user_id, username):
    response = requests.put(f"{API_URL}/{user_id}",
                            json={"username": username})
    if response.status_code == 200:
        st.success("User updated successfully.")
    else:
        st.error("Failed to update user.")


def delete_user(user_id):
    response = requests.delete(f"{API_URL}/{user_id}")
    if response.status_code == 204:
        st.success("User deleted successfully.")
    else:
        st.error("Failed to delete user.")


st.title("Users")
# users = fetch_users()


# Add new user
col1, col2 = st.columns([5, 1])
with col1:
    new_user_name = st.text_input("", label_visibility="collapsed")
with col2:
    if st.button("Add User", use_container_width=True, type='primary'):
        # add_user(new_user_name)
        st.experimental_rerun()
st.divider()


# Display and edit users
for user in [{"id": 321312, "username": 'sdasd'}, {"id": 2, "username": 'sdasd'}]:
    col1, col2, col3 = st.columns([5, 0.5, 0.5])
    with col1:
        new_username = st.text_input(
            "", value=user['username'], key=f"edit_{user['id']}", label_visibility="collapsed")
    with col2:
        if st.button("✍️", key=f"update_{user['id']}", use_container_width=True):
            update_user(user['id'], new_username)
            st.experimental_rerun()
    with col3:
        if st.button("🗑", key=f"delete_{user['id']}", use_container_width=True):
            delete_user(user['id'])
            st.experimental_rerun()

st.write(
    """<style>
    [data-testid="stHorizontalBlock"] {
        align-items: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True
)
