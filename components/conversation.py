import streamlit as st


def load_conversation(conversation):
    st.session_state["conversation"] = conversation
    print(conversation)


def render_conversation():

    user_input = st.chat_input()

    if user_input:
        st.session_state.conversation.append({"msg": user_input, "speaker": "user"})

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
