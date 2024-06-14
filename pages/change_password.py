import time

import streamlit as st

from config.db import logins_db
from config.menu import menu_with_redirect

menu_with_redirect()

st.header("Edit your password")
st.write("You can edit your password here")

with st.form("edit_form"):
    current_password = st.text_input("Current Password", type='password')
    new_password = st.text_input("New Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    submitted = st.form_submit_button("Submit")
    if submitted:
        current_password = current_password.strip()
        new_password = new_password.strip()
        confirm_password = confirm_password.strip()
        if len(current_password) == 0 or len(new_password) == 0 or len(confirm_password) == 0:
            st.error("All fields are required")
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            logged_user = st.session_state.user_data
            if logged_user['password'] == current_password:
                logins_db.update({
                    "password": new_password,
                }, st.session_state.user_data['username'])
                st.session_state.user_data['password'] = new_password
                st.success("Password changed successfully")
                time.sleep(1)
                st.switch_page("pages/profile.py")
            else:
                st.error("Wrong Password")

back = st.button("Back")
if back:
    st.switch_page("pages/profile.py")
