import time

import streamlit as st

from config.db import logins_db
from config.menu import menu
from utils.logout import clear_session

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if st.session_state.user_data['access'] is not None:
    clear_session()
    st.success("You have been logged out")
    time.sleep(1)
    st.rerun()
else:
    st.title("Certify")
    st.write("### A platform that helps you manage your certificates")

    with st.form("auth_form"):
        st.write("### Login")
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button("Submit")
        if submitted:
            if len(username) == 0 or len(password) == 0:
                st.error("All fields are required")
            else:
                username = username.strip().lower()
                password = password.strip()
                with st.spinner('Authenticating...'):
                    logged_user = logins_db.get(username)
                    if not logged_user or len(logged_user) == 0:
                        st.error('Login Failed')
                    else:
                        if logged_user['password'] == password:
                            st.session_state.access = logged_user['access']
                            st.session_state.user_data = {
                                'username': logged_user['key'],
                                'name': logged_user['name'],
                                'position': logged_user['position'],
                                'access': logged_user['access'],
                                'year': logged_user['year'],
                                'password': logged_user['password']
                            }
                            st.success('Login Successful')
                            st.switch_page("pages/profile.py")
                        else:
                            st.error('Wrong Password')

menu()
