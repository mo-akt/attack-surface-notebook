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

Current test suite: 26 tests passing.

## Planned Features

- Identify potentially sensitive endpoints
- Generate an attack surface summary
- Store analysis results
- Export reports