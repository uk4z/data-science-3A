import streamlit as st
from loguru import logger
from components.sidebar import render_sidebar
from components.conversation import render_conversation
import json

# Configuration du logger pour écrire dans un fichier
logger.add("application.log", rotation="500 KB", retention="10 days", level="DEBUG")

def load_css(file_name):
    with open(file_name) as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    logger.info(f"CSS chargé depuis '{file_name}'")

# Chargement du fichier base.json
try:
    with open("data/base.json", "r") as f:
        data = json.load(f)
    logger.info("Fichier 'base.json' chargé avec succès")
except Exception as e:
    logger.error("Erreur lors du chargement de 'base.json'")
    raise e

# Initialisation de la session et création de session.json si première exécution
if "is_first_load" not in st.session_state:
    try:
        with open("data/session.json", "w") as f:
            json.dump(data, f, indent=4)
        st.session_state["is_first_load"] = True
        logger.info("Session initialisée et 'session.json' créé")
    except Exception as e:
        logger.error("Erreur lors de l'écriture de 'session.json'")
        raise e

load_css("main.css")
logger.info("Affichage de la sidebar")
render_sidebar(data.keys())
logger.info("Affichage de la conversation")
render_conversation()
