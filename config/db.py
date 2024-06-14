import streamlit as st
from deta import Deta

deta = Deta(st.secrets["data_key"])
logins_db = deta.Base("Logins")
events_db = deta.Base("Events")
participants_db = deta.Base("Participants")
certificate_db = deta.Base("Certificate")
templates_db = deta.Drive("Templates")
