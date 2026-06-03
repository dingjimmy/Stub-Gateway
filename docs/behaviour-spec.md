# Stub Gateway — Behaviour Specification

A lightweight HTTP test-double that stands in for third-party services during automated acceptance tests. Test authors define which URLs the double listens on and which responses it returns; tests interact with it exactly as they would with a real service. This document states **observable behaviour only** (what the system does), not internal design (how it is built).

**Scope assumptions (behavioural, not implementation):**

- The system speaks HTTP/1.1 (and optionally HTTPS) on a configurable base URL.
- Configuration can be applied before or while the service is running, via a management interface (web UI and/or HTTP API — exact channel is unspecified).
- A **stub** is a rule: "when a request matches these criteria, respond like this."
- A **recording** is a stored copy of a request the system actually received.

---

## Scenario: Run the stub service for acceptance tests

### Rule: The service exposes a reachable HTTP endpoint for tests

**Example: Start listening on a chosen port**

```gherkin
Given no stub service is listening on port 9090
When the operator starts the stub service on port 9090
Then HTTP clients can connect to http://localhost:9090
And requests to configured paths receive configured responses
```

**Example: Report that the service is running**

```gherkin
Given the stub service is running on port 9090
When the operator asks for the service status
Then the status indicates the service is running
And the status includes the base URL http://localhost:9090
```

### Rule: The service can be stopped cleanly

**Example: Stop releases the port**

```gherkin
Given the stub service is running on port 9090
When the operator stops the stub service
Then HTTP clients cannot connect to http://localhost:9090
And the status indicates the service is not running
```

### Rule: Only one listener may bind to a given port at a time

**Example: Second instance on same port is rejected**

```gherkin
Given the stub service is already running on port 9090
When the operator attempts to start another stub service on port 9090
Then the start attempt fails with a clear error
And the existing service on port 9090 continues to accept requests
```

---

## Scenario: Define stubs that map requests to predetermined responses

### Rule: A stub is identified by how incoming requests are matched

**Example: Match by HTTP method and path**

```gherkin
Given the stub service is running on port 9090
And a stub is configured for GET /payments/123 with response status 200 and body "paid"
When a client sends GET http://localhost:9090/payments/123
Then the client receives HTTP status 200
And the response body is "paid"
```

**Example: Different methods on the same path are distinct**

```gherkin
Given stubs are configured for GET /resource returning 200 and POST /resource returning 201
When a client sends POST http://localhost:9090/resource
Then the client receives HTTP status 201
When a client sends GET http://localhost:9090/resource
Then the client receives HTTP status 200
```

### Rule: Stubs can match query strings when specified

**Example: Match required query parameters**

```gherkin
Given a stub matches GET /search?q=hello with response body "results-for-hello"
When a client sends GET http://localhost:9090/search?q=hello
Then the client receives response body "results-for-hello"
When a client sends GET http://localhost:9090/search?q=world
Then the client receives HTTP status 404
And the response indicates no matching stub was found
```

### Rule: Stubs can match request headers when specified

**Example: Require an Authorization header**

```gherkin
Given a stub matches POST /orders with header Authorization: Bearer test-token and response status 201
When a client sends POST http://localhost:9090/orders with header Authorization: Bearer test-token
Then the client receives HTTP status 201
When a client sends POST http://localhost:9090/orders without header Authorization
Then the client receives HTTP status 404
And the response indicates no matching stub was found
```

### Rule: Stubs can match request body content when specified

**Example: Match JSON body**

```gherkin
Given a stub matches POST /webhook with body containing "event":"order.created" and response status 202
When a client sends POST http://localhost:9090/webhook with body {"event":"order.created"}
Then the client receives HTTP status 202
When a client sends POST http://localhost:9090/webhook with body {"event":"order.cancelled"}
Then the client receives HTTP status 404
And the response indicates no matching stub was found
```

### Rule: Each stub defines a complete HTTP response

**Example: Return status, headers, and body**

```gherkin
Given a stub for GET /profile returns status 200, header Content-Type: application/json, and body {"id":1}
When a client sends GET http://localhost:9090/profile
Then the client receives HTTP status 200
And the response includes header Content-Type: application/json
And the response body is {"id":1}
```

**Example: Return empty body**

```gherkin
Given a stub for DELETE /session/abc returns status 204 with no body
When a client sends DELETE http://localhost:9090/session/abc
Then the client receives HTTP status 204
And the response has an empty body
```

### Rule: Unmatched requests are observable failures for tests

**Example: No stub configured**

