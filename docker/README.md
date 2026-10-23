# Docker scripts

Two reusable Python scripts that build this project into a Docker image and run it in a container. They work on macOS, Linux and Windows. Copy this `docker/` folder and [project_config.py](../project_config.py) into another uv project's main folder, then edit `project_config.py`.

They use only Python's built-in modules, so there's nothing to install except [Docker Desktop](https://www.docker.com/). Open Docker Desktop before running them.

| File | What it does |
| --- | --- |
| [build_image.py](build_image.py) | Builds the image from the [Dockerfile](Dockerfile) |
| [run_container.py](run_container.py) | Runs the project (or any command) inside a container, with your `.env` keys |
| [../project_config.py](../project_config.py) | Your settings (shared with the `ci/` scripts): the only file you need to edit |
| [docker_helpers.py](docker_helpers.py) | Shared helper code used by both scripts (no need to edit) |
| [Dockerfile](Dockerfile) | Recipe for the image: Python + uv + your packages + your code |
| [Dockerfile.dockerignore](Dockerfile.dockerignore) | Files kept out of the image (`.env`, `.venv`, `.git`, …) |
| [DOCKER_COMMANDS.md](DOCKER_COMMANDS.md) | Cheat sheet of everyday Docker commands |

## Settings

Open [project_config.py](../project_config.py) in the main folder and check the Docker values:

| Setting | Meaning | Default |
| --- | --- | --- |
| `IMAGE_NAME` | Name of the image | `"langchain-coures-v03"` |
| `TAG` | Version label of the image | `"latest"` |
| `PYTHON_VERSION` | Python version inside the image | `"3.13"` |
| `UV_VERSION` | uv version inside the image | `"0.12.24"` |
| `ENV_FILE` | File with your API keys, passed in when the container starts | `".env"` |
| `DEFAULT_COMMAND` | What the container runs when you don't give a command | `["python", "main.py"]` |
| `PORTS` | Ports to open, e.g. `["8000:8000"]` for a web API | `[]` |

## Usage

Run from anywhere inside the project.

Build the image:

```bash
python docker/build_image.py
```

Run the project in a container:

```bash
python docker/run_container.py
```

Rebuild with your latest code, then run:

```bash
python docker/run_container.py --build
```

Open a shell inside the container (type `exit` to leave):

```bash
python docker/run_container.py bash
```

On macOS, use `python3` if `python` isn't found. Add `--help` to either script to see its options.

## Docker Compose

For more than one container (for example the app plus a database), use [docker-compose.yml](../docker-compose.yml) in the main folder:

```bash
docker compose up --build
```

It has a commented-out Postgres example to start from. Commands are in [DOCKER_COMMANDS.md](DOCKER_COMMANDS.md#docker-compose).

## Good to know

- **Your code is copied in at build time.** After changing code, run with `--build` so the container gets the new version.
- **Your `.env` is never put in the image.** It's passed in only when the container starts, so the image is safe to share.
- **Packages come from `uv.lock`.** After `uv add <package>`, rebuild the image.
- The first build downloads Python and your packages, so it's slow. Later builds reuse those steps and are fast.
