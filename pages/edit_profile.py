import time

import streamlit as st

from config.db import logins_db
from config.menu import menu_with_redirect

menu_with_redirect()

st.header("Edit your profile")
st.write("You can edit your profile here")

with st.form("edit_form"):
    name = st.text_input("Name", value=st.session_state.user_data['name'])
    position = st.text_input(
        "Position", value=st.session_state.user_data['position'])
    year = st.text_input("Year", value=st.session_state.user_data['year'])
    st.selectbox("Access", options=["sadmin"], disabled=True)
    submitted = st.form_submit_button("Submit")
    if submitted:
        name = name.strip()
        role = position.strip()
        year = year.strip()
        if len(name) == 0 or len(position) == 0 or len(year) == 0:
            st.error("All fields are required")
        logins_db.update({
            "name": st.session_state.user_data['name'],
            "position": st.session_state.user_data['position'],
            "year": st.session_state.user_data['year'],
        }, st.session_state.user_data['username'])
        st.session_state.user_data['name'] = name
        st.session_state.user_data['position'] = role
        st.session_state.user_data['year'] = year
        st.success("Profile updated successfully")
        time.sleep(1)
        st.switch_page("pages/profile.py")

back = st.button("Back")
if back:
    st.switch_page("pages/profile.py")
