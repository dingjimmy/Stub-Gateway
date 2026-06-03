# Stub Gateway

A lightweight HTTP test-double for acceptance tests. Replace third-party services with configurable stubs that return predetermined responses, without depending on real external systems.

This repository is **specification-first**: behaviour is defined in BDD form before implementation. The canonical specification lives in [docs/behaviour-spec.md](docs/behaviour-spec.md). Executable examples are in [specs/](specs/).

## Repository layout

| Path | Purpose |
|------|---------|
| `docs/behaviour-spec.md` | Full behaviour specification (scenarios, rules, examples) |
| `specs/` | Gherkin spec files (`.spec`) derived from the behaviour spec |
| `src/` | Application implementation (to be added) |

## Working with the spec

1. Read `docs/behaviour-spec.md` for observable behaviour (the *what*).
2. Implement against scenarios in `specs/`; keep step definitions thin and aligned with the spec language.
3. Add new behaviour by updating the spec first, then the matching `.spec` file.

## Status

Specification and Gherkin spec files are in place. Runtime implementation is not started.
