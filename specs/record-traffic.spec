Feature: Record traffic for assertions in acceptance tests

  Rule: Every received request can be recorded when recording is enabled

    Example: Record method, path, headers, and body
      Given recording is enabled
      And a stub exists for POST /callback returning status 200
      When a client sends POST http://localhost:9090/callback with header X-Signature: abc and body "payload"
      Then the operator can retrieve a recording that includes method POST, path /callback, header X-Signature: abc, and body "payload"

  Rule: Recordings are ordered by arrival time

    Example: Multiple requests preserve order
      Given recording is enabled
      When a client sends GET http://localhost:9090/a
      And then sends GET http://localhost:9090/b
      Then the recordings list shows /a before /b

  Rule: Recordings can be cleared between tests

    Example: Reset recordings
      Given recordings exist from previous requests
      When the operator clears all recordings
      Then the recordings list is empty
      And new requests produce new recordings starting from the first position

  Rule: Recordings can be filtered for test assertions

    Example: Filter by path
      Given recordings exist for GET /a and POST /b
      When the operator requests recordings for path /b
      Then only the POST /b recording is returned
