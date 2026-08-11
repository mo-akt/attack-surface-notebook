from src.cli import tag_review_signals


def test_user_data_signal():
    """Ensure user-related paths are tagged for review."""
    result = tag_review_signals(
        "GET",
        "/users/{id}",
        []
    )

    assert "user-data" in result


def test_admin_surface_signal():
    """Ensure admin-related paths are tagged for review."""
    result = tag_review_signals(
        "GET",
        "/admin/dashboard",
        []
    )

    assert "admin-surface" in result


def test_authentication_related_signal():
    """Ensure authentication-related paths are tagged for review."""
    result = tag_review_signals(
        "POST",
        "/login",
        []
    )

    assert "authentication-related" in result


def test_destructive_operation_signal():
    """Ensure DELETE operations are tagged as destructive."""
    result = tag_review_signals(
        "DELETE",
        "/products/{id}",
        []
    )

    assert "destructive-operation" in result


def test_sensitive_input_signal():
    """Ensure sensitive parameter names are tagged for review."""
    parameters = [
        {
            "name": "password",
            "in": "query",
            "required": True
        }
    ]

    result = tag_review_signals(
        "POST",
        "/login",
        parameters
    )

    assert "sensitive-input" in result


def test_multiple_review_signals():
    """Ensure an endpoint can receive multiple review signals."""
    parameters = [
        {
            "name": "secret",
            "in": "header",
            "required": True
        }
    ]

    result = tag_review_signals(
        "DELETE",
        "/admin/account/token",
        parameters
    )

    assert result == [
        "user-data",
        "admin-surface",
        "authentication-related",
        "destructive-operation",
        "sensitive-input"
    ]


def test_health_endpoint_has_no_signals():
    """Ensure unrelated endpoints do not receive review signals."""
    result = tag_review_signals(
        "GET",
        "/health",
        []
    )

    assert result == []


def test_method_matching_is_case_insensitive():
    """Ensure HTTP method matching is case-insensitive."""
    result = tag_review_signals(
        "delete",
        "/products/{id}",
        []
    )

    assert "destructive-operation" in result