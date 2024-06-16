import time

import pandas as pd
import streamlit as st

from config.db import events_db, participants_db
from config.menu import menu_with_redirect
from utils.common import convert_to_uppercase, capitalize_name

menu_with_redirect()

st.header("Add Participants")
st.write("You can add participants to an event here")
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
        event_data = [event_data for event_data in all_event_data.items if event_data["key"] == event.split(" | ")[0]]
        event_data = event_data[0]
        if event_data["participant_count"] is not None:
            st.write("Participants are already added")
            delete_participants = st.button("Delete Participants")
            if delete_participants:
                participants_db.delete(event.split(" | ")[0])
                events_db.update({
                    "participant_count": None
                }, event.split(" | ")[0])
                st.success("Participants deleted successfully")
                time.sleep(1)
                st.rerun()
        else:
            st.header("Step 2: Upload a CSV file")
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                df2 = df.loc[:, ['Name']]
                if 'Name' not in df2.columns:
                    st.error("Name column not found")
                    st.stop()
                df2['Name'] = df2['Name'].apply(capitalize_name)
                df2 = df2.sort_values(by='Name')
                df2['Selected'] = True
                df2.reset_index(drop=True, inplace=True)
                df2['S.No'] = df2.index + 1
                df2 = df2[['S.No', 'Name', 'Selected']]
                edited_df = st.data_editor(df2, use_container_width=True, num_rows="dynamic")
                upload = st.button("Upload")
                all_names = edited_df.loc[
                    edited_df["Selected"] == True, 'Name'].tolist()
                if upload:
                    st.write("Uploading the data")
                    events_db.update({
                        "participant_count": len(all_names)
                    }, event.split(" | ")[0])
                    participants_db.put({
                        "count": len(all_names),
                        "participants": all_names
                    }, event.split(" | ")[0])
                    st.success("Data uploaded successfully")
                    time.sleep(1)
                    st.switch_page("pages/view_event.py")
