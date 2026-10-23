# Virtual Environment Commands

A quick reference for activating and deactivating the project's `.venv` (macOS / Linux, zsh or bash).

## Activate and deactivate

| Command | What it does |
| --- | --- |
| `source .venv/bin/activate` | Activate the project's virtual environment |
| `deactivate` | Turn off the active virtual environment |

## Tips

- Run `source .venv/bin/activate` from the project root folder.
- When it's active, your prompt starts with `(langchain-coures-v03)` or `(.venv)`.
- You don't need to activate it when you use `uv run`. For example, `uv run search-agent` always uses `.venv`.
- In VS Code, pick `./.venv/bin/python` with **Python: Select Interpreter**, and new terminals activate it automatically.
