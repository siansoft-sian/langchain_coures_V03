"""Starting point of the program. Run it with: uv run search-agent"""

from search_agent.config import check_env


def main() -> None:
    check_env()
    print("hello world!")


if __name__ == "__main__":
    main()
