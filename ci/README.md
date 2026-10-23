# CI scripts

Reusable Python scripts for project setup and everyday Git work. They work in any project on macOS, Linux and Windows. Copy this `ci/` folder and [project_config.py](../project_config.py) into the project's main folder, then edit `project_config.py`.

They use only Python's built-in modules (Python 3.9+), so there's nothing to install.

| File | What it does |
| --- | --- |
| [setup_project.py](setup_project.py) | Sets up the project on a new computer: installs packages, turns on the commit checks and creates `.env` from `.env.example` |
| [create_branch.py](create_branch.py) | Gets the latest `main`, creates a new branch from it, and uploads the branch to GitHub |
| [save_project.py](save_project.py) | Commits all changes, downloads other people's changes to the branch, and uploads everything |
| [../project_config.py](../project_config.py) | Your settings (shared with the `docker/` scripts): the only file you need to edit |
| [git_helpers.py](git_helpers.py) | Shared helper code used by both scripts (no need to edit) |

## Settings

Open [project_config.py](../project_config.py) in the main folder and check the Git values:

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

Set up the project (first time on a computer, safe to run again):

```bash
python ci/setup_project.py
```

Create a branch:

```bash
python ci/create_branch.py my-new-feature
```

Save your work (as often as you like):

```bash
python ci/save_project.py "Add search agent"
```

Save your work and also update `main` to match your branch:

```bash
python ci/save_project.py "Add search agent" --main
```

`--main` only moves `main` forward. If `main` has commits your branch doesn't have, it stops and tells you to merge `main` into your branch first, so nothing on `main` is ever overwritten.

In a uv project you can also use `uv run python ci/save_project.py "..."`. On macOS, use `python3` if `python` isn't found.

Add `--help` to either script to see its options.

## Checks before every commit

`setup_project.py` turns on [pre-commit](https://pre-commit.com/), set up in [.pre-commit-config.yaml](../.pre-commit-config.yaml). Before each commit it runs Ruff (lint and format) and a few safety checks, such as blocking private keys and leftover conflict markers.

If a check fixes a file, the commit stops. Run `python ci/save_project.py` again and the fixes are included.

On GitHub, [.github/workflows/check.yml](../.github/workflows/check.yml) runs the same checks plus the tests and a Docker build on every push. See the results in the repository's **Actions** tab.

## What happens on a conflict

If someone else changed the same lines, the script stops and tells you what to do:

1. Open the files Git lists and keep the code you want (remove the `<<<<<<<`, `=======`, `>>>>>>>` markers).
2. Run the command the script printed (`git add . && git rebase --continue`, or `git add . && git commit` for a main merge).
3. Run `python ci/save_project.py` again to upload.

## Cheat sheets

In the [Git_Gh_UV_ENV_COMMANDS](Git_Gh_UV_ENV_COMMANDS/) folder:

- [GIT_COMMANDS.md](Git_Gh_UV_ENV_COMMANDS/GIT_COMMANDS.md): Git commands and step-by-step recipes
- [GH_COMMANDS.md](Git_Gh_UV_ENV_COMMANDS/GH_COMMANDS.md): GitHub CLI (`gh`) commands
- [UV_COMMANDS.md](Git_Gh_UV_ENV_COMMANDS/UV_COMMANDS.md): uv commands
- [ENV_COMMAND.md](Git_Gh_UV_ENV_COMMANDS/ENV_COMMAND.md): activate and deactivate the virtual environment
