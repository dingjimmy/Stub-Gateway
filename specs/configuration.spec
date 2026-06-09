Feature: Prepare and reset configuration for repeatable test runs

  Rule: The full stub configuration can be exported and imported

    Example: Export captures all stubs
      Given stubs exist for GET /one and POST /two
      When the operator exports the configuration
      Then the export includes both stubs with their match rules and responses

    Example: Import restores behaviour
      Given an exported configuration file from a previous environment
      When the operator imports that configuration into a running stub service on port 9090
      Then a client request that matched in the source environment receives the same status and body on port 9090

  Rule: Configuration can be reset to a known empty baseline

    Example: Clear all stubs and recordings
      Given stubs and recordings exist
      When the operator resets configuration to empty
      Then no stubs are defined
      And no recordings remain
      And unmatched requests receive HTTP status 404

  Rule: Invalid configuration is rejected without partial application

    Example: Reject stub with no response status
      Given the operator submits a new stub with a path but no response status
      When the operator attempts to save the stub
      Then the save fails with a clear validation error
      And no change is applied to live behaviour
