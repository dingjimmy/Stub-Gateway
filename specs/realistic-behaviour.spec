Feature: Replicate realistic third-party behaviour beyond a single static response

  Rule: A stub can return different responses in a defined sequence

    Scenario: First call fails then succeeds for retry testing
      Given a stub for POST /charge is configured with responses in order:
        | call | status |
        | 1    | 503    |
        | 2    | 200    |
      When a client sends POST http://localhost:9090/charge
      Then the client receives HTTP status 503
      When the same client sends POST http://localhost:9090/charge again
      Then the client receives HTTP status 200

    Scenario: After the sequence is exhausted behaviour follows policy
      Given a stub for GET /status has a two-response sequence and then policy "repeat last"
      When the client has already received both responses once
      And the client sends GET http://localhost:9090/status again
      Then the client receives the same response as the second call in the sequence

  Rule: A stub can introduce configurable response delay

    Scenario: Delay before responding
      Given a stub for GET /slow returns status 200 after a delay of 2 seconds
      When a client sends GET http://localhost:9090/slow at time T0
      Then the client receives HTTP status 200 no earlier than T0 + 2 seconds

  Rule: A stub can simulate connection-level or HTTP error behaviour

    Scenario: Return a server error status
      Given a stub for GET /broken returns status 500 and body "upstream error"
      When a client sends GET http://localhost:9090/broken
      Then the client receives HTTP status 500
      And the response body is "upstream error"

    Scenario: Close connection without a complete response when configured
      Given a stub for GET /drop is configured to reset the connection without an HTTP response
      When a client sends GET http://localhost:9090/drop
      Then the client observes a connection reset or incomplete response
      And no successful HTTP status line is received
