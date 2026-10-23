"""Tests for src/search_agent/config.py. Run them with: uv run pytest"""

import pytest

from search_agent import config


def test_check_env_passes_when_all_keys_are_set(monkeypatch):
    for key in config.REQUIRED_KEYS:
        monkeypatch.setenv(key, "test-value")

    config.check_env()  # should not stop the program


def test_check_env_stops_and_names_the_missing_key(monkeypatch):
    for key in config.REQUIRED_KEYS:
        monkeypatch.setenv(key, "test-value")
    monkeypatch.delenv("OPENAI_API_KEY")

    with pytest.raises(SystemExit) as error:
        config.check_env()

    assert "OPENAI_API_KEY" in str(error.value)
    assert "TAVILY_API_KEY" not in str(error.value)


def test_required_keys_match_env_example():
    """REQUIRED_KEYS in config.py and .env.example must list the same keys."""
    from setup_project import read_env_keys

    assert set(read_env_keys(".env.example")) == set(config.REQUIRED_KEYS)
