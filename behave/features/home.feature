Feature: Home

  Scenario: User opens home page
    When a user makes a request to get the "/" endpoint
    Then the response status code is 200
    And the response contains "Ephemeral"
