import streamlit as st
from loguru import logger


# Load a given conversation into session state
def load_conversation(conversation):
    st.session_state["conversation"] = conversation


# Write a new message to the conversation data
# contact: the name of the contact
# msg: the message content
# speaker: either "user" or "contact"
def write_message(contact, msg, speaker):
    st.session_state.data[contact].append({"msg": msg, "speaker": speaker})
    st.session_state.save_data = True  # Flag to indicate that data needs saving
    st.rerun()  # Rerun the app to reflect the new message
    logger.info(st.session_state.save_data)  # Log the save_data status


# Render the current conversation in the Streamlit UI
def render_conversation():
    user_input = st.chat_input()  # Capture user input from chat input field

    if "conversation" not in st.session_state:
        load_conversation("")  # Initialize conversation if not already set

    if "active_contact" in st.session_state:
        if user_input:
            # If user typed a message, write it to the conversation
            write_message(st.session_state.active_contact, user_input, "user")

        # Display the active contact's name centered at the top
        st.markdown(
            f"<h2 style='text-align: center; width: 100%;'>{st.session_state.active_contact}</h2>",
            unsafe_allow_html=True,
        )

    # Iterate over messages in the conversation and display them
    for ingress in st.session_state.conversation:
        col1, col2 = st.columns(
            [1, 1]
        )  # Create two equal columns for left and right alignment

        if ingress["speaker"] == "contact":
            with col1:  # Display contact messages on the left
                st.markdown(
                    f"""
                    <div class="left-align">
                        <div class="message-container contact-message">
                            {ingress["msg"]}
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
        else:
            with col2:  # Display user messages on the right
                st.markdown(
                    f"""
                    <div class="right-align">
                        <div class="message-container user-message">
                            {ingress["msg"]}
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
