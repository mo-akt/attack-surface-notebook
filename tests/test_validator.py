import pytest
from src.cli import validate_openapi
# Test 1: Valid and complete OpenAPI document
def test_validate_openapi_valid():
    valid_data = {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API",
            "version": "1.0.0"
        },
        "paths": {}
    }
    assert validate_openapi(valid_data) is True


# Test 2: Missing the 'info' field
def test_validate_openapi_missing_info():
    invalid_data = {
        "openapi": "3.0.0",
        "paths": {}
    }
    with pytest.raises(ValueError, match="Missing required field: info"):
        validate_openapi(invalid_data)


# Test 3: Missing the 'paths' field
def test_validate_openapi_missing_paths():
    invalid_data = {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API",
            "version": "1.0.0"
        }
    }
    with pytest.raises(ValueError, match="Missing required field: paths"):
        validate_openapi(invalid_data)


# Test 4: Missing the 'version' field inside 'info'
def test_validate_openapi_missing_version():
    invalid_data = {
        "openapi": "3.0.0",
        "info": {
            "title": "Sample API"
        },
        "paths": {}
    }
    with pytest.raises(ValueError, match="Missing required field: info.version"):
        validate_openapi(invalid_data)

def test_validate_openapi_rejects_non_object_paths():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": []
    }

    with pytest.raises(ValueError):
        validate_openapi(data)

def test_validate_openapi_rejects_non_object_path_item():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": ["get"]
        }
    }

    with pytest.raises(ValueError):
        validate_openapi(data)

def test_validate_openapi_rejects_non_object_operation():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": []
            }
        }
    }

    with pytest.raises(ValueError):
        validate_openapi(data)

def test_validate_openapi_rejects_non_object_document():
    with pytest.raises(ValueError):
        validate_openapi([])


def test_validate_openapi_rejects_non_list_path_parameters():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "parameters": {}
            }
        }
    }

    with pytest.raises(ValueError):
        validate_openapi(data)


def test_validate_openapi_rejects_non_object_path_parameter():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "parameters": ["invalid-parameter"]
            }
        }
    }

    with pytest.raises(ValueError):
        validate_openapi(data)


def test_validate_openapi_rejects_non_list_operation_parameters():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": {
                    "parameters": {}
                }
            }
        }
    }

    with pytest.raises(ValueError):
        validate_openapi(data)


def test_validate_openapi_rejects_non_object_operation_parameter():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": {
                    "parameters": ["invalid-parameter"]
                }
            }
        }
    }

    with pytest.raises(ValueError):
        validate_openapi(data)


def test_validate_openapi_rejects_non_list_operation_security():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/admin": {
                "get": {
                    "security": {}
                }
            }
        }
    }

    with pytest.raises(ValueError):
        validate_openapi(data)


def test_validate_openapi_rejects_non_list_global_security():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "security": {},
        "paths": {}
    }

    with pytest.raises(ValueError):
        validate_openapi(data)