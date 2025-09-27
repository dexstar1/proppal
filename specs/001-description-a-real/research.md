# Research for Real Estate Investment Platform

This document outlines the decisions made to resolve the unknowns in the technical context of the implementation plan.

## Python Version

- **Decision**: Python 3.11
- **Rationale**: A recent, stable version of Python that is widely used and supported.
- **Alternatives considered**: Python 3.10, 3.12. 3.11 was chosen as a balance between being up-to-date and having wide library support.

## Testing Framework

- **Decision**: `pytest`
- **Rationale**: `pytest` is a mature, feature-rich testing framework for Python that is easy to use and has a large ecosystem of plugins.
- **Alternatives considered**: `unittest`. `pytest` was chosen for its more concise syntax and powerful features.

## Target Platform

- **Decision**: Modern web browsers (Chrome, Firefox, Safari, Edge - latest versions).
- **Rationale**: As a web application, the primary interface will be through a web browser.
- **Alternatives considered**: None.

## Performance Goals

- **Decision**:
    - Page load time: < 2 seconds
    - API response time: < 200ms (p95)
- **Rationale**: These are standard performance goals for a modern web application to ensure a good user experience.
- **Alternatives considered**: Stricter or looser goals. These were chosen as a reasonable starting point.

## Constraints

- **Decision**: No specific constraints identified.
- **Rationale**: The prompt did not mention any specific constraints.
- **Alternatives considered**: None.

## Scale/Scope

- **Decision**:
    - Initial user base: 10,000 users
    - Initial property listings: 100,000
- **Rationale**: These are reasonable starting estimates for a new platform, which can be used for initial capacity planning.
- **Alternatives considered**: Higher or lower estimates. These were chosen as a realistic target for a new application.
