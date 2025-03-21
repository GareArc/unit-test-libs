import json
import os
from unittest.mock import mock_open, patch

import pytest
import yaml

from src.helpers.configs import load_config_files, override_with_env_vars


@pytest.fixture
def json_config(tmp_path):
    config = {
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "app": {
            "name": "test-app"
        }
    }
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump(config, f)
    return str(config_file)


@pytest.fixture
def yaml_config(tmp_path):
    config = {
        "database": {
            "password": "secret",
            "name": "testdb"
        },
        "app": {
            "port": 8080
        }
    }
    config_file = tmp_path / "config.yml"
    with open(config_file, "w") as f:
        yaml.dump(config, f)
    return str(config_file)


def test_load_config_files_single_json(json_config):
    result = load_config_files([json_config])
    assert result["database"]["host"] == "localhost"
    assert result["database"]["port"] == 5432
    assert result["app"]["name"] == "test-app"


def test_load_config_files_single_yaml(yaml_config):
    result = load_config_files([yaml_config])
    assert result["database"]["password"] == "secret"
    assert result["database"]["name"] == "testdb"
    assert result["app"]["port"] == 8080


def test_load_config_files_multiple(json_config, yaml_config):
    result = load_config_files([json_config, yaml_config])
    assert result["database"]["host"] == "localhost"
    assert result["database"]["port"] == 5432
    assert result["database"]["password"] == "secret"
    assert result["database"]["name"] == "testdb"
    assert result["app"]["name"] == "test-app"
    assert result["app"]["port"] == 8080


def test_load_config_files_invalid_extension(tmp_path):
    invalid_file = tmp_path / "config.txt"
    invalid_file.write_text("{}")
    with pytest.raises(ValueError) as exc:
        load_config_files([str(invalid_file)])
    assert "Unsupported config file format" in str(exc.value)


def test_override_with_env_vars():
    config = {
        "database": {
            "host": "localhost",
            "port": 5432
        }
    }

    config_copy = json.loads(json.dumps(config))

    env_vars = {
        "TEST_database__host": "remotehost",
        "TEST_database__port": "5433",
        "TEST_other__value": "test"
    }

    with patch.dict(os.environ, env_vars, clear=True):
        result = override_with_env_vars(config_copy, prefix="TEST_")
        assert result == {
            "database": {
                "host": "remotehost",
                "port": "5433"
            },
            "other": {
                "value": "test"
            }
        }
        assert config["database"]["host"] == "localhost"
        assert config["database"]["port"] == 5432


def test_override_with_env_vars_no_prefix():
    config = {"key": "value"}
    with patch.dict(os.environ, {}, clear=True):
        result = override_with_env_vars(config)
        assert result == config


def test_override_with_env_vars_empty_config():
    config = {}
    with patch.dict(os.environ, {"TEST_new__key": "value"}, clear=True):
        result = override_with_env_vars(config, prefix="TEST_")
        assert result == {"new": {"key": "value"}}


def test_override_with_env_vars_nested_override():
    config = {
        "level1": {
            "level2": {
                "key": "original"
            }
        }
    }

    config_copy = json.loads(json.dumps(config))

    env_vars = {"PRE_level1__level2__key": "new"}
    with patch.dict(os.environ, env_vars, clear=True):
        result = override_with_env_vars(config_copy, prefix="PRE_")
        assert result == {
            "level1": {
                "level2": {
                    "key": "new"
                }
            }
        }
        assert config["level1"]["level2"]["key"] == "original"
