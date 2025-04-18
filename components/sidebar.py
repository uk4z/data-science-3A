import streamlit as st
from components.conversation import load_conversation


# Initialize the contact list in session state if it doesn't exist
def initialize_contacts(contacts):
    if "contacts" not in st.session_state:
        st.session_state["contacts"] = contacts


# Return a click handler function that sets the active contact and loads the conversation
def handleContactClick(contact):
    def _click():
        load_conversation(
            st.session_state.data[contact]
        )  # Load the conversation data for the selected contact
        st.session_state["active_contact"] = (
            contact  # Set the active contact in session state
        )

    return _click


# Render the contact list in the sidebar
def render_sidebar(contacts):
    st.sidebar.title("Contacts")  # Set the title of the sidebar

    initialize_contacts(contacts)  # Ensure the contacts list is initialized

    with st.sidebar.container(border=True):
        # Create a button for each contact in the list
        for contact in st.session_state.contacts:
            if st.sidebar.button(
                contact, on_click=handleContactClick(contact), key=f"btn_{contact}"
            ):
                st.session_state.selected_contact = (
                    contact  # Optionally store the selected contact
                )
