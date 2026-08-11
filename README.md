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

Current test suite: 34 tests passing.

### Review Signal Limitations

Review signals are heuristic indicators intended to help prioritize manual security review.

They do not represent confirmed vulnerabilities. A signal such as `admin-surface`, `sensitive-input`, or `destructive-operation` indicates that an endpoint may deserve additional review, but further evidence is required before making a security finding.

## Planned Features

- Identify potentially sensitive endpoints
- Generate an attack surface summary
- Store analysis results
- Export reports