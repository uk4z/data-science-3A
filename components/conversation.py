import streamlit as st
from loguru import logger


def load_conversation(conversation):
    st.session_state["conversation"] = conversation


def write_message(contact, msg, speaker):
    st.session_state.data[contact].append({"msg": msg, "speaker": speaker})
    st.session_state.save_data = True
    st.rerun()
    logger.info(st.session_state.save_data)


def render_conversation():
    user_input = st.chat_input()

    if "conversation" not in st.session_state:
        load_conversation("")

    if "active_contact" in st.session_state:
        if user_input:
            write_message(st.session_state.active_contact, user_input, "user")
        
        st.markdown(
            f"<h2 style='text-align: center; width: 100%;'>{st.session_state.active_contact}</h2>", 
            unsafe_allow_html=True
        )

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
