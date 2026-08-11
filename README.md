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

Current test suite: 21 tests passing.

## Planned Features

- Extract parameters and request metadata
- Identify potentially sensitive endpoints
- Generate an attack surface summary
- Store analysis results
- Export reports