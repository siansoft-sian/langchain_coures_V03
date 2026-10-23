"""Run the project inside a Docker container.

Usage:
    python docker/run_container.py                 (runs DEFAULT_COMMAND, e.g. python main.py)
    python docker/run_container.py --build         (build the image first)
    python docker/run_container.py bash            (open a shell inside the container)
    python docker/run_container.py python other.py (run any command)
"""

import argparse
import os
import sys

import config
from build_image import build
from docker_helpers import check_docker_running, docker, fail, go_to_project_root, image_exists, step


def build_help_epilog() -> str:
    image = f"{config.IMAGE_NAME}:{config.TAG}"
    default = " ".join(config.DEFAULT_COMMAND)
    return f"""\
what it does:
  1. checks Docker is running
  2. builds the image first (only with --build, or if it doesn't exist yet)
  3. starts a container from {image} with your {config.ENV_FILE} keys
  4. runs the command, shows its output, and removes the container when it ends

examples:
  python docker/run_container.py
      run the default command: {default}

  python docker/run_container.py --build
      rebuild the image with your latest code, then run it

  python docker/run_container.py bash
      open a shell inside the container (type exit to leave)

  python docker/run_container.py python main.py
      run any command inside the container

settings (edit in docker/config.py, current values shown):
  IMAGE_NAME       {config.IMAGE_NAME!r}
  TAG              {config.TAG!r}
  ENV_FILE         {config.ENV_FILE!r:<20} API keys passed in at start (never built into the image)
  DEFAULT_COMMAND  {config.DEFAULT_COMMAND!r}
  PORTS            {config.PORTS!r:<20} e.g. ["8000:8000"] for a web API

note:
  The container runs the code that was copied in when the image was built.
  After you change code, use --build (or run docker/build_image.py) first.
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the project inside a Docker container.",
        epilog=build_help_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--build", action="store_true", help="build the image before running")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="command to run (default: DEFAULT_COMMAND)")
    args = parser.parse_args()

    check_docker_running()
    go_to_project_root()

    image = f"{config.IMAGE_NAME}:{config.TAG}"

    if args.build or not image_exists(image):
        build()

    command = ["run", "--rm"]
    if sys.stdin.isatty():
        command.append("-it")  # lets you type into the container, e.g. for bash
    if os.path.isfile(config.ENV_FILE):
        command += ["--env-file", config.ENV_FILE]
    else:
        step(f"Note: no {config.ENV_FILE} file found, so no API keys are passed in.")
    for port in config.PORTS:
        command += ["--publish", port]
    command.append(image)
    command += args.command or config.DEFAULT_COMMAND

    step(f"Running {' '.join(args.command or config.DEFAULT_COMMAND)} in {image}")
    code = docker(*command, check=False)
    if code != 0:
        fail(f"The command inside the container stopped with exit code {code}.")


if __name__ == "__main__":
    main()
