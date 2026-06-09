Feature: Define stubs that map requests to predetermined responses

  Rule: A stub is identified by how incoming requests are matched

    Example: Match by HTTP method and path
      Given the stub service is running on port 9090
      And a stub is configured for GET /payments/123 with response status 200 and body "paid"
      When a client sends GET http://localhost:9090/payments/123
      Then the client receives HTTP status 200
      And the response body is "paid"

    Example: Different methods on the same path are distinct
      Given stubs are configured for GET /resource returning 200 and POST /resource returning 201
      When a client sends POST http://localhost:9090/resource
      Then the client receives HTTP status 201
      When a client sends GET http://localhost:9090/resource
      Then the client receives HTTP status 200

  Rule: Stubs can match query strings when specified

    Example: Match required query parameters
      Given a stub matches GET /search?q=hello with response body "results-for-hello"
      When a client sends GET http://localhost:9090/search?q=hello
      Then the client receives response body "results-for-hello"
      When a client sends GET http://localhost:9090/search?q=world
      Then the client receives HTTP status 404
      And the response indicates no matching stub was found

  Rule: Stubs can match request headers when specified

    Example: Require an Authorization header
      Given a stub matches POST /orders with header Authorization: Bearer test-token and response status 201
      When a client sends POST http://localhost:9090/orders with header Authorization: Bearer test-token
      Then the client receives HTTP status 201
      When a client sends POST http://localhost:9090/orders without header Authorization
      Then the client receives HTTP status 404
      And the response indicates no matching stub was found

  Rule: Stubs can match request body content when specified

    Example: Match JSON body
      Given a stub matches POST /webhook with body containing "event":"order.created" and response status 202
      When a client sends POST http://localhost:9090/webhook with body {"event":"order.created"}
      Then the client receives HTTP status 202
      When a client sends POST http://localhost:9090/webhook with body {"event":"order.cancelled"}
      Then the client receives HTTP status 404
      And the response indicates no matching stub was found

  Rule: Each stub defines a complete HTTP response

    Example: Return status, headers, and body
      Given a stub for GET /profile returns status 200, header Content-Type: application/json, and body {"id":1}
      When a client sends GET http://localhost:9090/profile
      Then the client receives HTTP status 200
      And the response includes header Content-Type: application/json
      And the response body is {"id":1}

    Example: Return empty body
      Given a stub for DELETE /session/abc returns status 204 with no body
      When a client sends DELETE http://localhost:9090/session/abc
      Then the client receives HTTP status 204
      And the response has an empty body

  Rule: Unmatched requests are observable failures for tests

    Example: No stub configured
      Given the stub service is running on port 9090
      And no stub matches GET /unknown
      When a client sends GET http://localhost:9090/unknown
      Then the client receives HTTP status 404
      And the response indicates no matching stub was found

  Rule: Stubs can be added, updated, and removed without restarting the whole suite when the service stays up

    Example: Add a stub while running
      Given the stub service is running on port 9090
      When the operator adds a stub for GET /health returning status 200 and body "ok"
      And a client sends GET http://localhost:9090/health
      Then the client receives HTTP status 200 and body "ok"

    Example: Update changes behaviour for subsequent requests
      Given a stub for GET /rate returns status 200 and body "1.0"
      When the operator updates that stub to return body "2.0"
      And a client sends GET http://localhost:9090/rate
      Then the client receives body "2.0"

    Example: Remove stops matching
      Given a stub exists for GET /temp
      When the operator removes that stub
      And a client sends GET http://localhost:9090/temp
      Then the client receives HTTP status 404
      And the response indicates no matching stub was found
