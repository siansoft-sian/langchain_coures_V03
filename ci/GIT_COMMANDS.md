# Common Git Commands

A quick reference for the [Git](https://git-scm.com/docs) commands you'll use most often.

For GitHub CLI (`gh`) commands, see [GH_COMMANDS.md](GH_COMMANDS.md).

## First-time setup

| Command | What it does |
|---|---|
| `git config --global user.name "Your Name"` | Set the name used on your commits |
| `git config --global user.email "you@example.com"` | Set the email used on your commits |
| `git config --global init.defaultBranch main` | Make `main` the default branch for new repos |
| `git config --list` | Show your current Git settings |

## Starting a repository

| Command | What it does |
|---|---|
| `git init` | Turn the current folder into a Git repository |
| `git clone <url>` | Download a repository from GitHub |
| `git remote -v` | Show which GitHub repo this folder is connected to |
| `git remote add origin <url>` | Connect a local repo to a GitHub repo |

## Saving changes

| Command | What it does |
|---|---|
| `git status` | See which files changed |
| `git add file.py` | Stage one file for the next commit |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Save staged changes as a commit |
| `git commit -am "message"` | Stage and commit all *tracked* files in one step |
| `git commit --amend` | Change the last commit (message or files), only before pushing |

## Viewing history and changes

| Command | What it does |
|---|---|
| `git log --oneline` | Show commit history, one line each |
| `git log --oneline --graph --all` | Show history as a branch graph |
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes |
| `git show <commit>` | Show what a specific commit changed |

## Branches

| Command | What it does |
|---|---|
| `git branch` | List local branches |
| `git branch -a` | List local and remote branches |
| `git switch -c new-branch` | Create a new branch and switch to it |
| `git switch main` | Switch to an existing branch |
| `git merge feature-branch` | Merge another branch into the current one |
| `git branch -d old-branch` | Delete a merged local branch |
| `git push origin --delete old-branch` | Delete a branch on GitHub |

> `git checkout -b new-branch` and `git checkout main` are the older equivalents of `git switch`.

## Syncing with GitHub

| Command | What it does |
|---|---|
| `git push -u origin my-branch` | Push a new branch to GitHub and track it |
| `git push` | Push new commits on the current branch |
| `git pull` | Download and merge new commits from GitHub |
| `git fetch` | Download changes without merging them |
| `git pull --rebase` | Pull and replay your commits on top (cleaner history) |

## Undoing things

| Command | What it does |
|---|---|
| `git restore file.py` | Discard unstaged changes to a file |
| `git restore --staged file.py` | Unstage a file (keep the changes) |
| `git reset --soft HEAD~1` | Undo the last commit, keep its changes staged |
| `git revert <commit>` | Create a new commit that undoes an old one (safe after pushing) |
| `git stash` | Put uncommitted changes aside temporarily |
| `git stash pop` | Bring stashed changes back |

> Be careful with `git reset --hard`: it permanently deletes uncommitted changes.

## Tags

| Command | What it does |
|---|---|
| `git tag v1.0` | Tag the current commit |
| `git push origin v1.0` | Push a tag to GitHub |

## `.gitignore`

A `.gitignore` file lists files Git should not track. For a Python/uv project, it usually includes:

```
.venv/
__pycache__/
.env
*.pyc
```

> Never commit `.env` files or API keys.

## Step-by-step recipes

Follow these in order for common tasks. Replace names like `my-branch` with your own.

### 1. Create a new branch and save it to GitHub

```bash
git switch main                       # 1. go to the main branch
git pull                              # 2. get the latest version from GitHub
git switch -c my-branch               # 3. create the new branch and move to it
# ... edit your files ...
git add .                             # 4. stage your changes
git commit -m "Describe your change"  # 5. save a snapshot
git push -u origin my-branch          # 6. upload the branch to GitHub (first time)
```

Check it worked: `git branch -a` should list `remotes/origin/my-branch`.

### 2. Save more work to a branch that's already on GitHub

```bash
git status                            # 1. see what changed
git add .                             # 2. stage your changes
git commit -m "Describe your change"  # 3. save a snapshot
git push                              # 4. upload (no -u needed after the first push)
```

### 3. Upload a brand-new project to GitHub

```bash
git init                              # 1. start tracking the folder
git add .                             # 2. stage all files
git commit -m "Initial commit"        # 3. first snapshot
git branch -M main                    # 4. name the branch main
# 5. create an empty repo on github.com (no README), then:
git remote add origin https://github.com/<user>/<repo>.git   # 6. connect to it
git push -u origin main               # 7. upload
```

Prefer the terminal? Steps 5–7 can be done with one `gh` command. See [GH_COMMANDS.md](GH_COMMANDS.md).

### 4. Open a pull request and merge the branch into main

```bash
git push                              # 1. make sure the branch is uploaded
# 2. on github.com, click "Compare & pull request", then "Create pull request"
# 3. click "Merge pull request", then "Delete branch"
git switch main                       # 4. go back to main
git pull                              # 5. download the merged result
git branch -d my-branch               # 6. delete the local branch
```

To do steps 2–3 from the terminal, see [GH_COMMANDS.md](GH_COMMANDS.md).

### 5. Merge a branch into main locally (without a pull request)

```bash
git switch main                       # 1. go to main
git pull                              # 2. get the latest main
git merge my-branch                   # 3. bring the branch's changes in
git push                              # 4. upload main to GitHub
```

If Git reports a **conflict**: open the listed files, keep the code you want (remove the `<<<<<<<`, `=======`, `>>>>>>>` markers), then run `git add .` and `git commit`.

### 6. Get the latest changes from GitHub

```bash
git switch main                       # 1. go to the branch you want to update
git pull                              # 2. download and merge new commits
```

To update your own branch with the latest main:

```bash
git switch my-branch
git merge main
```

### 7. Switch branches when you have unsaved changes

```bash
git stash                             # 1. put changes aside
git switch other-branch               # 2. switch branch
# ... do your work, then come back ...
git switch my-branch                  # 3. return
git stash pop                         # 4. bring the changes back
```

### 8. Download an existing project from GitHub

```bash
git clone https://github.com/<user>/<repo>.git   # 1. download it
cd <repo>                                         # 2. go into the folder
uv sync                                           # 3. install dependencies (uv projects)
```

### 9. Undo the last commit (before pushing)

```bash
git reset --soft HEAD~1               # 1. undo the commit, keep the changes staged
# ... fix files ...
git commit -m "Better message"        # 2. commit again
```

Already pushed? Use `git revert <commit>` and then `git push` instead. It adds a new commit that undoes the old one.

### 10. Delete a branch everywhere

```bash
git switch main                       # 1. you can't delete the branch you're on
git branch -d my-branch               # 2. delete it locally (-D to force if unmerged)
git push origin --delete my-branch    # 3. delete it on GitHub
```
