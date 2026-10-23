"""Set up the project on a new computer (or check an existing setup).

Steps:
    1. check that uv is installed
    2. install the Python version and packages (uv sync)
    3. turn on the checks that run before every commit (pre-commit)
    4. create .env from .env.example, if .env doesn't exist yet
    5. list any keys in .env that are still empty

Safe to run again at any time: it never overwrites your .env.

Usage:
    python CI_Docker_DEV_GUID_COMMAND/ci/setup_project.py
"""

import argparse
import os
import shutil
import subprocess

from git_helpers import fail, go_to_repo_root, step

ENV_FILE = ".env"
ENV_EXAMPLE = ".env.example"
PRE_COMMIT_CONFIG = ".pre-commit-config.yaml"


def read_env_keys(path: str) -> dict[str, str]:
    """Return KEY -> value for every KEY=value line in an env file."""
    keys = {}
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            keys[key.strip()] = value.strip().strip("\"'")
    return keys


def build_help_epilog() -> str:
    return f"""\
what it does:
  1. checks that uv is installed
  2. installs the Python version and packages from uv.lock (uv sync)
  3. turns on the checks that run before every commit (pre-commit)
  4. creates {ENV_FILE} from {ENV_EXAMPLE}, if {ENV_FILE} doesn't exist yet
  5. lists any keys in {ENV_FILE} that are still empty

It never overwrites your {ENV_FILE}, so it's safe to run again at any time.

examples:
  python CI_Docker_DEV_GUID_COMMAND/ci/setup_project.py
      set up the project (on macOS use python3 if python isn't found)

after it finishes:
  1. open {ENV_FILE} and fill in any empty keys
  2. run the project: uv run src/main.py
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set up the project: install packages and create .env.",
        epilog=build_help_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.parse_args()

    go_to_repo_root()

    # --- 1. Check uv -----------------------------------------------------
    step("Checking that uv is installed")
    if not shutil.which("uv"):
        fail("uv is not installed. Install it from https://docs.astral.sh/uv/getting-started/installation/")

    # --- 2. Install Python and packages ----------------------------------
    step("Installing Python and packages (uv sync)")
    if subprocess.run(["uv", "sync"]).returncode != 0:
        fail("'uv sync' failed (see the message above).")

    # --- 3. Turn on the commit checks -----------------------------------
    if os.path.isfile(PRE_COMMIT_CONFIG):
        step("Turning on the checks that run before every commit (pre-commit)")
        if subprocess.run(["uv", "run", "pre-commit", "install"]).returncode != 0:
            fail("'pre-commit install' failed (see the message above).")

    # --- 4. Create .env --------------------------------------------------
    try:
        example_keys = read_env_keys(ENV_EXAMPLE)
    except FileNotFoundError:
        fail(f"{ENV_EXAMPLE} not found. It lists the keys the project needs.")

    try:
        env_keys = read_env_keys(ENV_FILE)
        step(f"{ENV_FILE} already exists, leaving it as it is")
    except FileNotFoundError:
        step(f"Creating {ENV_FILE} from {ENV_EXAMPLE}")
        shutil.copyfile(ENV_EXAMPLE, ENV_FILE)
        env_keys = read_env_keys(ENV_FILE)

    # --- 5. Check for empty keys -----------------------------------------
    missing = [key for key in example_keys if not env_keys.get(key)]
    if missing:
        print(f"✓ Setup done, but these keys in {ENV_FILE} are still empty:")
        for key in missing:
            print(f"    {key}")
        print(f"  Open {ENV_FILE}, fill them in, then run: uv run src/main.py")
    else:
        print("✓ Setup done. Run the project with: uv run src/main.py")


if __name__ == "__main__":
    main()
