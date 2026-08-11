from src.cli import extract_parameters


def test_path_and_operation_parameters_are_merged():
    """Ensure path-level and operation-level parameters are merged for an operation."""
    data = {
        "paths": {
            "/users/{id}": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True
                    }
                ],
                "get": {
                    "parameters": [
                        {
                            "name": "details",
                            "in": "query",
                            "required": False
                        }
                    ]
                }
            }
        }
    }

    result = extract_parameters(data)

    expected = [
        {
            "method": "GET",
            "path": "/users/{id}",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True
                },
                {
                    "name": "details",
                    "in": "query",
                    "required": False
                }
            ]
        }
    ]

    assert result == expected


def test_multiple_operation_parameters():
    """Ensure multiple operation-level parameters are extracted correctly."""
    data = {
        "paths": {
            "/search": {
                "get": {
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": True
                        },
                        {
                            "name": "X-Request-ID",
                            "in": "header",
                            "required": False
                        }
                    ]
                }
            }
        }
    }

    result = extract_parameters(data)

    expected = [
        {
            "method": "GET",
            "path": "/search",
            "parameters": [
                {
                    "name": "q",
                    "in": "query",
                    "required": True
                },
                {
                    "name": "X-Request-ID",
                    "in": "header",
                    "required": False
                }
            ]
        }
    ]

    assert result == expected


def test_operation_without_parameters():
    """Ensure an operation without parameters returns an empty parameter list."""
    data = {
        "paths": {
            "/health": {
                "get": {}
            }
        }
    }

    result = extract_parameters(data)

    expected = [
        {
            "method": "GET",
            "path": "/health",
            "parameters": []
        }
    ]

    assert result == expected


def test_path_parameter_is_applied_to_multiple_operations():
    """Ensure path-level parameters are inherited by all HTTP operations under the same path."""
    data = {
        "paths": {
            "/users/{id}": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True
                    }
                ],
                "get": {},
                "delete": {}
            }
        }
    }

    result = extract_parameters(data)

    expected = [
        {
            "method": "GET",
            "path": "/users/{id}",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True
                }
            ]
        },
        {
            "method": "DELETE",
            "path": "/users/{id}",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True
                }
            ]
        }
    ]

    assert result == expected
def test_operation_parameter_overrides_path_parameter():
    """Ensure an operation-level parameter overrides the same path-level parameter."""
    data = {
        "paths": {
            "/users/{id}": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "Path-level definition"
                    }
                ],
                "get": {
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "description": "GET-specific definition"
                        }
                    ]
                }
            }
        }
    }

    result = extract_parameters(data)

    expected = [
        {
            "method": "GET",
            "path": "/users/{id}",
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "description": "GET-specific definition"
                }
            ]
        }
    ]

    assert result == expected