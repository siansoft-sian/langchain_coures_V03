"""Build the Docker image for this project.

Usage:
    python docker/build_image.py
    python docker/build_image.py --no-cache     (rebuild everything from scratch)
"""

import argparse

from docker_helpers import DOCKER_DIR, check_docker_running, config, docker, go_to_project_root, step


def build_help_epilog() -> str:
    image = f"{config.IMAGE_NAME}:{config.TAG}"
    return f"""\
what it does:
  1. checks Docker is running
  2. builds the image {image} from docker/Dockerfile
     (files in docker/Dockerfile.dockerignore, like .env, are left out)

examples:
  python docker/build_image.py
      build the image (fast after the first time, unchanged steps are reused)

  python docker/build_image.py --no-cache
      rebuild every step, e.g. after a strange error

settings (edit in project_config.py, current values shown):
  IMAGE_NAME      {config.IMAGE_NAME!r}
  TAG             {config.TAG!r}
  PYTHON_VERSION  {config.PYTHON_VERSION!r}
  UV_VERSION      {config.UV_VERSION!r}

to run the image, see: python docker/run_container.py --help
"""


def build(no_cache: bool = False) -> None:
    """Build the image. Also used by run_container.py --build."""
    image = f"{config.IMAGE_NAME}:{config.TAG}"
    command = [
        "build",
        "--file",
        str(DOCKER_DIR / "Dockerfile"),
        "--tag",
        image,
        "--build-arg",
        f"PYTHON_VERSION={config.PYTHON_VERSION}",
        "--build-arg",
        f"UV_VERSION={config.UV_VERSION}",
    ]
    if no_cache:
        command.append("--no-cache")
    command.append(".")

    step(f"Building {image}")
    docker(*command)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build the Docker image for this project.",
        epilog=build_help_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--no-cache", action="store_true", help="rebuild every step from scratch")
    args = parser.parse_args()

    check_docker_running()
    go_to_project_root()

    build(no_cache=args.no_cache)

    print(f"✓ Image '{config.IMAGE_NAME}:{config.TAG}' is ready. Run it with: python docker/run_container.py")


if __name__ == "__main__":
    main()
