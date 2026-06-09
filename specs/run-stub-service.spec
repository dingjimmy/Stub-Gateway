Feature: Run the stub service for acceptance tests

  Rule: The service exposes a reachable HTTP endpoint for tests

    Example: Start listening on a chosen port
      Given no stub service is listening on port 9090
      When the operator starts the stub service on port 9090
      Then HTTP clients can connect to http://localhost:9090
      And requests to configured paths receive configured responses

    Example: Report that the service is running
      Given the stub service is running on port 9090
      When the operator asks for the service status
      Then the status indicates the service is running
      And the status includes the base URL http://localhost:9090

  Rule: The service can be stopped cleanly

    Example: Stop releases the port
      Given the stub service is running on port 9090
      When the operator stops the stub service
      Then HTTP clients cannot connect to http://localhost:9090
      And the status indicates the service is not running

  Rule: Only one listener may bind to a given port at a time

    Example: Second instance on same port is rejected
      Given the stub service is already running on port 9090
      When the operator attempts to start another stub service on port 9090
      Then the start attempt fails with a clear error
      And the existing service on port 9090 continues to accept requests
