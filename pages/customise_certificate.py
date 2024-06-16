import io

import streamlit as st
from PIL import Image, ImageFont, ImageDraw

from config.db import certificate_db

if st.session_state.access is None:
    st.switch_page("app.py")

st.title("Customize Certificate")
certificate_image = st.session_state.template_image
if certificate_image is None:
    st.write("No certificate template found")
else:
    name = st.selectbox("Select a random name", [
        "6C SAM",
        "10C SAMPLE",
        "16C SAMPLE IMAGE"
    ])
    image_source = Image.open(io.BytesIO(certificate_image))
    draw = ImageDraw.Draw(image_source)

    image_size = image_source.size

    fs = st.sidebar.slider("Font Size", key="fs",
                           value=150,
                           min_value=0, max_value=500)

    cpx = st.sidebar.slider("Position X", key="cpx", value=0, min_value=0, max_value=image_size[0])
    cpy = st.sidebar.slider("Position Y", key="cpy", value=0, min_value=0, max_value=image_size[1])

    font_file = ImageFont.truetype('./font/GreatVibes-Regular.ttf', fs)

    text_bbox = draw.textbbox((cpx, cpy), name, font=font_file)

    csx = st.sidebar.slider("Size X", key="csx", value=0, min_value=text_bbox[2], max_value=image_size[0])
    csy = st.sidebar.slider("Size Y", key="csy", value=0, min_value=text_bbox[3], max_value=image_size[1])

    ha = st.sidebar.selectbox("Horizontal Alignment", key="ha",
                              options=["start", "center", "end"])
    fc = st.sidebar.color_picker("Font Color", key="fc", value="#000000")

    draw.rectangle((text_bbox[0], text_bbox[1], text_bbox[2] + csx, text_bbox[3] + csy), outline="red", width=5)

    if ha == "start":
        draw.text((cpx, cpy), name, font=font_file, fill=fc)
    elif ha == "center":
        draw.text((cpx + csx / 2, cpy), name, font=font_file, fill=fc)
    elif ha == "end":
        draw.text((cpx + csx, cpy), name, font=font_file, fill=fc)

    st.image(image_source, use_column_width=True)

    col1, col2 = st.columns(2)

    with col1:
        cancel = st.button("Cancel")
        if cancel:
            st.session_state.event_key = None
            st.session_state.template_image = None
            st.switch_page("pages/add_template.py")

    with col2:
        save = st.button("Save")
        if save:
            certificate_db.update({
                "fs": fs,
                "cpx": cpx,
                "cpy": cpy,
                "csx": csx,
                "csy": csy,
                "ha": ha,
                "fc": fc,
            }, st.session_state.event_key)
            st.session_state.event_key = None
            st.session_state.template_image = None
            st.switch_page("pages/view_events.py")
