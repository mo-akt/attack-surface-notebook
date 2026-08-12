from src.report import (
    generate_markdown_report,
    save_markdown_report,
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