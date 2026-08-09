import json
import pytest
from src.cli import load_openapi

# Test 1 — Valid file
def test_load_valid_openapi(tmp_path):
    """Ensure a valid JSON file is read correctly and returns a dictionary."""
    file_path = tmp_path / "openapi.json"
    data = {
        "info": {
            "title": "Demo API",
            "version": "1.0.0"
        },
        "paths": {}
    }
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_openapi(file_path)
    assert result["info"]["title"] == "Demo API"

# Test 2 — Missing file
def test_missing_file():
    """Ensure FileNotFoundError is raised when the file does not exist."""
    with pytest.raises(FileNotFoundError):
        load_openapi("does-not-exist.json")

# Test 3 — Invalid JSON
def test_invalid_json(tmp_path):
    """Ensure json.JSONDecodeError is raised when the file contains invalid JSON."""
    file_path = tmp_path / "bad.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_openapi(file_path)
