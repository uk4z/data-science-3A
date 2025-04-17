import streamlit as st
from loguru import logger
from components.sidebar import render_sidebar
from components.conversation import render_conversation
import json
import s3fs
import os

os.environ["AWS_ACCESS_KEY_ID"] = "<TO_WRITE>"
os.environ["AWS_SECRET_ACCESS_KEY"] = "<TO_WRITE>"
os.environ["AWS_SESSION_TOKEN"] = "<TO_WRITE>"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


# Utilisation de S3 pour stocker la data.
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": "https://" + "minio.lab.sspcloud.fr"},
    key=os.environ["AWS_ACCESS_KEY_ID"],
    secret=os.environ["AWS_SECRET_ACCESS_KEY"],
    token=os.environ["AWS_SESSION_TOKEN"],
)

MY_BUCKET = "ukazmierczak"
PATH = "/base.json"

# Configuration du logger pour écrire dans un fichier
logger.add("application.log", rotation="500 KB", retention="1 day", level="DEBUG")


# Chargement du fichier css
def load_css(file_name):
    with open(file_name) as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


# Chargement du fichier base.json
def load_data():
    try:
        with fs.open(f"s3://{MY_BUCKET}/{PATH}", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return {}


def save_data(data):
    try:
        with fs.open(f"s3://{MY_BUCKET}/{PATH}", "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Data successfully written to S3")
    except Exception as e:
        logger.error(f"Error saving data: {e}")


if "is_first_load" not in st.session_state:
    logger.info("Loading...")
    st.session_state.data = load_data()
    st.session_state.is_first_load = True
elif st.session_state.data and "save_data" in st.session_state:
    if st.session_state.save_data:
        save_data(st.session_state.data)
        st.session_state.save_data = False
        logger.info(st.session_state.save_data)


load_css("main.css")
render_sidebar(st.session_state.data.keys())
render_conversation()
