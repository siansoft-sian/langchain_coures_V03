"""Small helpers shared by the ci scripts. You don't need to edit this file."""

import os
import subprocess
import sys
from pathlib import Path

# Load the shared settings file (project_config.py) from the project's main folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import project_config as config  # noqa: E402


def fail(message: str) -> None:
    """Print an error and stop the script."""
    print(f"✗ {message}", file=sys.stderr)
    sys.exit(1)


def step(message: str) -> None:
    print(f"→ {message}", flush=True)


def git(*args: str, check: bool = True, quiet: bool = False) -> subprocess.CompletedProcess:
    """Run a git command.

    quiet=False shows git's output live; quiet=True captures it instead.
    check=True stops the script if the command fails.
    """
    try:
        result = subprocess.run(["git", *args], capture_output=quiet, text=True)
    except FileNotFoundError:
        fail("git is not installed or not on your PATH.")
    if check and result.returncode != 0:
        if quiet and result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        fail(f"'git {' '.join(args)}' failed (see the message above).")
    return result


def git_ok(*args: str) -> bool:
    """Return True if the git command succeeds. Output is hidden."""
    return git(*args, check=False, quiet=True).returncode == 0


def git_output(*args: str) -> str:
    """Return the text a git command prints."""
    return git(*args, quiet=True).stdout.strip()


def go_to_repo_root() -> None:
    """Move to the top folder of the git repository, so paths work from anywhere."""
    result = git("rev-parse", "--show-toplevel", check=False, quiet=True)
    if result.returncode != 0:
        fail("This folder is not a git repository.")
    os.chdir(result.stdout.strip())


def check_remote(remote: str) -> None:
    if not git_ok("remote", "get-url", remote):
        fail(f"Remote '{remote}' not found. Check REMOTE in project_config.py.")


def local_branch_exists(branch: str) -> bool:
    return git_ok("show-ref", "--verify", "--quiet", f"refs/heads/{branch}")


def remote_branch_exists(remote: str, branch: str) -> bool:
    return git_ok("ls-remote", "--exit-code", "--heads", remote, branch)


def ask(question: str) -> str:
    """Ask the user something. Ctrl+C or Ctrl+D cancels the script."""
    try:
        return input(question).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        fail("Cancelled.")
