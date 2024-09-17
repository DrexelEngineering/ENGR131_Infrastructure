FROM jupyter/minimal-notebook:latest
# Replace `latest` with an image tag from to ensure reproducible builds:
# https://hub.docker.com/r/jupyter/minimal-notebook/tags/
# Inspect the Dockerfile at:
# https://github.com/jupyter/docker-stacks/tree/HEAD/minimal-notebook/Dockerfile

COPY ./requirements.txt /tmp/requirements.txt

# install additional package...
RUN pip install --no-cache-dir -r /tmp/requirements.txt
