def infer_assets(signals):
    assets = []

    if "user-data" in signals:
        assets.append("User/account data")

    if "admin-surface" in signals:
        assets.append("Administrative capabilities")

    if "authentication-related" in signals:
        assets.append("Authentication/session assets")

    return assets


def infer_threats(method, path, security, parameters, signals):
    threats = []

    parameter_names = {
        parameter.get("name", "").lower()
        for parameter in parameters
    }

    if "user-data" in signals:
        threats.append(
            "An authenticated user may attempt to access or manipulate "
            "user data outside their authorized scope."
        )

    if "admin-surface" in signals:
        threats.append(
            "A lower-privileged authenticated user may attempt to invoke "
            "an administrative operation."
        )

    if "authentication-related" in signals:
        threats.append(
            "An attacker may attempt to abuse the authentication or "
            "session-related operation."
        )

    if "destructive-operation" in signals:
        threats.append(
            "An unauthorized or unintended caller may attempt to perform "
            "a destructive operation."
        )

    if "sensitive-input" in signals:
        threats.append(
            "Sensitive input may be exposed, mishandled, or processed "
            "without appropriate protection."
        )

    if "id" in parameter_names and "user-data" in signals:
        threats.append(
            "A caller may attempt to access another user's object by "
            "manipulating an identifier parameter."
        )

    return threats


def infer_security_assumptions(method, path, security, parameters, signals):
    assumptions = []

    parameter_names = {
        parameter.get("name", "").lower()
        for parameter in parameters
    }

    has_object_identifier = "id" in parameter_names

    # Missing declared authentication is relevant unless this is
    # an authentication entry point such as login.
    if not security and "authentication-related" not in signals:
        assumptions.append(
            "The OpenAPI specification does not declare an authentication "
            "requirement for this operation."
        )

    if security:
        assumptions.append(
            "Declared authentication requirements are enforced by the backend."
        )

    if "user-data" in signals and has_object_identifier:
        assumptions.append(
            "The backend enforces object-level authorization before returning "
            "or modifying user-related data."
        )

    if "user-data" in signals and not has_object_identifier:
        assumptions.append(
            "Access to user-related data and operations is restricted to "
            "appropriately authorized callers."
        )

    if "admin-surface" in signals:
        assumptions.append(
            "Administrative operations require appropriate administrative "
            "authorization."
        )

    if "authentication-related" in signals:
        assumptions.append(
            "Authentication and session handling are implemented with "
            "appropriate validation and abuse protections."
        )

    if "destructive-operation" in signals:
        assumptions.append(
            "Destructive operations require appropriate authorization and "
            "are protected against unintended execution."
        )

    return assumptions

def infer_review_questions(method, path, security, parameters, signals):
    questions = []

    parameter_names = {
        parameter.get("name", "").lower()
        for parameter in parameters
    }

    has_object_identifier = "id" in parameter_names

    # Do not automatically treat an authentication endpoint such as /login
    # as suspicious merely because it has no declared authentication.
    if not security and "authentication-related" not in signals:
        questions.append(
            "Is authentication enforced outside the OpenAPI specification, "
            "such as by middleware or an API gateway?"
        )

    if "user-data" in signals and has_object_identifier:
        questions.append(
            "Can an authenticated user access or modify another user's data "
            "by changing the object identifier?"
        )

    if "user-data" in signals and not has_object_identifier:
        questions.append(
            "What authorization controls restrict access to this "
            "user-related operation?"
        )

    if "admin-surface" in signals:
        questions.append(
            f"Can a non-admin authenticated user successfully invoke "
            f"{method} {path}?"
        )

    if "authentication-related" in signals:
        questions.append(
            "Are authentication failures, token handling, and repeated "
            "authentication attempts handled securely?"
        )

    if "destructive-operation" in signals:
        questions.append(
            "What authorization controls prevent unauthorized or accidental "
            "execution of this destructive operation?"
        )

    if "sensitive-input" in signals:
        questions.append(
            "Could sensitive input be exposed through URLs, logs, headers, "
            "error messages, or other unintended locations?"
        )
    return questions

def build_threat_model(analysis_results):
    threat_model = []

    for result in analysis_results:
        method = result.get("method", "").upper()
        path = result.get("path", "")
        security = result.get("security", [])
        parameters = result.get("parameters", [])
        signals = result.get("signals", [])

        operation_model = {
            "method": method,
            "path": path,
            "assets": infer_assets(signals),
            "threats": infer_threats(
                method,
                path,
                security,
                parameters,
                signals
            ),
            "security_assumptions": infer_security_assumptions(
                method,
                path,
                security,
                parameters,
                signals
            ),
            "review_questions": infer_review_questions(
                method,
                path,
                security,
                parameters,
                signals
            )
        }

        threat_model.append(operation_model)

    return threat_model