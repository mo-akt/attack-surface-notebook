# Attack Surface Notebook

A Python-based security analysis tool for mapping API attack surfaces from OpenAPI specifications.

It extracts endpoints, authentication requirements, parameters, and explainable security review signals, stores structured analysis results in SQLite, generates Markdown reports, and compares API versions to identify newly introduced attack surface.

> Review signals are heuristic indicators for prioritizing manual security review. They are not confirmed vulnerabilities.

## Problem Statement

Security engineers often need to inspect APIs and understand their attack surface before performing a security review.

This project analyzes OpenAPI specifications and extracts structured security-relevant information such as endpoints, authentication requirements, parameters, review signals, and API version changes.

The goal is to support manual security review with organized evidence, not to claim automatic vulnerability discovery.

## Current Status

The project currently provides a Python CLI for loading, validating, analyzing, storing, reporting, and comparing OpenAPI JSON specifications.

Implemented functionality:

- Load and validate OpenAPI JSON specifications
- Extract HTTP methods and endpoint paths
- Analyze authentication requirements
- Support global and operation-level security requirements
- Extract path-level and operation-level parameters
- Merge inherited parameters and support operation-level overrides
- Tag endpoints with explainable security review signals
- Store endpoints, authentication requirements, parameters, and review signals in SQLite
- Prevent duplicate analysis records
- Generate Markdown attack surface analysis reports
- Compare two OpenAPI versions using HTTP method and path identity
- Detect added, removed, and unchanged API operations
- Generate Markdown API version comparison reports
- Automated testing using pytest

Current test suite: 54 tests passing.

## Architecture

```mermaid
flowchart TD
    A[OpenAPI Specification] --> B[Parser]
    B --> C[Security Analysis]

    C --> D[Authentication Analysis]
    C --> E[Parameter Analysis]
    C --> F[Review Signals]

    C --> G[SQLite Persistence]
    C --> H[Markdown Report]

    I[OpenAPI V1] --> J[API Version Comparison]
    K[OpenAPI V2] --> J

    J --> L[Added Operations]
    J --> M[Removed Operations]
    J --> N[Unchanged Operations]

    J --> O[Comparison Report]

## SQLite Persistence

Analysis results can be stored locally in `attack_surface.db`.

The database stores:

- API endpoints
- Authentication requirements
- Parameters
- Review signals

Related analysis data is linked to its endpoint using foreign keys.

Endpoint identity is based on the combination of HTTP method and path.

For example:

```text
GET /users
DELETE /users
```

are treated as different API operations.

Parameterized SQL queries are used when inserting and retrieving values.

## Markdown Reports

The project generates Markdown reports containing:

- API summary
- Endpoint inventory
- Authentication requirements
- Parameter metadata
- Review signals
- Analysis limitations

The reports distinguish heuristic review signals from confirmed security findings.

## API Version Comparison

The CLI can compare two OpenAPI specifications and classify API operations as:

- Added
- Removed
- Unchanged

API operation identity is based on:

```text
(method, path)
```

For example:

```text
V1:
GET /users
DELETE /legacy

V2:
GET /users
POST /admin/users
```

The comparison identifies:

```text
Added:
POST /admin/users

Removed:
DELETE /legacy

Unchanged:
GET /users
```

New operations are treated as newly introduced attack surface requiring review, not as confirmed vulnerabilities.

## Review Signal Limitations

Review signals are heuristic indicators intended to help prioritize manual security review.

Examples include:

- `user-data`
- `admin-surface`
- `authentication-related`
- `destructive-operation`
- `sensitive-input`

These signals do not represent confirmed vulnerabilities.

A signal indicates that an endpoint may deserve additional review, but further evidence and authorized testing are required before making a security finding.

The project distinguishes between:

```text
Observation
    ↓
Review Signal / Heuristic
    ↓
Confirmed Finding
```

## Running the CLI

Run the project from the repository root:

```powershell
python -m src.cli
```

The CLI provides two modes:

```text
1. Analyze API
2. Compare API versions
```

### Analyze API

This mode analyzes one OpenAPI specification, stores structured results in SQLite, and generates a Markdown attack surface report.

### Compare API Versions

This mode compares an old and new OpenAPI specification and generates a Markdown report showing added, removed, and unchanged API operations.

## Testing

Run the full test suite:

```powershell
python -m pytest
```

Current test suite:

```text
54 tests passing
```

Tests cover the main parsing, validation, security analysis, persistence, reporting, and API comparison functionality.

## Known Limitations

- OpenAPI documentation may not reflect the application's actual runtime security controls.
- Missing authentication declarations do not prove that an endpoint is unauthenticated in production.
- Review signals are heuristic and require manual validation.
- API version comparison currently focuses on HTTP method and path changes.
- Changes to request bodies, schemas, authentication requirements, and parameter definitions are not yet included in version comparison.

## Planned Features

- Export HTML reports
- Generate a threat-model worksheet
- Add HAR file support

## Ethical Use

This project is intended for defensive security, security education, local laboratories, systems you own, and security assessments where you have explicit authorization.

Do not use this project to test systems without permission.