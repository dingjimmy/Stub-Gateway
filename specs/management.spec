Feature: Operate the system through a lightweight management experience

  Rule: An operator can view all active stubs and the service status

    Example: List stubs
      Given stubs exist for GET /health and POST /pay
      When the operator opens the management view
      Then the operator sees both stubs listed with their match criteria and response summary
      And the operator sees whether the HTTP listener is running and on which base URL

  Rule: An operator can create and edit stubs without hand-editing raw HTTP traffic

    Example: Create stub via management interface
      Given the stub service is running on port 9090
      When the operator defines match GET /vat-check and response status 200 with body {"rate":20}
      And the operator saves the stub
      Then a client GET http://localhost:9090/vat-check receives status 200 and body {"rate":20}

  Rule: Management actions intended for automation expose the same outcomes as the UI

    Example: Configure via management API
      Given the stub service exposes a management API
      When an automated test suite creates a stub for GET /token returning body "test-token" via the management API
      Then a client GET http://localhost:9090/token receives body "test-token"
