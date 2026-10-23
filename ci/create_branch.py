"""Create a new branch from the latest main branch and upload it to GitHub.

Usage:
    python ci/create_branch.py my-branch
    python ci/create_branch.py            (asks for the name)
"""

import argparse

from git_helpers import (
    ask,
    check_remote,
    config,
    fail,
    git,
    git_ok,
    go_to_repo_root,
    local_branch_exists,
    remote_branch_exists,
    step,
)


def build_help_epilog() -> str:
    """Extra --help text: what the script does, examples, settings and errors."""
    m = config.MAIN_BRANCH
    prefix = config.BRANCH_PREFIX
    example = f"{prefix}my-new-feature"
    main_not_found = f'"{m}" not found'
    return f"""\
what it does:
  1. checks the name is valid and the branch doesn't exist yet
  2. switches to {m}
  3. downloads the latest {m} from {config.REMOTE}
  4. creates the new branch from it and switches to it
  5. uploads the new branch to {config.REMOTE}

examples:
  python ci/create_branch.py my-new-feature
      create and upload the branch {example}

  python ci/create_branch.py
      asks you for the branch name

  uv run python ci/create_branch.py my-new-feature
      the same, inside a uv project (on macOS use python3 if python isn't found)

settings (edit in project_config.py, current values shown):
  REMOTE         {config.REMOTE!r:<18} GitHub remote name (git remote -v)
  MAIN_BRANCH    {config.MAIN_BRANCH!r:<18} branch new branches start from
  BRANCH_PREFIX  {prefix!r:<18} added before the name, e.g. "feature/" -> feature/login

if it stops:
  "already exists"           pick another name, or switch to it: git switch <branch>
  "not a valid branch name"  avoid spaces and characters like ~ ^ : ? * [
  {main_not_found:<26} check MAIN_BRANCH in project_config.py
  pull fails                 your local {m} has commits of its own; save them on
                             a branch first, then run this script again

tip:
  Save or commit your work before creating a branch. Changes you haven't
  committed move with you to the new branch.

to save your work later, see: python ci/save_project.py --help
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a new branch from main and upload it to GitHub.",
        epilog=build_help_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
        fail(f"Branch '{config.MAIN_BRANCH}' not found. Check MAIN_BRANCH in project_config.py.")
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
