import streamlit as st
from components.sidebar import render_sidebar
from components.conversation import render_conversation
import json


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


with open("data.json", "r") as f:
    data = json.loads(f.read())

    load_css("main.css")
    render_sidebar(data.keys())
    render_conversation()
