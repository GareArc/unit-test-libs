import json
import os
from typing import Dict, Any
from unittest.mock import mock_open, patch

import pytest
import yaml

from src.helpers.configs import load_config_files, override_with_env_vars


@pytest.fixture
def json_config_file(tmp_path):
    config = {"database": {"host": "localhost", "port": 5432}}
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(config, f)
    return str(config_file)


@pytest.fixture
def yaml_config_file(tmp_path):
    config = {"api": {"url": "http://api.example.com", "key": "secret"}}
    config_file = tmp_path / "config.yml"
    with open(config_file, "w") as f:
        yaml.dump(config, f)
    return str(config_file)


def test_load_config_files_single_json(json_config_file):
    result = load_config_files([json_config_file])
    assert result == {"database": {"host": "localhost", "port": 5432}}


def test_load_config_files_single_yaml(yaml_config_file):
    result = load_config_files([yaml_config_file])
    assert result == {"api": {"url": "http://api.example.com", "key": "secret"}}


def test_load_config_files_multiple(json_config_file, yaml_config_file):
    result = load_config_files([json_config_file, yaml_config_file])
    assert result == {
        "database": {"host": "localhost", "port": 5432},
        "api": {"url": "http://api.example.com", "key": "secret"}
    }


def test_load_config_files_override(tmp_path):
    config1 = {"database": {"host": "localhost", "port": 5432}}
    config2 = {"database": {"port": 5433, "name": "testdb"}}

    file1 = tmp_path / "config1.json"
    file2 = tmp_path / "config2.json"

    with open(file1, "w") as f:
        json.dump(config1, f)
    with open(file2, "w") as f:
        json.dump(config2, f)

    result = load_config_files([str(file1), str(file2)])
    assert result == {
        "database": {
            "host": "localhost",
            "port": 5433,
            "name": "testdb"
        }
    }


def test_load_config_files_invalid_format(tmp_path):
    invalid_file = tmp_path / "config.txt"
    invalid_file.write_text("invalid")

    with pytest.raises(ValueError) as exc:
        load_config_files([str(invalid_file)])
    assert "Unsupported config file format" in str(exc.value)


def test_load_config_files_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config_files(["nonexistent.json"])


def test_override_with_env_vars_simple(monkeypatch):
    config = {"database": {"host": "localhost", "port": 5432}}
    monkeypatch.setenv("APP_database__host", "remotehost")
    monkeypatch.setenv("IGNORED_VAR", "test")

    result = override_with_env_vars(config.copy(), prefix="APP_")
    assert result == {
        "database": {
            "host": "remotehost",
            "port": 5432
        }
    }


def test_override_with_env_vars_nested(monkeypatch):
    config = {"api": {"auth": {"token": "old"}}}
    monkeypatch.setenv("APP_api__auth__token", "new")

    result = override_with_env_vars(config.copy(), prefix="APP_")
    assert result == {
        "api": {
            "auth": {
                "token": "new"
            }
        }
    }


def test_override_with_env_vars_new_key(monkeypatch):
    config = {"existing": "value"}
    monkeypatch.setenv("APP_new__key", "newvalue")

    result = override_with_env_vars(config.copy(), prefix="APP_")
    assert result == {
        "existing": "value",
        "new": {
            "key": "newvalue"
        }
    }


def test_override_with_env_vars_no_prefix(monkeypatch):
    config = {"key": "value"}
    monkeypatch.setenv("SOME_VAR", "test")

    result = override_with_env_vars(config.copy(), prefix="APP_")
    assert result == config


def test_override_with_env_vars_empty_config(monkeypatch):
    monkeypatch.setenv("APP_new__key", "value")

    result = override_with_env_vars({}, prefix="APP_")
    assert result == {
        "new": {
            "key": "value"
        }
    }
