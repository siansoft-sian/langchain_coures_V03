"""Save all project changes on the current branch and sync with GitHub.

Steps:
    1. commit every new, changed or deleted file
    2. download other people's changes to this branch
    3. (optional) merge the latest main into this branch
    4. upload the result

Usage:
    python ci/save_project.py "Describe your change"
    python ci/save_project.py               (uses DEFAULT_COMMIT_MESSAGE)
"""

import argparse
import fnmatch
import os

import config
from git_helpers import (
    ask,
    check_remote,
    fail,
    git,
    git_ok,
    git_output,
    go_to_repo_root,
    remote_branch_exists,
    step,
)


def find_blocked_files() -> list[str]:
    """Return files that would be committed and match BLOCKED_FILES."""
    output = git_output("ls-files", "--others", "--modified", "--exclude-standard", "-z")
    changed = [path for path in output.split("\0") if path]
    return [
        path
        for path in changed
        if any(fnmatch.fnmatch(os.path.basename(path), pattern) for pattern in config.BLOCKED_FILES)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Commit all changes and sync the current branch with GitHub.")
    parser.add_argument("message", nargs="?", default=config.DEFAULT_COMMIT_MESSAGE, help="commit message")
    args = parser.parse_args()

    # --- Checks ----------------------------------------------------------
    go_to_repo_root()

    branch = git_output("branch", "--show-current")
    if not branch:
        fail("You are not on a branch. Switch to one with: git switch <branch>")
    check_remote(config.REMOTE)

    if branch == config.MAIN_BRANCH and config.CONFIRM_ON_MAIN:
        answer = ask(f"You are on '{config.MAIN_BRANCH}'. Save directly to it? [y/N] ")
        if answer.lower() != "y":
            fail("Cancelled. Create a branch with: python ci/create_branch.py <name>")

    blocked = find_blocked_files()
    if blocked:
        fail(f"'{blocked[0]}' is a blocked file. Add it to .gitignore or remove it, then try again.")

    # --- 1. Save (commit) ------------------------------------------------
    step("Staging all changes")
    git("add", "-A")

    if git_ok("diff", "--cached", "--quiet"):
        step("No new changes to commit")
    else:
        step(f"Committing: {args.message}")
        git("commit", "-m", args.message)

    # --- 2. Get other people's changes to this branch --------------------
    if remote_branch_exists(config.REMOTE, branch):
        step(f"Getting the latest {branch} from {config.REMOTE}")
        if git("pull", "--rebase", config.REMOTE, branch, check=False).returncode != 0:
            fail("Conflict while updating. Fix the files git lists, then run: git add . && git rebase --continue")

    # --- 3. Optionally bring in the latest main --------------------------
    if config.SYNC_WITH_MAIN and branch != config.MAIN_BRANCH:
        if remote_branch_exists(config.REMOTE, config.MAIN_BRANCH):
            step(f"Merging the latest {config.MAIN_BRANCH} into {branch}")
            git("fetch", config.REMOTE, config.MAIN_BRANCH)
            if git("merge", "--no-edit", f"{config.REMOTE}/{config.MAIN_BRANCH}", check=False).returncode != 0:
                fail(f"Conflict while merging {config.MAIN_BRANCH}. Fix the files git lists, then run: git add . && git commit")

    # --- 4. Upload -------------------------------------------------------
    step(f"Uploading {branch} to {config.REMOTE}")
    git("push", "-u", config.REMOTE, branch)

    print(f"✓ Project saved and '{branch}' is up to date on {config.REMOTE}.")


if __name__ == "__main__":
    main()
