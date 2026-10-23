"""Settings for the scripts in this folder.

Copy the docker/ folder into any project and edit only this file.
"""

# Name of the image (lowercase letters, numbers, - and _ only)
IMAGE_NAME = "langchain-coures-v03"

# Tag (version label) of the image
TAG = "latest"

# Python and uv versions used inside the image
PYTHON_VERSION = "3.13"
UV_VERSION = "0.12.24"

# File with your API keys. Passed to the container when it starts, never built into the image.
ENV_FILE = ".env"

# Command the container runs when you don't give one
DEFAULT_COMMAND = ["python", "main.py"]

# Ports to open, as "computer:container", e.g. ["8000:8000"] for a web API. Empty = none.
PORTS = []
