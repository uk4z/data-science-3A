import streamlit as st
from components.sidebar import render_sidebar
from components.conversation import render_conversation
import json


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


with open("data/base.json", "r") as f:
    data = json.load(f)

if "is_first_load" not in st.session_state:
    with open("data/session.json", "w") as f:
        json.dump(data, f, indent=4)

    st.session_state["is_first_load"] = True

load_css("main.css")
render_sidebar(data.keys())
render_conversation()
