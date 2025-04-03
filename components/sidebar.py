import streamlit as st
import json
from components.conversation import load_conversation


def initialize_contacts(contacts):
    if "contacts" not in st.session_state:
        st.session_state["contacts"] = contacts


def handleContactClick(contact):
    def _click():
        with open("data/session.json", "r") as f:
            data = json.loads(f.read())
            load_conversation(data[contact])
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
