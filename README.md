# Attack Surface Notebook

A Python-based security analysis tool for mapping API attack surfaces from OpenAPI specifications.

It extracts endpoints, authentication requirements, parameters, and explainable security review signals, and stores structured analysis results in SQLite for further security review and reporting.

> Review signals are heuristic indicators for prioritizing manual security review. They are not confirmed vulnerabilities.

## Current Status

The project currently provides a Python CLI for loading, validating, and analyzing OpenAPI JSON specifications.

Implemented functionality:

- Load OpenAPI specifications from JSON files
- Handle missing files and malformed JSON
- Validate required OpenAPI fields
- Extract HTTP methods and endpoint paths
- Normalize HTTP methods
- Ignore non-operation path fields such as `parameters`
- Extract defined security schemes
- Detect HTTP Bearer and API key security schemes
- Analyze authentication requirements for each API operation
- Support global and operation-level security requirements
- Identify operations with no authentication requirement
- Automated tests using pytest
- Extract path-level and operation-level parameters
- Support path, query, header, and cookie parameter metadata
- Merge inherited path-level parameters with operation-level parameters
- Support operation-level parameter overrides
- Display parameter location and required/optional status in the CLI
- Tag endpoints with explainable security review signals
- Identify user/account-related and admin-related API surfaces
- Identify authentication-related paths and sensitive input names
- Flag destructive HTTP operations for additional review
- Support multiple review signals per endpoint
- SQLite persistence for analyzed API endpoints
- Relational storage for authentication requirements, parameters, and review signals
- Duplicate-safe endpoint and analysis storage
- Foreign key relationships between endpoints and analysis data

Current test suite: 45 tests passing.

### SQLite Persistence

Analysis results can be stored locally in `attack_surface.db`.

The database currently stores:

- API endpoints
- Authentication requirements
- Parameters
- Review signals

Related analysis data is linked to its endpoint using foreign keys.

Parameterized SQL queries are used when inserting and retrieving values.

### Review Signal Limitations

Review signals are heuristic indicators intended to help prioritize manual security review.

They do not represent confirmed vulnerabilities. A signal such as `admin-surface`, `sensitive-input`, or `destructive-operation` indicates that an endpoint may deserve additional review, but further evidence is required before making a security finding.

## Planned Features
- Generate an attack surface summary
- Export Markdown and HTML reports
- Compare two API versions and identify newly introduced attack surface
- Generate a threat-model worksheet
- Add HAR file support