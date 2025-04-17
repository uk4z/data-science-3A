# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Run Streamlit when the container starts
# Note: The port might require adjustment. The current port is 8503.
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8503", "--server.address=0.0.0.0"]