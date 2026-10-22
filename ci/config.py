"""Settings for the scripts in this folder.

Copy the ci/ folder into any project and edit only this file.
"""

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
