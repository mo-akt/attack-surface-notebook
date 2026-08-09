# Attack Surface Notebook

## Problem Statement

Security engineers often need to inspect APIs and understand their attack surface before performing a security review.

This project aims to analyze OpenAPI specifications and extract useful security information such as endpoints, authentication methods, and potential attack surface.

## Current Status

The project currently provides a Python CLI for loading and inspecting OpenAPI JSON specifications.

Implemented functionality:

- Load OpenAPI specifications from JSON files
- Handle missing files and malformed JSON
- Validate required OpenAPI fields
- Extract HTTP methods and endpoint paths
- Normalize HTTP methods
- Ignore non-operation path fields such as `parameters`
- Automated tests using pytest

Current test suite: 12 tests passing.

## Planned Features

- Detect authentication methods and security schemes
- Extract parameters and request metadata
- Identify potentially sensitive endpoints
- Generate an attack surface summary
- Store analysis results
- Export reports

## Ethical Use

This project is intended only for defensive security, education, and authorized security assessments.