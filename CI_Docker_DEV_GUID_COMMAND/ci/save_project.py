"""Save all project changes on the current branch and sync with GitHub.

Steps:
    1. commit every new, changed or deleted file
    2. download other people's changes to this branch
    3. (optional) merge the latest main into this branch
    4. upload the result
    5. (with --main) also update main to match this branch

Usage:
    python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py "Describe your change"
    python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py               (uses DEFAULT_COMMIT_MESSAGE)
    python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py "Describe your change" --main
"""

import argparse
import fnmatch
import os

from git_helpers import (
    ask,
    check_remote,
    config,
    fail,
    git,
    git_ok,
    git_output,
    go_to_repo_root,
    local_branch_exists,
    remote_branch_exists,
    step,
)


def find_blocked_files() -> list[str]:
    """Return files that would be committed and match BLOCKED_FILES."""
    output = git_output("ls-files", "--others", "--modified", "--exclude-standard", "-z")
    changed = [path for path in output.split("\0") if path]
    allowed = getattr(config, "ALLOWED_FILES", [])
    return [
        path
        for path in changed
        if os.path.basename(path) not in allowed
        and any(fnmatch.fnmatch(os.path.basename(path), pattern) for pattern in config.BLOCKED_FILES)
    ]


def update_main(branch: str) -> None:
    """Move main forward to this branch, on GitHub and locally. Never merges."""
    main_branch = config.MAIN_BRANCH
    remote_main = f"{config.REMOTE}/{main_branch}"

    step(f"Updating {main_branch} to match {branch}")
    if remote_branch_exists(config.REMOTE, main_branch):
        git("fetch", config.REMOTE, main_branch)
        if not git_ok("merge-base", "--is-ancestor", remote_main, "HEAD"):
            fail(
                f"'{main_branch}' has changes that '{branch}' doesn't have, so it can't be updated cleanly.\n"
                f"  Bring them in first with: git merge {remote_main}\n"
                f"  (or set SYNC_WITH_MAIN = True in project_config.py),\n"
                f"  then run this script again with --main."
            )

    git("push", config.REMOTE, f"HEAD:refs/heads/{main_branch}")

    # Keep the local main in step too, if there is one.
    if local_branch_exists(main_branch) and not git_ok("fetch", config.REMOTE, f"{main_branch}:{main_branch}"):
        step(f"Note: your local '{main_branch}' has commits of its own, so it was left as it is.")

    print(f"✓ '{main_branch}' now matches '{branch}' on {config.REMOTE}.")


def build_help_epilog() -> str:
    """Extra --help text: what the script does, examples, settings and conflicts."""
    m = config.MAIN_BRANCH
    blocked = ", ".join(config.BLOCKED_FILES)
    return f"""\
what it does:
  1. commits every new, changed or deleted file
  2. downloads other people's changes to this branch
  3. merges the latest {m} into this branch (only if SYNC_WITH_MAIN = True)
  4. uploads the branch to {config.REMOTE}
  5. updates {m} to match this branch (only with --main)

examples:
  python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py "Add search agent"
      save your work on the current branch (as often as you like)

  python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py "Add search agent" --main
      save your work and also update {m} to match your branch

  python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py
      save with the default message: "{config.DEFAULT_COMMIT_MESSAGE}"

  uv run python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py "..."
      the same, inside a uv project (on macOS use python3 if python isn't found)

about --main:
  --main only moves {m} forward. If {m} has commits your branch doesn't
  have, the script stops and tells you to merge {m} into your branch first,
  so nothing on {m} is ever overwritten.

settings (edit in project_config.py, current values shown):
  REMOTE                  {config.REMOTE!r:<24} GitHub remote name (git remote -v)
  MAIN_BRANCH             {config.MAIN_BRANCH!r:<24} branch new branches start from
  DEFAULT_COMMIT_MESSAGE  used when you don't give a message
  CONFIRM_ON_MAIN         {config.CONFIRM_ON_MAIN!r:<24} ask before saving directly to {m}
  SYNC_WITH_MAIN          {config.SYNC_WITH_MAIN!r:<24} also merge the latest {m} into your branch
  BLOCKED_FILES           files that must never be uploaded:
                          {blocked}

if there is a conflict:
  The script stops when someone else changed the same lines. Then:
  1. open the files git lists and keep the code you want
     (remove the <<<<<<<, =======, >>>>>>> markers)
  2. run the command the script printed:
       git add . && git rebase --continue    (conflict on this branch)
       git add . && git commit               (conflict while merging {m})
  3. run python CI_Docker_DEV_GUID_COMMAND/ci/save_project.py again to upload

to create a new branch, see: python CI_Docker_DEV_GUID_COMMAND/ci/create_branch.py --help
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Commit all changes and sync the current branch with GitHub.",
        epilog=build_help_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("message", nargs="?", default=config.DEFAULT_COMMIT_MESSAGE, help="commit message")
    parser.add_argument(
        "--main",
        action="store_true",
        help=f"also update {config.MAIN_BRANCH} to match this branch (only if no merge is needed)",
    )
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
            fail("Cancelled. Create a branch with: python CI_Docker_DEV_GUID_COMMAND/ci/create_branch.py <name>")

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
                fail(
                    f"Conflict while merging {config.MAIN_BRANCH}. "
                    "Fix the files git lists, then run: git add . && git commit"
                )

    # --- 4. Upload -------------------------------------------------------
    step(f"Uploading {branch} to {config.REMOTE}")
    git("push", "-u", config.REMOTE, branch)

    # --- 5. Optionally update main to match this branch ------------------
    if args.main and branch != config.MAIN_BRANCH:
        update_main(branch)

    print(f"✓ Project saved and '{branch}' is up to date on {config.REMOTE}.")


if __name__ == "__main__":
    main()
