import os
import sys

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Keys the project needs. Keep this list in step with .env.example.
REQUIRED_KEYS = ["OPENAI_API_KEY", "TAVILY_API_KEY"]


def check_env() -> None:
    """Stop with a clear message if a required key is missing."""
    missing = [key for key in REQUIRED_KEYS if not os.getenv(key)]
    if missing:
        sys.exit(
            f"✗ Missing keys: {', '.join(missing)}\n"
            "  Add them to .env (see .env.example), or run: python CI_Docker_DEV_GUID_COMMAND/ci/setup_project.py"
        )


def main() -> None:
    check_env()
    print("hello world!")


if __name__ == "__main__":
    main()
