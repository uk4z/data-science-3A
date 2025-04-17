import streamlit as st
from components.conversation import load_conversation


def initialize_contacts(contacts):
    if "contacts" not in st.session_state:
        st.session_state["contacts"] = contacts


def handleContactClick(contact):
    def _click():
        load_conversation(st.session_state.data[contact])
        st.session_state["active_contact"] = contact

    return _click


def render_sidebar(contacts):
    st.sidebar.title("Contacts")

    initialize_contacts(contacts)

    with st.sidebar.container(border=True):
        for contact in st.session_state.contacts:
            if st.sidebar.button(
                contact, on_click=handleContactClick(contact), key=f"btn_{contact}"
            ):
                st.session_state.selected_contact = contact
