# Common uv Commands

A quick reference for the [uv](https://docs.astral.sh/uv/) commands you'll use most often in this project.

## Project setup

| Command | What it does |
|---|---|
| `uv init` | Create a new project (`pyproject.toml`, `.python-version`, etc.) |
| `uv init --package my-app` | Create a project with a `src/` package layout |
| `uv sync` | Install everything in `pyproject.toml` / `uv.lock` into `.venv` |
| `uv sync --upgrade` | Sync and upgrade all packages to the newest allowed versions |

## Managing packages

| Command | What it does |
|---|---|
| `uv add langchain` | Add a package to the project and install it |
| `uv add "langchain>=0.3"` | Add a package with a version constraint |
| `uv add --dev pytest` | Add a development-only package |
| `uv remove langchain` | Remove a package from the project |
| `uv add -r requirements.txt` | Add all packages from a requirements file |
| `uv tree` | Show the dependency tree |
| `uv pip list` | List installed packages in the environment |

## Running code

| Command | What it does |
|---|---|
| `uv run python main.py` | Run a script inside the project's environment |
| `uv run python` | Open a Python shell with project packages available |
| `uv run pytest` | Run a tool installed in the project |
| `uv run --with rich script.py` | Run with an extra package, without adding it to the project |

## Lock file

| Command | What it does |
|---|---|
| `uv lock` | Create or update `uv.lock` |
| `uv lock --upgrade` | Update the lock file to the latest allowed versions |
| `uv lock --upgrade-package langchain` | Upgrade only one package in the lock file |
| `uv export --format requirements-txt > requirements.txt` | Export dependencies to a `requirements.txt` |

## Python versions

| Command | What it does |
|---|---|
| `uv python list` | Show available and installed Python versions |
| `uv python install 3.12` | Install a Python version |
| `uv python pin 3.12` | Set the project's Python version (writes `.python-version`) |

## Virtual environments

| Command | What it does |
|---|---|
| `uv venv` | Create a `.venv` folder |
| `source .venv/bin/activate` | Activate the environment (macOS/Linux) |
| `deactivate` | Leave the environment |

> With `uv run`, you usually don't need to activate the environment.

## Global tools

| Command | What it does |
|---|---|
| `uvx ruff check` | Run a tool once without installing it |
| `uv tool install ruff` | Install a tool globally |
| `uv tool list` | List installed global tools |
| `uv tool upgrade --all` | Upgrade all global tools |

## Maintenance

| Command | What it does |
|---|---|
| `uv self update` | Update uv itself (if installed with the standalone installer) |
| `uv cache clean` | Clear uv's download cache |
| `uv --version` | Show the uv version |

## Typical workflow

```bash
uv sync                      # install everything after cloning
uv add langchain-openai      # add a new package
uv run python src/main.py    # run your code
git add pyproject.toml uv.lock && git commit -m "Add langchain-openai"
```
