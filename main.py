import streamlit as st
from loguru import logger
from components.sidebar import render_sidebar
from components.conversation import render_conversation
from dotenv import load_dotenv
import json
import s3fs
import os

load_dotenv()

# Use S3-compatible filesystem (e.g., MinIO) for data storage
fs = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": "https://" + "minio.lab.sspcloud.fr"},
    key=os.getenv("AWS_ACCESS_KEY_ID"),
    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
    token=os.getenv("AWS_SESSION_TOKEN"),
)

MY_BUCKET = "ukazmierczak"
PATH = "/base.json"

# Configure logger to write logs to a file with rotation and retention
logger.add("application.log", rotation="500 KB", retention="1 day", level="DEBUG")


# Load CSS from a local file and inject it into the Streamlit app
def load_css(file_name):
    with open(file_name) as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


# Load conversation data from S3 bucket
def load_data():
    try:
        with fs.open(f"s3://{MY_BUCKET}/{PATH}", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return {}


# Save updated conversation data to S3 bucket
def save_data(data):
    try:
        with fs.open(f"s3://{MY_BUCKET}/{PATH}", "w") as f:
            json.dump(data, f, indent=4)
        logger.info("Data successfully written to S3")
    except Exception as e:
        logger.error(f"Error saving data: {e}")


# Check if this is the first app load to initialize session state
if "is_first_load" not in st.session_state:
    logger.info("Loading...")
    st.session_state.data = load_data()  # Load existing data from S3
    st.session_state.is_first_load = True

# If data exists and a save flag is set, write to S3
elif st.session_state.data and "save_data" in st.session_state:
    if st.session_state.save_data:
        save_data(st.session_state.data)
        st.session_state.save_data = False  # Reset the save flag
        logger.info(st.session_state.save_data)

# Load UI styling
load_css("main.css")

# Render the sidebar with list of contacts
render_sidebar(st.session_state.data.keys())

# Render the main conversation interface
render_conversation()
