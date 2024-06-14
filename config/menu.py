import streamlit as st


def authenticated_menu():
    st.sidebar.markdown("# :rainbow[CERTIFY]")
    st.sidebar.page_link("pages/profile.py", label="Profile")
    st.sidebar.page_link("app.py", label="logout")


def unauthenticated_menu():
    st.sidebar.markdown("# :rainbow[CERTIFY]")
    st.sidebar.divider()
    st.sidebar.page_link("app.py", label="Log in")


def menu():
    if "access" not in st.session_state or st.session_state.access is None:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    if "access" not in st.session_state or st.session_state.access is None:
        st.switch_page("app.py")
    menu()
