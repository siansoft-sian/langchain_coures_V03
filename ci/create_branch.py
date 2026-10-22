"""Create a new branch from the latest main branch and upload it to GitHub.

Usage:
    python ci/create_branch.py my-branch
    python ci/create_branch.py            (asks for the name)
"""

import argparse

import config
from git_helpers import (
    ask,
    check_remote,
    fail,
    git,
    git_ok,
    go_to_repo_root,
    local_branch_exists,
    remote_branch_exists,
    step,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new branch from main and upload it to GitHub.")
    parser.add_argument("name", nargs="?", help="name of the new branch")
    args = parser.parse_args()

    # --- Branch name -----------------------------------------------------
    name = args.name or ask("New branch name: ")
    if not name:
        fail("No branch name given.")
    branch = f"{config.BRANCH_PREFIX}{name}"

    # --- Checks ----------------------------------------------------------
    go_to_repo_root()

    if not git_ok("check-ref-format", "--branch", branch):
        fail(f"'{branch}' is not a valid branch name.")
    check_remote(config.REMOTE)
    if not local_branch_exists(config.MAIN_BRANCH):
        fail(f"Branch '{config.MAIN_BRANCH}' not found. Check MAIN_BRANCH in ci/config.py.")
    if local_branch_exists(branch):
        fail(f"Branch '{branch}' already exists locally. Switch to it with: git switch {branch}")
    if remote_branch_exists(config.REMOTE, branch):
        fail(f"Branch '{branch}' already exists on {config.REMOTE}.")

    # --- Create the branch -----------------------------------------------
    step(f"Switching to {config.MAIN_BRANCH}")
    git("switch", config.MAIN_BRANCH)

    if remote_branch_exists(config.REMOTE, config.MAIN_BRANCH):
        step(f"Getting the latest {config.MAIN_BRANCH} from {config.REMOTE}")
        git("pull", "--ff-only", config.REMOTE, config.MAIN_BRANCH)

    step(f"Creating branch {branch}")
    git("switch", "-c", branch)

    step(f"Uploading {branch} to {config.REMOTE}")
    git("push", "-u", config.REMOTE, branch)

    print(f"✓ Branch '{branch}' created and uploaded. You are now on it.")


if __name__ == "__main__":
    main()
