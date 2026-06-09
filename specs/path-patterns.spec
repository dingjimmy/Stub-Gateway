Feature: Support path patterns for services with variable identifiers

  Rule: Stubs can match paths with placeholders

    Example: Single path segment variable
      Given a stub matches GET /users/{id} and returns status 200 with body "user:{id}"
      When a client sends GET http://localhost:9090/users/42
      Then the client receives HTTP status 200
      And the response body is "user:42"

    Example: Multiple segments
      Given a stub matches GET /accounts/{accountId}/orders/{orderId} returning status 200
      When a client sends GET http://localhost:9090/accounts/A1/orders/O9
      Then the client receives HTTP status 200

  Rule: More specific stubs take precedence over general patterns when both could match

    Example: Exact path wins over pattern
      Given a stub for GET /users/99 returns body "special"
      And a stub for GET /users/{id} returns body "generic"
      When a client sends GET http://localhost:9090/users/99
      Then the client receives body "special"
      When a client sends GET http://localhost:9090/users/100
      Then the client receives body "generic"
