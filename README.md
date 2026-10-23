# LangChain course: search agent

A search agent built with [LangChain](https://python.langchain.com/), using OpenAI models and [Tavily](https://tavily.com/) web search.

## Setup

You need [uv](https://docs.astral.sh/uv/getting-started/installation/) and git. uv installs the right Python version for you.

```bash
git clone <this repo>
cd langchain_coures_V03
python ci/setup_project.py
```

This installs the packages, turns on the checks that run before each commit, and creates `.env` from `.env.example`. Open `.env` and fill in your keys:

| Key | Where to get it |
| --- | --- |
| `OPENAI_API_KEY` | <https://platform.openai.com/api-keys> |
| `TAVILY_API_KEY` | <https://app.tavily.com/> |

On macOS, use `python3` if `python` isn't found.

## Run

```bash
uv run main.py
```

Or in Docker (open Docker Desktop first):

```bash
python docker/run_container.py --build
```

## Check the code

```bash
uv run pytest                 # run the tests
uv run ruff check . --fix     # find and fix common mistakes
uv run ruff format .          # format the code
uv run pre-commit run --all-files   # run every commit check on all files
```

GitHub runs the lint, the tests and a Docker build on every push (see the **Actions** tab).

## Project layout

| Path | What it is |
| --- | --- |
| [main.py](main.py) | The program |
| [.env.example](.env.example) | The keys the project needs (copy to `.env`) |
| [project_config.py](project_config.py) | Settings for the `ci/` and `docker/` scripts |
| [ci/](ci/README.md) | Scripts for setup, branches and saving work to GitHub |
| [docker/](docker/README.md) | Scripts to build and run the project in Docker |
| [docker-compose.yml](docker-compose.yml) | Runs the app (and later a database, etc.) with `docker compose up` |
| [tests/](tests/) | Tests, run with `uv run pytest` |
| [.github/workflows/check.yml](.github/workflows/check.yml) | Lint, tests and Docker build on GitHub after every push |
| [.pre-commit-config.yaml](.pre-commit-config.yaml) | Checks that run before every commit |
| [.vscode/](.vscode/) | VS Code settings: uses `.venv`, formats with Ruff on save |

## Everyday commands

```bash
python ci/create_branch.py my-feature     # new branch from main
python ci/save_project.py "What changed"  # commit and upload
uv add <package>                          # add a package
```

Cheat sheets for Git, GitHub CLI, uv and Docker are in [ci/Git_Gh_UV_ENV_COMMANDS/](ci/Git_Gh_UV_ENV_COMMANDS/) and [docker/DOCKER_COMMANDS.md](docker/DOCKER_COMMANDS.md).
