# Stub Gateway

A lightweight HTTP test-double for acceptance tests. Replace third-party services with configurable stubs that return predetermined responses, without depending on real external systems.

This repository is **specification-first**: behaviour is defined in BDD form before implementation. High-level requirements are in [docs/requirements.md](docs/requirements.md). Canonical scenarios and rules are in [specs/](specs/).

## Repository layout

| Path | Purpose |
|------|---------|
| `docs/requirements.md` | High-level requirements, scope, and capability map |
| `specs/` | Gherkin spec files (`.spec`) with rules and executable scenarios |
| `src/` | Application implementation (to be added) |

## Working with the spec

1. Read `docs/requirements.md` for scope and capability overview.
2. Implement against scenarios in `specs/`; keep step definitions thin and aligned with the spec language.
3. Add new behaviour by updating the relevant `.spec` file first, then adjust the requirements doc if scope changes.

## Status

Specification and Gherkin spec files are in place. Runtime implementation is not started.
