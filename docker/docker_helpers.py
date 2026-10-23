"""Small helpers shared by the docker scripts. You don't need to edit this file."""

import os
import subprocess
import sys
from pathlib import Path

DOCKER_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DOCKER_DIR.parent

# Load the shared settings file (project_config.py) from the project's main folder.
sys.path.insert(0, str(PROJECT_ROOT))
import project_config as config  # noqa: E402, F401 (used by the scripts)


def fail(message: str) -> None:
    """Print an error and stop the script."""
    print(f"✗ {message}", file=sys.stderr)
    sys.exit(1)


def step(message: str) -> None:
    print(f"→ {message}", flush=True)


def docker(*args: str, check: bool = True) -> int:
    """Run a docker command and show its output live. Returns the exit code."""
    try:
        code = subprocess.run(["docker", *args]).returncode
    except FileNotFoundError:
        fail("Docker is not installed. Get Docker Desktop from https://www.docker.com/")
    if check and code != 0:
        fail(f"'docker {' '.join(args)}' failed (see the message above).")
    return code


def check_docker_running() -> None:
    """Stop with a clear message if Docker isn't installed or isn't started."""
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
    except FileNotFoundError:
        fail("Docker is not installed. Get Docker Desktop from https://www.docker.com/")
    if result.returncode != 0:
        fail("Docker is not running. Open Docker Desktop, wait until it says 'running', then try again.")


def image_exists(image: str) -> bool:
    result = subprocess.run(["docker", "image", "inspect", image], capture_output=True)
    return result.returncode == 0


def go_to_project_root() -> None:
    """Move to the project folder, so paths work from anywhere."""
    os.chdir(PROJECT_ROOT)
