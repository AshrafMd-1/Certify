import time

import streamlit as st

from config.db import templates_db, certificate_db, events_db
from config.menu import menu_with_redirect

menu_with_redirect()
st.header("Template")
st.write("Upload the certificate template")

if "template_image" not in st.session_state:
    st.session_state.template_image = None

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
        if event_data["extension"] is not None:
            certificate = templates_db.get(f"{event_data['key']}.{event_data['extension']}")
            st.write("Certificate template is uploaded")
            if st.session_state.template_image is not None:
                st.image(st.session_state.template_image, use_column_width=True)
                st.session_state.template_image = None
            else:
                st.image(certificate.read(), use_column_width=True)
            delete_template = st.button("Delete Template")
            if delete_template:
                certificate_db.delete(event.split(" | ")[0])
                templates_db.delete(f"{event_data['key']}.{event_data['extension']}")
                events_db.update({
                    "extension": None,
                }, event.split(" | ")[0])
                st.success("Template deleted successfully")
                time.sleep(1)
                st.rerun()
            customise = st.button("Customise Template")
            if customise:
                st.write("Customise the template")
        else:
            uploaded_image = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
            if uploaded_image is not None:
                st.image(uploaded_image, use_column_width=True)
                upload_template = st.button("Upload Template")
                st.session_state.template_image = uploaded_image
                if upload_template:
                    with st.spinner('Saving certificate template...'):
                        extension = uploaded_image.name.split(".")[-1]
                        certificate_data = certificate_db.put({
                            "fs": None,
                            "cpx": None,
                            "cpy": None,
                            "csx": None,
                            "csy": None,
                            "ha": None,
                            "fc": None,
                        }, event.split(" | ")[0])
                        templates_db.put(
                            f"{certificate_data['key']}.{extension}",
                            data=uploaded_image.read(),
                        )
                        events_db.update({
                            "extension": extension,
                        }, event.split(" | ")[0])
                        st.success("Template uploaded successfully")
                        time.sleep(1)
                    st.rerun()