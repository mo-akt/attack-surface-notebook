from src.cli import (
    analyze_endpoint_security,
    extract_security_schemes,
    get_operation_security,
)
def test_extract_security_schemes_no_schemes():
    # 1. No security schemes
    data = {}
    assert extract_security_schemes(data) == []

def test_extract_security_schemes_bearer_auth():
    # 2. BearerAuth Input
    data = {
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer"
                }
            }
        }
    }
    
    expected = {
        "name": "BearerAuth",
        "type": "http",
        "scheme": "bearer"
    }
    
    result = extract_security_schemes(data)
    assert expected in result

def test_extract_security_schemes_api_key_auth():
    # 3. ApiKeyAuth Input
    data = {
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                }
            }
        }
    }
    
    expected = {
        "name": "ApiKeyAuth",
        "type": "apiKey",
        "in": "header",
        "param_name": "X-API-Key"
    }
    
    result = extract_security_schemes(data)
    assert expected in result


def test_operation_uses_local_security():
    operation = {
        "security": [
            {"ApiKeyAuth": []}
        ]
    }

    global_security = [
        {"BearerAuth": []}
    ]

    result = get_operation_security(operation, global_security)

    assert result == [
        {"ApiKeyAuth": []}
    ]

def test_operation_inherits_global_security():
    operation = {}

    global_security = [
        {"BearerAuth": []}
    ]

    result = get_operation_security(operation, global_security)

    assert result == [
        {"BearerAuth": []}
    ]

def test_operation_empty_security_overrides_global():
    operation = {
        "security": []
    }

    global_security = [
        {"BearerAuth": []}
    ]

    result = get_operation_security(operation, global_security)

    assert result == []
def test_analyze_endpoint_inherits_global():
    data = {
        "security": [
            {"BearerAuth": []}
        ],
        "paths": {
            "/products": {
                "get": {}
            }
        }
    }

    result = analyze_endpoint_security(data)

    assert result == [
        {
            "method": "GET",
            "path": "/products",
            "security": ["BearerAuth"]
        }
    ]

def test_analyze_endpoint_uses_local_security():
    data = {
        "security": [
            {"BearerAuth": []}
        ],
        "paths": {
            "/admin": {
                "post": {
                    "security": [
                        {"ApiKeyAuth": []}
                    ]
                }
            }
        }
    }

    result = analyze_endpoint_security(data)

    assert result == [
        {
            "method": "POST",
            "path": "/admin",
            "security": ["ApiKeyAuth"]
        }
    ]

def test_analyze_endpoint_empty_security():
    data = {
        "security": [
            {"BearerAuth": []}
        ],
        "paths": {
            "/public": {
                "get": {
                    "security": []
                }
            }
        }
    }

    result = analyze_endpoint_security(data)

    assert result == [
        {
            "method": "GET",
            "path": "/public",
            "security": []
        }
    ]