```gherkin
Given the stub service is running on port 9090
And no stub matches GET /unknown
When a client sends GET http://localhost:9090/unknown
Then the client receives HTTP status 404
And the response indicates no matching stub was found
```

### Rule: Stubs can be added, updated, and removed without restarting the whole suite when the service stays up

**Example: Add a stub while running**

```gherkin
Given the stub service is running on port 9090
When the operator adds a stub for GET /health returning status 200 and body "ok"
And a client sends GET http://localhost:9090/health
Then the client receives HTTP status 200 and body "ok"
```

**Example: Update changes behaviour for subsequent requests**

```gherkin
Given a stub for GET /rate returns status 200 and body "1.0"
When the operator updates that stub to return body "2.0"
And a client sends GET http://localhost:9090/rate
Then the client receives body "2.0"
```

**Example: Remove stops matching**

```gherkin
Given a stub exists for GET /temp
When the operator removes that stub
And a client sends GET http://localhost:9090/temp
Then the client receives HTTP status 404
And the response indicates no matching stub was found
```

---

## Scenario: Replicate realistic third-party behaviour beyond a single static response

### Rule: A stub can return different responses in a defined sequence

**Example: First call succeeds, second call fails (retry testing)**

```gherkin
Given a stub for POST /charge is configured with responses in order:
  | call | status |
  | 1    | 503    |
  | 2    | 200    |
When a client sends POST http://localhost:9090/charge
Then the client receives HTTP status 503
When the same client sends POST http://localhost:9090/charge again
Then the client receives HTTP status 200
```

**Example: After the sequence is exhausted, behaviour is explicit**

```gherkin
Given a stub for GET /status has a two-response sequence and then policy "repeat last"
When the client has already received both responses once
And the client sends GET http://localhost:9090/status again
Then the client receives the same response as the second call in the sequence
```

### Rule: A stub can introduce configurable response delay

**Example: Delay before responding**

```gherkin
Given a stub for GET /slow returns status 200 after a delay of 2 seconds
When a client sends GET http://localhost:9090/slow at time T0
Then the client receives HTTP status 200 no earlier than T0 + 2 seconds
```

### Rule: A stub can simulate connection-level or HTTP error behaviour

**Example: Return a server error status**

```gherkin
Given a stub for GET /broken returns status 500 and body "upstream error"
When a client sends GET http://localhost:9090/broken
Then the client receives HTTP status 500
And the response body is "upstream error"
```

**Example: Close connection without a complete response when configured**

```gherkin
Given a stub for GET /drop is configured to reset the connection without an HTTP response
When a client sends GET http://localhost:9090/drop
Then the client observes a connection reset or incomplete response
And no successful HTTP status line is received
```

---

## Scenario: Support path patterns for services with variable identifiers

### Rule: Stubs can match paths with placeholders

**Example: Single path segment variable**

```gherkin
Given a stub matches GET /users/{id} and returns status 200 with body "user:{id}"
When a client sends GET http://localhost:9090/users/42
Then the client receives HTTP status 200
And the response body is "user:42"
```

**Example: Multiple segments**

```gherkin
Given a stub matches GET /accounts/{accountId}/orders/{orderId} returning status 200
When a client sends GET http://localhost:9090/accounts/A1/orders/O9
Then the client receives HTTP status 200
```

### Rule: More specific stubs take precedence over general patterns when both could match

**Example: Exact path wins over pattern**

```gherkin
Given a stub for GET /users/99 returns body "special"
And a stub for GET /users/{id} returns body "generic"
When a client sends GET http://localhost:9090/users/99
Then the client receives body "special"
When a client sends GET http://localhost:9090/users/100
Then the client receives body "generic"
```

---

## Scenario: Record traffic for assertions in acceptance tests

### Rule: Every received request can be recorded when recording is enabled

**Example: Record method, path, headers, and body**

```gherkin
Given recording is enabled
And a stub exists for POST /callback returning status 200
When a client sends POST http://localhost:9090/callback with header X-Signature: abc and body "payload"
Then the operator can retrieve a recording that includes method POST, path /callback, header X-Signature: abc, and body "payload"
```

### Rule: Recordings are ordered by arrival time

**Example: Multiple requests preserve order**

```gherkin
Given recording is enabled
When a client sends GET http://localhost:9090/a
And then sends GET http://localhost:9090/b
Then the recordings list shows /a before /b
```

### Rule: Recordings can be cleared between tests

**Example: Reset recordings**

