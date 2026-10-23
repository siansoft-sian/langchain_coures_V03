"""Tests for CI_Docker_DEV_GUID_COMMAND/ci/setup_project.py. Run them with: uv run pytest"""

from setup_project import read_env_keys


def test_read_env_keys_reads_values_and_skips_comments(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text('# a comment\n\nOPENAI_API_KEY=abc123\nTAVILY_API_KEY=\nQUOTED="hello"\nWITH_EQUALS=a=b\n')

    assert read_env_keys(str(env_file)) == {
        "OPENAI_API_KEY": "abc123",
        "TAVILY_API_KEY": "",
        "QUOTED": "hello",
        "WITH_EQUALS": "a=b",
    }
