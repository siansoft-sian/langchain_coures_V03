"""Settings for the scripts in CI_Docker_DEV_GUID_COMMAND/ci/ and CI_Docker_DEV_GUID_COMMAND/docker/.

This is the only file you need to edit. To reuse the scripts in another
project, copy this file and the CI_Docker_DEV_GUID_COMMAND/ folder into its main folder.
"""

# =====================================================================
# Git and GitHub (CI_Docker_DEV_GUID_COMMAND/ci/ scripts)
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
BLOCKED_FILES = [".env", ".env.*", "*.pem", "*.key", "id_rsa", "credentials.json"]

# Files that match BLOCKED_FILES but are safe to upload (they hold no real keys)
ALLOWED_FILES = [".env.example"]

# =====================================================================
# Docker (CI_Docker_DEV_GUID_COMMAND/docker/ scripts)
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
DEFAULT_COMMAND = ["search-agent"]

# Ports to open, as "computer:container", e.g. ["8000:8000"] for a web API. Empty = none.
PORTS = []
