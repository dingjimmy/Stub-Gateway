# Stub Gateway — Requirements

This document states **what** the system must do at a requirements level. **Observable behaviour** is specified in full as executable Gherkin scenarios in [`specs/`](../specs/). Implementation choices (database, in-memory store, framework, UI framework) are intentionally omitted.

---

## How to use this documentation

| Document | Role |
|----------|------|
| This file (`docs/requirements.md`) | High-level requirements, scope, and capability map |
| [`specs/*.spec`](../specs/) | Canonical BDD scenarios (rules and examples) for acceptance tests and implementation |

When adding or changing behaviour, update the relevant `.spec` file first, then adjust this document only if scope, capabilities, or non-functional expectations change.

---

## Purpose

Stub Gateway is a lightweight HTTP test-double that stands in for third-party services during automated acceptance tests. Test authors define which URLs the double listens on and which responses it returns; the system under test interacts with it as it would with a real service.

This lets acceptance tests run without depending on real external HTTP services. A test suite configures predictable responses for specific requests, sends traffic to the double, and asserts on responses and optionally on recorded request traffic. Configuration can be prepared, reset, and isolated between runs so tests remain repeatable in CI and parallel execution.

---

## Core concepts

- **Stub** — A rule: when an incoming request matches specified criteria, respond in a defined way.
- **Recording** — A stored copy of a request the system actually received, for later inspection in tests.
- **Workspace** — An optional isolated namespace of configuration so parallel test runs do not interfere with each other.

**Scope assumptions (behavioural, not implementation):**

- The system speaks HTTP/1.1 (and optionally HTTPS) on a configurable base URL.
- Configuration can be applied before or while the service is running, via a management interface (web UI and/or HTTP API; exact channel is unspecified).
- Management UI, API, or both may be offered; behaviour must be consistent across channels.

---

## Capability areas

Each area below summarises the requirement. Detailed rules and Gherkin scenarios live in the linked spec file.

### Run the stub service

The service must start and stop cleanly, expose a reachable HTTP endpoint for tests, report running status including base URL, and reject a second listener on the same port without disrupting the existing one.

**Spec:** [`specs/run-stub-service.spec`](../specs/run-stub-service.spec)

### Define stubs

Stubs match incoming requests by method, path, and optionally query string, headers, and body. Each stub defines a complete HTTP response (status, headers, body). Unmatched requests return an explicit 404 suitable for failing tests. Stubs can be added, updated, and removed while the service stays up.

**Spec:** [`specs/define-stubs.spec`](../specs/define-stubs.spec)

### Path patterns

Stubs can match paths with placeholders for variable segments (for example `/users/{id}`). When multiple stubs could match, more specific rules take precedence over general patterns.

**Spec:** [`specs/path-patterns.spec`](../specs/path-patterns.spec)

### Realistic third-party behaviour

Beyond a single static response, a stub can return responses in a defined sequence (with explicit behaviour after the sequence is exhausted), introduce configurable delay before responding, and simulate HTTP errors or connection-level failures.

**Spec:** [`specs/realistic-behaviour.spec`](../specs/realistic-behaviour.spec)

### Record traffic

When recording is enabled, received requests are stored with method, path, headers, and body, ordered by arrival time. Recordings can be cleared between tests and filtered (for example by path) for assertions.

**Spec:** [`specs/record-traffic.spec`](../specs/record-traffic.spec)

### Configuration lifecycle

The full stub configuration can be exported and imported so behaviour is portable between environments. Configuration can be reset to an empty baseline (stubs and recordings cleared). Invalid configuration is rejected without partial application.

**Spec:** [`specs/configuration.spec`](../specs/configuration.spec)

### Management

Operators can view active stubs and service status, and create or edit stubs without hand-editing raw HTTP traffic. Management actions exposed for automation must produce the same outcomes as the UI.

**Spec:** [`specs/management.spec`](../specs/management.spec)

### CI and parallel test runs

Test runs can target an isolated workspace of configuration when required (for example via a workspace header). Matched stub paths are served entirely by the double; outcomes must not depend on reachability of external hostnames implied by stub paths.

**Spec:** [`specs/ci-and-parallel-runs.spec`](../specs/ci-and-parallel-runs.spec)

---

## Non-functional requirements

These expectations are observable in test and operations, not internal design targets.

| Concern | Requirement |
|---------|-------------|
| Startup time | From "start" to first successful HTTP response on a preconfigured stub completes within a limit agreed for CI (for example under 5 seconds on a reference machine). |
| Determinism | Same configuration and same sequence of client requests produce the same responses and recordings every time. |
| Transparency | Unmatched requests and validation failures return explicit, human-readable messages suitable for failing acceptance tests. |

---

## Out of scope

Unless added in a later version:

- TLS certificate management beyond "listener accepts HTTPS" if offered.
- SOAP/gRPC non-HTTP protocols.
- Full traffic replay from production captures.
- Authentication of management UI (may be required in shared environments; not specified here).

---

## Spec file index

| Spec file | Feature |
|-----------|---------|
| [`run-stub-service.spec`](../specs/run-stub-service.spec) | Run the stub service for acceptance tests |
| [`define-stubs.spec`](../specs/define-stubs.spec) | Define stubs that map requests to predetermined responses |
| [`path-patterns.spec`](../specs/path-patterns.spec) | Support path patterns for services with variable identifiers |
| [`realistic-behaviour.spec`](../specs/realistic-behaviour.spec) | Replicate realistic third-party behaviour beyond a single static response |
| [`record-traffic.spec`](../specs/record-traffic.spec) | Record traffic for assertions in acceptance tests |
| [`configuration.spec`](../specs/configuration.spec) | Prepare and reset configuration for repeatable test runs |
| [`management.spec`](../specs/management.spec) | Operate the system through a lightweight management experience |
| [`ci-and-parallel-runs.spec`](../specs/ci-and-parallel-runs.spec) | Use the double safely in CI and parallel test runs |
