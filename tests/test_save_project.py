"""Tests for the secret-file check in CI_Docker_DEV_GUID_COMMAND/ci/save_project.py. Run them with: uv run pytest"""

import save_project


def blocked(monkeypatch, changed_files):
    """Run find_blocked_files as if git reported these changed files."""
    monkeypatch.setattr(save_project, "git_output", lambda *args: "\0".join(changed_files))
    return save_project.find_blocked_files()


def test_env_files_are_blocked(monkeypatch):
    files = [".env", ".env.local", ".env.production", "config/.env.dev"]
    assert blocked(monkeypatch, files) == files


def test_key_files_are_blocked(monkeypatch):
    files = ["server.pem", "deploy.key", "id_rsa", "credentials.json"]
    assert blocked(monkeypatch, files) == files


def test_env_example_and_normal_files_are_allowed(monkeypatch):
    assert blocked(monkeypatch, [".env.example", "main.py", "README.md", "environment.md"]) == []
