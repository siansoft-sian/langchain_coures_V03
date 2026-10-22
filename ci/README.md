# CI scripts

Two reusable Python scripts for everyday Git work. They work in any project on macOS, Linux and Windows. Copy this `ci/` folder in and edit [config.py](config.py).

They use only Python's built-in modules (Python 3.9+), so there's nothing to install.

| File | What it does |
| --- | --- |
| [create_branch.py](create_branch.py) | Gets the latest `main`, creates a new branch from it, and uploads the branch to GitHub |
| [save_project.py](save_project.py) | Commits all changes, downloads other people's changes to the branch, and uploads everything |
| [config.py](config.py) | Your settings: the only file you need to edit |
| [git_helpers.py](git_helpers.py) | Shared helper code used by both scripts (no need to edit) |

## Settings

Open `ci/config.py` and check the values:

| Setting | Meaning | Default |
| --- | --- | --- |
| `REMOTE` | GitHub remote name (`git remote -v`) | `"origin"` |
| `MAIN_BRANCH` | Branch new branches start from | `"main"` |
| `BRANCH_PREFIX` | Added before new branch names, e.g. `"feature/"` | `""` |
| `DEFAULT_COMMIT_MESSAGE` | Used when you don't give a message | `"Update project files"` |
| `CONFIRM_ON_MAIN` | Ask before saving directly to main | `True` |
| `SYNC_WITH_MAIN` | Also merge the latest main into your branch when saving | `False` |
| `BLOCKED_FILES` | Files that must never be uploaded (secrets, keys) | `.env`, `*.pem`, `*.key`, … |

## Usage

Run from anywhere inside the project.

Create a branch:

```bash
python ci/create_branch.py my-new-feature
```

Save your work (as often as you like):

```bash
python ci/save_project.py "Add search agent"
```

In a uv project you can also use `uv run python ci/save_project.py "..."`. On macOS, use `python3` if `python` isn't found.

Add `--help` to either script to see its options.

## What happens on a conflict

If someone else changed the same lines, the script stops and tells you what to do:

1. Open the files Git lists and keep the code you want (remove the `<<<<<<<`, `=======`, `>>>>>>>` markers).
2. Run the command the script printed (`git add . && git rebase --continue`, or `git add . && git commit` for a main merge).
3. Run `python ci/save_project.py` again to upload.

## Cheat sheets

In the [Git_Gh_UV_Commands](Git_Gh_UV_Commands/) folder:

- [GIT_COMMANDS.md](Git_Gh_UV_Commands/GIT_COMMANDS.md): Git commands and step-by-step recipes
- [GH_COMMANDS.md](Git_Gh_UV_Commands/GH_COMMANDS.md): GitHub CLI (`gh`) commands
- [UV_COMMANDS.md](Git_Gh_UV_Commands/UV_COMMANDS.md): uv commands
