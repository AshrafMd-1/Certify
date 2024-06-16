import streamlit as st


def authenticated_menu():
    st.sidebar.markdown("# :rainbow[CERTIFY]")
    st.sidebar.page_link("pages/profile.py", label="Profile")
    st.sidebar.page_link("pages/create_event.py", label="Create Event")
    st.sidebar.page_link("pages/view_event.py", label="View Events")
    st.sidebar.page_link("pages/add_participants.py", label="Add Participants")
    st.sidebar.page_link("pages/add_template.py", label="Add/Customise Template")
    st.sidebar.page_link("pages/get_certificate.py", label="Get Certificate")
    st.sidebar.page_link("app.py", label="logout")


def unauthenticated_menu():
    st.sidebar.markdown("# :rainbow[CERTIFY]")
    st.sidebar.divider()
    st.sidebar.page_link("app.py", label="Log in")
    st.sidebar.page_link("pages/get_certificate.py", label="Get Certificate")


def menu():
    if "access" not in st.session_state or st.session_state.access is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    if "access" not in st.session_state or st.session_state.access is None:
        st.switch_page("app.py")
    menu()
