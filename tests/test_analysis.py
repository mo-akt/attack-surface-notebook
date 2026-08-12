from src.cli import build_analysis_results


def test_build_analysis_results_combines_endpoint_data():
    """Combine endpoint, authentication, parameters, and review signals into one result."""
    data = {
        "info": {
            "title": "Demo API",
            "version": "1.0.0"
        },
        "security": [
            {
                "BearerAuth": []
            }
        ],
        "paths": {
            "/admin/users/{id}": {
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True
                    }
                ],
                "delete": {}
            }
        }
    }

    result = build_analysis_results(data)

    expected = [
        {
            "method": "DELETE",
            "path": "/admin/users/{id}",
            "security": ["BearerAuth"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True
                }
            ],
            "signals": [
                "user-data",
                "admin-surface",
                "destructive-operation"
            ]
        }
    ]

    assert result == expected


def test_build_analysis_results_handles_public_endpoint():
    """Return empty security and review-signal lists when no indicators are present."""
    data = {
        "info": {
            "title": "Demo API",
            "version": "1.0.0"
        },
        "paths": {
            "/health": {
                "get": {}
            }
        }
    }

    result = build_analysis_results(data)

    expected = [
        {
            "method": "GET",
            "path": "/health",
            "security": [],
            "parameters": [],
            "signals": []
        }
    ]

    assert result == expected