```gherkin
Given recordings exist from previous requests
When the operator clears all recordings
Then the recordings list is empty
And new requests produce new recordings starting from the first position
```

### Rule: Recordings can be filtered for test assertions

**Example: Filter by path**

```gherkin
Given recordings exist for GET /a and POST /b
When the operator requests recordings for path /b
Then only the POST /b recording is returned
```

---

## Scenario: Prepare and reset configuration for repeatable test runs

### Rule: The full stub configuration can be exported and imported

**Example: Export captures all stubs**

```gherkin
Given stubs exist for GET /one and POST /two
When the operator exports the configuration
Then the export includes both stubs with their match rules and responses
```

**Example: Import restores behaviour**

```gherkin
Given an exported configuration file from a previous environment
When the operator imports that configuration into a running stub service on port 9090
Then a client request that matched in the source environment receives the same status and body on port 9090
```

### Rule: Configuration can be reset to a known empty baseline

**Example: Clear all stubs and recordings**

```gherkin
Given stubs and recordings exist
When the operator resets configuration to empty
Then no stubs are defined
And no recordings remain
And unmatched requests receive HTTP status 404
```

### Rule: Invalid configuration is rejected without partial application

**Example: Reject stub with no response status**

```gherkin
Given the operator submits a new stub with a path but no response status
When the operator attempts to save the stub
Then the save fails with a clear validation error
And no change is applied to live behaviour
```

---

## Scenario: Operate the system through a lightweight management experience

### Rule: An operator can view all active stubs and the service status

**Example: List stubs**

```gherkin
Given stubs exist for GET /health and POST /pay
When the operator opens the management view
Then the operator sees both stubs listed with their match criteria and response summary
And the operator sees whether the HTTP listener is running and on which base URL
```

### Rule: An operator can create and edit stubs without hand-editing raw HTTP traffic

**Example: Create stub via management interface**

```gherkin
Given the stub service is running on port 9090
When the operator defines match GET /vat-check and response status 200 with body {"rate":20}
And the operator saves the stub
Then a client GET http://localhost:9090/vat-check receives status 200 and body {"rate":20}
```

### Rule: Management actions intended for automation expose the same outcomes as the UI

**Example: Configure via management API**

```gherkin
Given the stub service exposes a management API
When an automated test suite creates a stub for GET /token returning body "test-token" via the management API
Then a client GET http://localhost:9090/token receives body "test-token"
```

*(Whether management is UI-only, API-only, or both is a deployment choice; behaviour must be consistent across channels.)*

---

## Scenario: Use the double safely in CI and parallel test runs

### Rule: Each test run can target an isolated namespace of configuration when required

**Example: Isolated workspace**

```gherkin
Given workspace "checkout-tests" has stub GET /inventory returning body "in-stock"
And workspace "payment-tests" has stub GET /inventory returning body "out-of-stock"
When a client sends GET http://localhost:9090/inventory with header X-Stub-Workspace: checkout-tests
Then the client receives body "in-stock"
When a client sends the same request with header X-Stub-Workspace: payment-tests
Then the client receives body "out-of-stock"
```

*(If isolation is not used, a single shared configuration applies to all clients.)*

### Rule: The system does not call real third-party hosts for stubbed paths

**Example: No outbound dependency for matched stubs**

```gherkin
Given a stub handles GET /external-api/status
When a client sends GET http://localhost:9090/external-api/status
Then the client receives only the configured stub response
And the outcome does not depend on network reachability of any external hostname defined in the stub path
```

---

## Non-functional behavioural expectations (still observable)

| Concern | Observable expectation |
|--------|-------------------------|
| Startup time | From "start" to first successful HTTP response on a preconfigured stub completes within a limit agreed for CI (e.g. under 5 seconds on a reference machine). |
| Determinism | Same configuration and same sequence of client requests produce the same responses and recordings every time. |
| Transparency | Unmatched requests and validation failures return explicit, human-readable messages suitable for failing acceptance tests. |

---

## Out of scope (unless added in a later version)

- TLS certificate management beyond "listener accepts HTTPS" if offered.
- SOAP/gRPC non-HTTP protocols.
- Full traffic replay from production captures.
- Authentication of management UI (may be required in shared environments; not specified here).

---

This specification is sufficient for acceptance tests to be written against a single deployable **Stub Gateway**: configure paths and responses, send real HTTP requests from the system under test, assert on responses and optional request recordings, and reset between scenarios. Implementation choices (database, in-memory store, framework, UI framework) are intentionally omitted so that delivery can follow BDD examples as executable specifications.
