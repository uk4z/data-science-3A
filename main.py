import streamlit as st
from loguru import logger
from components.sidebar import render_sidebar
from components.conversation import render_conversation
import json
import s3fs


# Utilisation de S3 pour stocker la data.
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
MY_BUCKET = "ukazmierczak"
PATH = "base.json"

# Configuration du logger pour écrire dans un fichier
logger.add("application.log", rotation="500 KB", retention="10 days", level="DEBUG")


def load_css(file_name):
    with open(file_name) as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    logger.info(f"CSS chargé depuis '{file_name}'")


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


st.session_state.data = load_data()

if "is_first_load" not in st.session_state:
    st.session_state.is_first_load = True
elif st.session_state.data:
    logger.info("Condition met")
    save_data(st.session_state.data)


load_css("main.css")
logger.info("Affichage de la sidebar")
render_sidebar(st.session_state.data.keys())
logger.info("Affichage de la conversation")
render_conversation()
