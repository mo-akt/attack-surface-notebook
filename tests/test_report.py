from src.report import (
    generate_markdown_report,
    save_markdown_report,
    generate_comparison_section,
    generate_threat_model_section,
)

def test_generate_markdown_report_with_endpoint_analysis():
    analysis_results = [
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

    report = generate_markdown_report(
        "Demo API",
        "1.0.0",
        analysis_results
    )

    assert "# Attack Surface Analysis Report" in report
    assert "- API: Demo API" in report
    assert "- Version: 1.0.0" in report
    assert "- Endpoints: 1" in report

    assert "### DELETE /admin/users/{id}" in report
    assert "- BearerAuth" in report
    assert "- `id` — path — required" in report

    assert "- user-data" in report
    assert "- admin-surface" in report
    assert "- destructive-operation" in report

    assert "## Limitations" in report
    assert "do not represent confirmed vulnerabilities" in report


def test_generate_markdown_report_handles_empty_metadata():
    analysis_results = [
        {
            "method": "GET",
            "path": "/health",
            "security": [],
            "parameters": [],
            "signals": []
        }
    ]

    report = generate_markdown_report(
        "Health API",
        "1.0.0",
        analysis_results
    )

    assert "### GET /health" in report
    assert (
        "- No authentication requirement is declared "
        "in the OpenAPI specification."
    ) in report
    assert "- None declared" in report
    assert "**Review Signals**" in report

def test_save_markdown_report(tmp_path):
    report_text = "# Test Report\n\nHello"

    output_path = tmp_path / "report.md"

    save_markdown_report(
        report_text,
        output_path
    )

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == report_text

def test_generate_comparison_section():
    mock_result = {
        "added": [{"method": "POST", "path": "/admin/users"}],
        "removed": [{"method": "DELETE", "path": "/legacy"}],
        "unchanged": [
            {"method": "GET", "path": "/health"},
            {"method": "GET", "path": "/users"},
            {"method": "POST", "path": "/login"}
        ]
    }

    markdown_output = generate_comparison_section(mock_result)

    assert "## API Version Comparison" in markdown_output
    assert "### Newly Introduced Attack Surface" in markdown_output
    assert "- POST /admin/users" in markdown_output

    assert "### Removed Attack Surface" in markdown_output
    assert "- DELETE /legacy" in markdown_output

    assert "### Unchanged Operations" in markdown_output
    assert "- GET /health" in markdown_output

def test_generate_comparison_section_handles_empty_results():
    empty_result = {
        "added": [],
        "removed": [],
        "unchanged": []
    }

    markdown_output = generate_comparison_section(empty_result)

    assert "## API Version Comparison" in markdown_output

    assert "### Newly Introduced Attack Surface" in markdown_output
    assert "_No new endpoints added._" in markdown_output

    assert "### Removed Attack Surface" in markdown_output
    assert "_No endpoints were removed._" in markdown_output

    assert "### Unchanged Operations" in markdown_output
    assert "_No unchanged endpoints._" in markdown_output

def test_generate_threat_model_section():
    threat_model = [
        {
            "method": "GET",
            "path": "/users/{id}",
            "assets": ["User/account data"],
            "threats": [
                "A caller may attempt to access another user's object."
            ],
            "security_assumptions": [
                "The backend enforces object-level authorization."
            ],
            "review_questions": [
                "Can User A access User B's object by changing the identifier?"
            ],
        }
    ]

    output = generate_threat_model_section(threat_model)

    assert "## Threat Model Worksheet" in output
    assert "### GET /users/{id}" in output
    assert "User/account data" in output
    assert "another user's object" in output
    assert "object-level authorization" in output
    assert "Can User A access User B" in output
    assert "Threat Model Limitations" in output


def test_generate_threat_model_section_handles_empty_input():
    output = generate_threat_model_section([])

    assert "## Threat Model Worksheet" in output
    assert "_No threat-model entries generated._" in output