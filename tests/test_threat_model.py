from src.threat_model import (
    infer_assets,
    build_threat_model,
)


def test_infer_assets_from_review_signals():
    signals = [
        "user-data",
        "admin-surface",
        "authentication-related",
        "destructive-operation",
    ]

    assets = infer_assets(signals)

    assert assets == [
        "User/account data",
        "Administrative capabilities",
        "Authentication/session assets",
    ]


def test_build_threat_model_for_user_data_endpoint():
    analysis_results = [
        {
            "method": "get",
            "path": "/users/{id}",
            "security": ["BearerAuth"],
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                }
            ],
            "signals": ["user-data"],
        }
    ]

    result = build_threat_model(analysis_results)

    assert len(result) == 1

    operation = result[0]

    assert operation["method"] == "GET"
    assert operation["path"] == "/users/{id}"
    assert "User/account data" in operation["assets"]

    assert any(
        "another user's object" in threat
        for threat in operation["threats"]
    )

    assert any(
        "object-level authorization" in assumption
        for assumption in operation["security_assumptions"]
    )

    assert any(
        "object identifier" in question
        for question in operation["review_questions"]
    )


def test_build_threat_model_for_admin_endpoint():
    analysis_results = [
        {
            "method": "post",
            "path": "/admin/users",
            "security": ["BearerAuth"],
            "parameters": [],
            "signals": ["admin-surface"],
        }
    ]

    result = build_threat_model(analysis_results)

    operation = result[0]

    assert "Administrative capabilities" in operation["assets"]

    assert any(
        "lower-privileged" in threat
        for threat in operation["threats"]
    )

    assert any(
        "non-admin" in question
        for question in operation["review_questions"]
    )


def test_build_threat_model_handles_no_declared_security():
    analysis_results = [
        {
            "method": "post",
            "path": "/login",
            "security": [],
            "parameters": [],
            "signals": ["authentication-related"],
        }
    ]

    result = build_threat_model(analysis_results)

    operation = result[0]

    assert not any(
        "middleware or an API gateway" in question
        for question in operation["review_questions"]
    )

    assert any(
        "authentication attempts" in question
        for question in operation["review_questions"]
    )

def test_user_data_without_id_does_not_infer_object_level_question():
    analysis_results = [
        {
            "method": "GET",
            "path": "/users",
            "security": [],
            "parameters": [],
            "signals": ["user-data"],
        }
    ]

    result = build_threat_model(analysis_results)
    operation = result[0]

    assert not any(
        "object identifier" in question
        for question in operation["review_questions"]
    )

    assert any(
        "authorization controls" in question
        for question in operation["review_questions"]
    )


def test_authentication_endpoint_without_security_is_not_treated_as_missing_auth():
    analysis_results = [
        {
            "method": "POST",
            "path": "/login",
            "security": [],
            "parameters": [],
            "signals": ["authentication-related"],
        }
    ]

    result = build_threat_model(analysis_results)
    operation = result[0]

    assert not any(
        "middleware or an API gateway" in question
        for question in operation["review_questions"]
    )

    assert any(
        "authentication attempts" in question
        for question in operation["review_questions"]
    )

def test_build_threat_model_handles_empty_input():
    assert build_threat_model([]) == []

def test_threat_model_handles_minimal_operation():
    analysis_results = [
        {
            "method": "GET",
            "path": "/health"
        }
    ]

    result = build_threat_model(analysis_results)

    assert len(result) == 1

    operation = result[0]

    assert operation["method"] == "GET"
    assert operation["path"] == "/health"
    assert operation["assets"] == []
    assert operation["threats"] == []
    assert isinstance(operation["security_assumptions"], list)
    assert isinstance(operation["review_questions"], list)


def test_threat_model_handles_partial_parameters_without_id_inference():
    analysis_results = [
        {
            "method": "GET",
            "path": "/users",
            "security": [],
            "parameters": [
                {"name": "username"},
                {"in": "header", "required": True},
                {}
            ],
            "signals": ["user-data"]
        }
    ]

    result = build_threat_model(analysis_results)
    operation = result[0]

    assert "User/account data" in operation["assets"]

    assert not any(
        "object identifier" in question.lower()
        for question in operation["review_questions"]
    )

    assert any(
        "authorization controls" in question.lower()
        for question in operation["review_questions"]
    )


def test_duplicate_signals_do_not_duplicate_threat_model_output():
    analysis_results = [
        {
            "method": "POST",
            "path": "/admin/users",
            "security": ["BearerAuth"],
            "parameters": [],
            "signals": [
                "user-data",
                "admin-surface",
                "user-data",
                "admin-surface"
            ]
        }
    ]

    result = build_threat_model(analysis_results)
    operation = result[0]

    assert len(operation["assets"]) == len(set(operation["assets"]))
    assert len(operation["threats"]) == len(set(operation["threats"]))
    assert len(operation["security_assumptions"]) == len(
        set(operation["security_assumptions"])
    )
    assert len(operation["review_questions"]) == len(
        set(operation["review_questions"])
    )