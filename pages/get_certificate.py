import io

import streamlit as st
from PIL import Image, ImageFont, ImageDraw

from config.db import certificate_db, participants_db, templates_db, events_db
from config.menu import menu

menu()

st.header("Get your certificate here")
st.write("You can get your certificate here")
st.divider()

if 'data' not in st.session_state:
    st.session_state.data = None


if 'all_event_data' not in st.session_state:
    st.session_state.all_event_data = None

if 'participants' not in st.session_state:
    st.session_state.participants = None

def on_change():
    st.session_state.fetched = False


all_event_data = events_db.fetch({
    "extension?not_contains": "None",
    "participant_count?not_contains": "None"
})

all_events_name = []
if not all_event_data is None and not all_event_data.count == 0:
    all_events_name = [event["key"] + ' | ' + event['name'] for event in all_event_data.items]

if len(all_events_name) == 0:
    st.write("No events found")
else:
    event = st.selectbox("Select an event", all_events_name, index=None,
                         placeholder="Select an event",on_change=on_change)
    if event:
        event_data = [
            event_data for event_data in all_event_data.items if event_data["key"] == event.split(" | ")[0]]
        event_data = event_data[0]
        if not st.session_state.fetched:
            participants = participants_db.get(event_data["key"])
            st.session_state.participants = participants
        participants = st.session_state.participants
        if participants is None:
            st.error("No participants found")
            st.stop()
        people = participants['participants']
        selected_person = st.selectbox("Select your name", people, index=None, key=None)

        if selected_person:
            if not st.session_state.fetched:
                current_template = certificate_db.get(event_data["key"])
                st.session_state.data = current_template
            certificate_image = templates_db.get(f"{event_data['key']}.{event_data['extension']}")
            current_template = st.session_state.data
            st.session_state.fetched = True
            certificate_image_data = certificate_image.read()
            image_source = Image.open(io.BytesIO(certificate_image_data))
            draw = ImageDraw.Draw(image_source)
            print(current_template)
            cpx = current_template['cpx']
            cpy = current_template['cpy']
            csx = current_template['csx']
            csy = current_template['csy']
            font_size = current_template['fs']
            fc = current_template['fc']
            ha = current_template['ha']
            font_file = ImageFont.truetype('./font/GreatVibes-Regular.ttf', font_size)

            if ha == "start":
                draw.text((cpx, cpy), selected_person, font=font_file, fill=fc)
            elif ha == "center":
                draw.text((cpx + csx / 2, cpy), selected_person, font=font_file, fill=fc)
            elif ha == "end":
                draw.text((cpx + csx, cpy), selected_person, font=font_file, fill=fc)

            io_data = io.BytesIO()
            st.image(image_source, use_column_width=True)
            image_source.save(io_data, format="PNG")

            st.download_button("Download Certificate", io_data, f"{selected_person}.png", "image/png")
