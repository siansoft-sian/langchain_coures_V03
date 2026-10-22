# Common GitHub CLI (`gh`) Commands

A quick reference for the [GitHub CLI](https://cli.github.com/manual/). `gh` lets you work with GitHub (repos, pull requests, issues) from the terminal instead of the website.

For plain Git commands, see [GIT_COMMANDS.md](GIT_COMMANDS.md).

## Install and log in

| Command | What it does |
|---|---|
| `brew install gh` | Install on macOS |
| `gh auth login` | Log in to GitHub (run once) |
| `gh auth status` | Check that you're logged in |
| `gh auth logout` | Log out |

## Repositories

| Command | What it does |
|---|---|
| `gh repo create` | Create a new GitHub repository (asks questions) |
| `gh repo create my-project --private --source=. --push` | Create a repo from the current folder and upload it |
| `gh repo clone owner/repo` | Download a repository |
| `gh repo view` | Show info about the current repo |
| `gh repo view --web` | Open the current repo in your browser |
| `gh repo list` | List your repositories |
| `gh repo fork owner/repo --clone` | Fork someone's repo and download your copy |

## Pull requests

| Command | What it does |
|---|---|
| `gh pr create` | Open a pull request for the current branch (asks questions) |
| `gh pr create --fill` | Open a pull request using your commit messages as the title and description |
| `gh pr list` | List open pull requests |
| `gh pr status` | Show pull requests related to you |
| `gh pr view 12` | Show pull request #12 |
| `gh pr view --web` | Open the current branch's pull request in the browser |
| `gh pr checkout 12` | Download pull request #12 and switch to its branch |
| `gh pr diff 12` | Show the changes in pull request #12 |
| `gh pr checks` | Show the status of automated checks |
| `gh pr review 12 --approve` | Approve pull request #12 |
| `gh pr merge 12` | Merge pull request #12 |
| `gh pr merge --merge --delete-branch` | Merge the current branch's pull request and delete the branch |
| `gh pr close 12` | Close pull request #12 without merging |

## Issues

| Command | What it does |
|---|---|
| `gh issue create` | Create an issue |
| `gh issue list` | List open issues |
| `gh issue view 5` | Show issue #5 |
| `gh issue close 5` | Close issue #5 |

## Other useful commands

| Command | What it does |
|---|---|
| `gh browse` | Open the current repo in your browser |
| `gh release create v1.0` | Create a release on GitHub |
| `gh run list` | List recent GitHub Actions runs |
| `gh run watch` | Watch a GitHub Actions run live |
| `gh gist create file.py` | Share a file as a gist |

## Step-by-step recipes

### 1. Upload a brand-new project to GitHub

```bash
git init                              # 1. start tracking the folder
git add .                             # 2. stage all files
git commit -m "Initial commit"        # 3. first snapshot
git branch -M main                    # 4. name the branch main
gh repo create my-project --private --source=. --push   # 5. create the GitHub repo and upload
```

Use `--public` instead of `--private` to make it public.

### 2. Create a branch, open a pull request and merge it

```bash
git switch main && git pull           # 1. start from the latest main
git switch -c my-branch               # 2. create a branch
# ... edit your files ...
git add .                             # 3. stage changes
git commit -m "Describe your change"  # 4. save a snapshot
git push -u origin my-branch          # 5. upload the branch
gh pr create --fill                   # 6. open a pull request
gh pr merge --merge --delete-branch   # 7. merge it and delete the branch on GitHub
git switch main && git pull           # 8. update your local main
git branch -d my-branch               # 9. delete the local branch
```

### 3. Review someone else's pull request

```bash
gh pr list                            # 1. find the pull request number
gh pr checkout 12                     # 2. download it and switch to its branch
# ... test the code ...
gh pr review 12 --approve             # 3. approve it (or --request-changes -b "comment")
git switch main                       # 4. go back to main
```

### 4. Download an existing project

```bash
gh repo clone owner/repo              # 1. download it
cd repo                               # 2. go into the folder
uv sync                               # 3. install dependencies (uv projects)
```
