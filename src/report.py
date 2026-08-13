
def generate_markdown_report(title, version, analysis_results):
    endpoint_count = len(analysis_results)

    lines = []
    lines.append("# Attack Surface Analysis Report")
    lines.append("")
    lines.append("## API Summary")
    lines.append("")
    lines.append(f"- API: {title}")
    lines.append(f"- Version: {version}")
    lines.append(f"- Endpoints: {endpoint_count}")
    lines.append("")
    lines.append("## Endpoint Analysis")

    for result in analysis_results:
        method = result["method"]
        path = result["path"]
        security = result.get("security", [])
        parameters = result.get("parameters", [])
        signals = result.get("signals", [])
        lines.append("")
        lines.append(f"### {method} {path}")
        lines.append("")
        lines.append("**Authentication**")
        lines.append("")
        if security:
            for scheme in security:
                lines.append(f"- {scheme}")
        else:
            lines.append("- No authentication requirement is declared in the OpenAPI specification.")

        lines.append("")
        lines.append("**Parameters**")
        lines.append("")
        if parameters:
           for parameter in parameters:
               name = parameter.get("name", "")
               location = parameter.get("in", "")

               if parameter.get("required", False):
                   required = "required"
               else:
                   required = "optional"

               lines.append(
                   f"- `{name}` — {location} — {required}"
               )
        else:
            lines.append("- None declared")
        lines.append("")
        lines.append("**Review Signals**")
        lines.append("")

        if signals:
            for signal in signals:
                lines.append(f"- {signal}")
        else:
            lines.append("- None")
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    lines.append("Review signals are heuristic indicators intended to prioritize manual security review.")
    lines.append("They do not represent confirmed vulnerabilities and require further evidence and authorized testing.")

    return "\n".join(lines)

def save_markdown_report(report_text, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report_text)

def generate_comparison_section(comparison_result):
    lines = []

    added = [
        f"- {endpoint['method']} {endpoint['path']}"
        for endpoint in comparison_result.get("added", [])
    ]

    removed = [
        f"- {endpoint['method']} {endpoint['path']}"
        for endpoint in comparison_result.get("removed", [])
    ]

    unchanged = [
        f"- {endpoint['method']} {endpoint['path']}"
        for endpoint in comparison_result.get("unchanged", [])
    ]

    lines.append("## API Version Comparison")
    lines.append("")

    lines.append("### Newly Introduced Attack Surface")
    lines.append("")

    if added:
        lines.extend(added)
    else:
        lines.append("_No new endpoints added._")

    lines.append("")
    lines.append("### Removed Attack Surface")
    lines.append("")

    if removed:
        lines.extend(removed)
    else:
        lines.append("_No endpoints were removed._")

    lines.append("")
    lines.append("### Unchanged Operations")
    lines.append("")
    if unchanged:
        lines.extend(unchanged)
    else:
        lines.append("_No unchanged endpoints._")

    return "\n".join(lines)

def generate_threat_model_section(threat_model):
    lines = []

    lines.append("## Threat Model Worksheet")
    lines.append("")

    if not threat_model:
        lines.append("_No threat-model entries generated._")
        return "\n".join(lines)

    for operation in threat_model:
        method = operation.get("method", "")
        path = operation.get("path", "")

        assets = operation.get("assets", [])
        threats = operation.get("threats", [])
        assumptions = operation.get("security_assumptions", [])
        questions = operation.get("review_questions", [])

        lines.append(f"### {method} {path}")
        lines.append("")

        lines.append("**Assets**")
        lines.append("")
        if assets:
            for asset in assets:
                lines.append(f"- {asset}")
        else:
            lines.append("- None inferred")

        lines.append("")
        lines.append("**Potential Threats**")
        lines.append("")
        if threats:
            for threat in threats:
                lines.append(f"- {threat}")
        else:
            lines.append("- None inferred from current analysis evidence")

        lines.append("")
        lines.append("**Security Assumptions**")
        lines.append("")
        if assumptions:
            for assumption in assumptions:
                lines.append(f"- {assumption}")
        else:
            lines.append("- None")

        lines.append("")
        lines.append("**Review Questions**")
        lines.append("")
        if questions:
            for question in questions:
                lines.append(f"- {question}")
        else:
            lines.append("- None")

        lines.append("")

    lines.append("### Threat Model Limitations")
    lines.append("")
    lines.append(
        "Threat scenarios and review questions are generated from available "
        "OpenAPI analysis evidence and do not represent confirmed vulnerabilities."
    )

    return "\n".join(lines)