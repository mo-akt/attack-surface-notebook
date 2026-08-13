import pytest
from src.cli import parse_endpoints

def test_single_get_endpoint():
    data = {
        "paths": {
            "/users": {
                "get": {}
            }
        }
    }

    result = parse_endpoints(data)

    assert result == [
        {"method": "GET", "path": "/users"}
    ]

def test_multiple_methods_same_path():
    data = {
        "paths": {
            "/users": {
                "get": {}
                ,"post":{}
            }
        }
    }

    result = parse_endpoints(data)

    assert result == [
        {"method": "GET", "path": "/users"}
        ,{"method": "POST", "path": "/users"}
    ]
def test_empty_get_endpoint():
    data = {
        "paths": {
        }
    }

    result = parse_endpoints(data)

    assert result == []
def test_parameters_get_endpoint():
    data = {
        "paths": {
            "/users": {
                "parameters": [],
                "get": {}
            }
        }
    }

    result = parse_endpoints(data)

    assert result == [
        {"method": "GET", "path": "/users"}
    ]
def test_uppercase_get_endpoint():
    data = {
        "paths": {
            "/users": {
                "GET": {}
            }
        }
    }

    result = parse_endpoints(data)

    assert result == [
        {"method": "GET", "path": "/users"}
    ]


def test_parse_endpoints_handles_non_object_path_item():
    data = {
        "info": {
            "title": "Broken API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": []
        }
    }

    endpoints = parse_endpoints(data)

    assert endpoints == []