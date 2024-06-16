import streamlit as st

from config.db import events_db
from config.menu import menu_with_redirect
from utils.common import wide_table

menu_with_redirect()

st.header("Events")
st.write("You can view all the events here")
all_event_data = events_db.fetch()
all_events_name = []
if not all_event_data is None and not all_event_data.count == 0:
    all_events_name = [event["key"] + ' | ' + event['name'] for event in all_event_data.items]

if len(all_events_name) == 0:
    st.write("No events found")
else:
    event = st.selectbox("Select an event", all_events_name, index=None,
                         placeholder="Select an event")

    event_data = [
        event_data for event_data in all_event_data.items if event_data["key"] == event.split(" | ")[0]]
    event_data = event_data[0]

    wide_table(["Title", "Detail"],
               [event_data["name"], event_data["detail"]]
               )
