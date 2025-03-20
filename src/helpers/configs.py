import json
import os
from typing import Any, Dict, List

import yaml


def load_config_files(file_paths: List[str]) -> Dict[str, Any]:
    """
    Loads and merges multiple configuration files (JSON or YAML).
    Later files overwrite keys from earlier files.
    """
    merged_config = {}
    for path in file_paths:
        data = _load_single_config(path)
        merged_config = _deep_merge(merged_config, data)
    return merged_config


def override_with_env_vars(config: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """
    Overrides config entries with environment variables, if they exist.
    For example, if prefix="MYAPP_", env var "MYAPP_DATABASE__HOST"
    will override config["database"]["host"], splitting by double underscores.
    """
    new_config = dict(config)
    for var, val in os.environ.items():
        if not var.startswith(prefix):
            continue
        # remove prefix
        stripped = var[len(prefix):]
        # path split by double underscores
        keys = stripped.split("__")
        _set_nested_key(new_config, keys, val)
    return new_config


def _load_single_config(path: str) -> Dict[str, Any]:
    if path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    elif path.lower().endswith(".yml") or path.lower().endswith(".yaml"):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported config file format: {path}")


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merges override keys into base dictionary.
    """
    result = dict(base)
    for key, val in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(val, dict)
        ):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def _set_nested_key(config_dict: Dict[str, Any], keys: List[str], value: Any) -> None:
    """
    Sets a nested key in a dictionary. For example:
      keys = ["database", "host"] => config_dict["database"]["host"] = value
    """
    d = config_dict
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    # Final key
    d[keys[-1]] = value
