import streamlit as st
from config import init_app
from users_utils import fetch_users, add_user


class UsersPage:
    PAGE_NAME = 'Users'

    def __init__(self):
        init_app(self.PAGE_NAME)
        st.title(self.PAGE_NAME)
        st.caption(
            "Only Telegram users are applicable")

        col1, col2 = st.columns([5, 1])
        with col1:
            new_user_name = st.text_input(
                "New User", label_visibility="collapsed")
        with col2:
            if st.button("Add User", use_container_width=True, type='primary'):
                add_user(new_user_name)
                st.experimental_rerun()
        st.divider()

        with st.spinner():
            if 'users' not in st.session_state:
                st.session_state['users'] = fetch_users()
            for user in st.session_state['users']:
                if user['app'] == 'tg':
                    st.write(
                        f"[{user['username']}](https://t.me/{user['username']})")
                else:
                    st.write(user['username'])


if __name__ == '__main__':
    UsersPage()
