"""Settings for the scripts in the ci/ and docker/ folders.

This is the only file you need to edit. To reuse the scripts in another
project, copy this file and the ci/ and docker/ folders into its main folder.
"""

# =====================================================================
# Git and GitHub (ci/ scripts)
# =====================================================================

# Name of the GitHub remote (see: git remote -v)
REMOTE = "origin"

# Main branch that new branches start from
MAIN_BRANCH = "main"

# Optional prefix added to new branch names, e.g. "feature/" -> feature/login
BRANCH_PREFIX = ""

# Commit message used when you don't pass one to save_project.py
DEFAULT_COMMIT_MESSAGE = "Update project files"

# Ask for confirmation before saving directly to the main branch
CONFIRM_ON_MAIN = True

# Also merge the latest main into your branch when saving
SYNC_WITH_MAIN = False

# Files that must never be uploaded. Saving stops if one of these would be committed.
BLOCKED_FILES = [".env", "*.pem", "*.key", "id_rsa", "credentials.json"]

# =====================================================================
# Docker (docker/ scripts)
# =====================================================================

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
