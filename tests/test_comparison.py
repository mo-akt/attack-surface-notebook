from src.comparison import compare_api_versions

def test_compare_api_versions_detects_changes():
    v1_data = {
    "openapi": "3.0.0",
    "info": {
        "title": "Test API V1",
        "version": "1.0.0"
    },
    "paths": {
        "/users": {
            "get": {
                "summary": "Get all users"
            }
        },
        "/login": {
            "post": {
                "summary": "User login"
            }
        },
        "/health": {
            "get": {
                "summary": "Health check"
            }
        },
        "/legacy": {
            "delete": {
                "summary": "Legacy endpoint"
            }
        }
    }}
    v2_data = {
    "openapi": "3.0.0",
    "info": {
        "title": "Test API V2",
        "version": "2.0.0"
    },
    "paths": {
        "/users": {
            "get": {
                "summary": "Get all users"
            }
        },
        "/login": {
            "post": {
                "summary": "User login"
            }
        },
        "/health": {
            "get": {
                "summary": "Health check"
            }
        },
        "/admin/users": {
            "post": {
                "summary": "Create admin user"
            }
        }
    }
}

    result = compare_api_versions(v1_data, v2_data)

    assert result["added"] == [
        {"method": "POST", "path": "/admin/users"}
    ]

    assert result["removed"] == [
        {"method": "DELETE", "path": "/legacy"}
    ]

    assert result["unchanged"] == [
        {"method": "GET", "path": "/health"},
        {"method": "GET", "path": "/users"},
        {"method": "POST", "path": "/login"},
    ]

def test_compare_api_versions_with_no_changes():
    v1_data = {
        "paths": {
            "/users": {
                "get": {}
            },
            "/health": {
                "get": {}
            }
        }
    }

    v2_data = {
        "paths": {
            "/users": {
                "get": {}
            },
            "/health": {
                "get": {}
            }
        }
    }

    result = compare_api_versions(v1_data, v2_data)

    assert result["added"] == []
    assert result["removed"] == []
    assert result["unchanged"] == [
        {"method": "GET", "path": "/health"},
        {"method": "GET", "path": "/users"},
    ]


def test_compare_api_versions_detects_method_change():
    v1_data = {
        "paths": {
            "/users": {
                "post": {}
            }
        }
    }

    v2_data = {
        "paths": {
            "/users": {
                "delete": {}
            }
        }
    }

    result = compare_api_versions(v1_data, v2_data)

    assert result["added"] == [
        {"method": "DELETE", "path": "/users"}
    ]

    assert result["removed"] == [
        {"method": "POST", "path": "/users"}
    ]

    assert result["unchanged"] == []
def test_compare_api_versions_handles_empty_old_api():
    v1_data = {
        "paths": {}
    }

    v2_data = {
        "paths": {
            "/health": {
                "get": {}
            }
        }
    }

    result = compare_api_versions(v1_data, v2_data)

    assert result["added"] == [
        {"method": "GET", "path": "/health"}
    ]

    assert result["removed"] == []
    assert result["unchanged"] == []
