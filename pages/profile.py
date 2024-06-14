import streamlit as st

from config.menu import menu_with_redirect
from utils.common import wide_table

menu_with_redirect()

st.header(f"Welcome, *{st.session_state.user_data['name']}*")
st.divider()
st.header("Your profile")
wide_table(["Username", "Name", "Position", "Year", "Access"], [
    st.session_state.user_data['username'],
    st.session_state.user_data['name'],
    st.session_state.user_data['position'],
    st.session_state.user_data['year'],
    st.session_state.user_data['access']
])

col1, col2 = st.columns(2)
with col1:
    change_password = st.button("Change Password")
    if change_password:
        st.switch_page("pages/change_password.py")
with col2:
    edit = st.button("Edit Profile")
    if edit:
        st.switch_page("pages/edit_profile.py")
