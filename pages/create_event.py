import time

import streamlit as st

from config.db import events_db
from config.menu import menu_with_redirect
from utils.common import capitalize_name

menu_with_redirect()

st.header("Enter the event details")
st.write("You can create an event here")
with st.form("create_event_form"):
    event_name = st.text_input("Enter the name of the event",value="")
    event_detail = st.text_area("Enter the description of the event",value="")
    submit = st.form_submit_button("Create Event")
    if submit:
        if len(event_name) == 0 or len(event_detail) == 0:
            st.error("All fields are required")
        else:
            event_name_new = capitalize_name(event_name)
            event_detail_new = event_detail.strip()
            events_db.put({
                "name": event_name_new,
                "detail": event_detail_new,
                "participant_count": None,
                "extension": None,
            })
            st.success("Event created successfully")
            time.sleep(1)
            st.switch_page("pages/add_participants.py")
