import streamlit as st
import json


def load_conversation(conversation):
    st.session_state["conversation"] = conversation


def write_message(contact, msg, speaker):
    with open("data/session.json", "r") as file:
        data = json.load(file)

    data[contact].append({"msg": msg, "speaker": speaker})
    with open("data/session.json", "w") as file:
        json.dump(data, file, indent=4)


def render_conversation():
    user_input = st.chat_input()

    if "conversation" not in st.session_state:
        load_conversation("")

    if user_input and "active_contact" in st.session_state:
        st.session_state.conversation.append({"msg": user_input, "speaker": "user"})
        write_message(st.session_state.active_contact, user_input, "user")

    for ingress in st.session_state.conversation:
        col1, col2 = st.columns([1, 1])

        if ingress["speaker"] == "contact":
            with col1:
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
            with col2:
                st.markdown(
                    f"""
                    <div class="right-align">
                        <div class="message-container user-message">
                            {ingress["msg"]}
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
