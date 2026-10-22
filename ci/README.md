# CI scripts

Two reusable scripts for everyday Git work. They work in any project. Copy this `ci/` folder in and edit [config.sh](config.sh).

| Script | What it does |
|---|---|
| [create_branch.sh](create_branch.sh) | Gets the latest `main`, creates a new branch from it, and uploads the branch to GitHub |
| [save_project.sh](save_project.sh) | Commits all changes, downloads other people's changes to the branch, and uploads everything |

## First-time setup

Run once per project, from the project folder:

```bash
chmod +x ci/*.sh
```

Then open `ci/config.sh` and check the settings:

| Setting | Meaning | Default |
|---|---|---|
| `REMOTE` | GitHub remote name (`git remote -v`) | `origin` |
| `MAIN_BRANCH` | Branch new branches start from | `main` |
| `BRANCH_PREFIX` | Added before new branch names, e.g. `feature/` | empty |
| `DEFAULT_COMMIT_MESSAGE` | Used when you don't give a message | `Update project files` |
| `CONFIRM_ON_MAIN` | Ask before saving directly to main | `yes` |
| `SYNC_WITH_MAIN` | Also merge the latest main into your branch when saving | `no` |
| `BLOCKED_FILES` | Files that must never be uploaded (secrets, keys) | `.env`, `*.pem`, `*.key`, … |

## Usage

Create a branch:

```bash
./ci/create_branch.sh my-new-feature
```

Save your work (as often as you like):

```bash
./ci/save_project.sh "Add search agent"
```

## What happens on a conflict

If someone else changed the same lines, the script stops and tells you what to do:

1. Open the files Git lists and keep the code you want (remove the `<<<<<<<`, `=======`, `>>>>>>>` markers).
2. Run the command the script printed (`git add . && git rebase --continue`, or `git add . && git commit` for a main merge).
3. Run `./ci/save_project.sh` again to upload.
