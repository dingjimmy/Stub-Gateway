Feature: Use the double safely in CI and parallel test runs

  Rule: Each test run can target an isolated namespace of configuration when required

    Example: Isolated workspace
      Given workspace "checkout-tests" has stub GET /inventory returning body "in-stock"
      And workspace "payment-tests" has stub GET /inventory returning body "out-of-stock"
      When a client sends GET http://localhost:9090/inventory with header X-Stub-Workspace: checkout-tests
      Then the client receives body "in-stock"
      When a client sends the same request with header X-Stub-Workspace: payment-tests
      Then the client receives body "out-of-stock"

  Rule: The system does not call real third-party hosts for stubbed paths

    Example: No outbound dependency for matched stubs
      Given a stub handles GET /external-api/status
      When a client sends GET http://localhost:9090/external-api/status
      Then the client receives only the configured stub response
      And the outcome does not depend on network reachability of any external hostname defined in the stub path
