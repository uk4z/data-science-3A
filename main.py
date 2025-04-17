import streamlit as st
from loguru import logger
from components.sidebar import render_sidebar
from components.conversation import render_conversation
import json
import s3fs
import os

os.environ["AWS_ACCESS_KEY_ID"] = "KWIT4KKCQMIH05NA16P4"
os.environ["AWS_SECRET_ACCESS_KEY"] = "n5MKQ49CtFo5QD6njFcPrbRHGosAV+e3gmYtvfqx"
os.environ["AWS_SESSION_TOKEN"] = (
    "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJLV0lUNEtLQ1FNSUgwNU5BMTZQNCIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sImF1ZCI6WyJtaW5pby1kYXRhbm9kZSIsIm9ueXhpYSIsImFjY291bnQiXSwiYXV0aF90aW1lIjoxNzQ0ODYyMzYxLCJhenAiOiJvbnl4aWEiLCJlbWFpbCI6InVseXNzZS5rYXptaWVyY3pha0BlbnNhZS5mciIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJleHAiOjE3NDU0NjcyMTAsImZhbWlseV9uYW1lIjoiS2F6bWllcmN6YWsiLCJnaXZlbl9uYW1lIjoiVWx5c3NlIiwiZ3JvdXBzIjpbIlVTRVJfT05ZWElBIl0sImlhdCI6MTc0NDg2MjQxMCwiaXNzIjoiaHR0cHM6Ly9hdXRoLmxhYi5zc3BjbG91ZC5mci9hdXRoL3JlYWxtcy9zc3BjbG91ZCIsImp0aSI6ImEzOTM2ZmRkLTE3Y2YtNDMzOC04M2E5LWE4N2VlZTgzMzhkMyIsIm5hbWUiOiJVbHlzc2UgS2F6bWllcmN6YWsiLCJwb2xpY3kiOiJzdHNvbmx5IiwicHJlZmVycmVkX3VzZXJuYW1lIjoidWthem1pZXJjemFrIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLXNzcGNsb3VkIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtc3NwY2xvdWQiXSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBncm91cHMgZW1haWwiLCJzaWQiOiI5ZDhiMjc2Ni04NWI1LTQ1NmUtODlhYS0zZGFhODBjMzMxYTYiLCJzdWIiOiIwZTYyMmExOS1hNGE4LTQ5NTQtYTYyMi1iODg5MmU1OGFhNDEiLCJ0eXAiOiJCZWFyZXIifQ.sHaOzqx7QVqoywanQ29wfrOpUMxeAray7UiQJRkZ003FcJ-XEV9X4Xj7DLkD2wtugUg2QUv9FmbwdIAamIc27A"
)
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
