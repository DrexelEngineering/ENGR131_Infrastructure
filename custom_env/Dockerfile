FROM jupyter/minimal-notebook:latest

# Switch to root user to install system packages
USER root

# Update and install packages
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Switch back to non-root `jovyan` user
USER $NB_USER

# Copy and install Python dependencies
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
