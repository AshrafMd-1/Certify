import streamlit as st

from config.db import events_db, participants_db, certificate_db, templates_db
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

    if event:

        event_data = [
            event_data for event_data in all_event_data.items if event_data["key"] == event.split(" | ")[0]]
        event_data = event_data[0]

        wide_table(["Title", "Detail", "Participants Count"],
                   [event_data["name"], event_data["detail"], event_data["participant_count"]]
                   )

        if event_data["participant_count"] is not None:
            st.write("Participants")
            participants = participants_db.get(event_data["key"])
            part = participants["participants"]
            st.dataframe(part, use_container_width=True)

        if event_data["extension"] is not None:
            st.write("Certificates")
            certificate = templates_db.get(f"{event_data['key']}.{event_data['extension']}")
            st.image(certificate.read(), use_column_width=True)
