import time

import streamlit as st

from config.db import events_db
from config.menu import menu_with_redirect
from utils.common import capitalize_name
from utils.event import max_allowed_offset_year

menu_with_redirect()

st.header("Enter the event details")
st.write("You can create an event here")
with st.form("create_event_form"):
    st.write("Enter the event details")
    event_name = st.text_input("Enter the name of the event", value="")
    event_detail = st.text_area("Enter the description of the event", value="")
    event_date = st.date_input("Enter the date of the event", value=None)
    event_time = st.time_input("Enter the time of the event", value=None)
    event_location = st.text_input("Enter the location of the event", value="")
    event_link = st.text_input("Enter the link of the event", value="")
    submit = st.form_submit_button("Create Event")
    if submit:
        if len(event_name) == 0 or len(event_detail) == 0 or event_date is None or event_time is None or len(
                event_location) == 0 or len(event_link) == 0:
            st.error("All fields are required")
        elif not max_allowed_offset_year(event_date.year, 10):
            st.error("Event date should be within 10 years from now")
        else:
            event_name_new = capitalize_name(event_name)
            event_detail_new = event_detail.strip()
            event_date_new = event_date.strftime("%Y-%m-%d")
            event_time_new = event_time.strftime("%H:%M:%S")
            event_location_new = event_location.strip()
            event_link_new = event_link.strip()
            events_db.put({
                "name": event_name_new,
                "detail": event_detail_new,
                "date": event_date_new,
                "time": event_time_new,
                "location": event_location_new,
                "link": event_link_new,
                "participant": None,
                "certificate": None
            })
            event_name = ""
            event_detail = ""
            event_date = None
            event_time = None
            event_location = ""
            event_link = ""
            st.success("Event created successfully")
            time.sleep(1)
            st.rerun()
