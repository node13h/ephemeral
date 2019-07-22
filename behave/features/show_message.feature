Feature: Reading messages

  Scenario: User opens a pin form with invalid message id
    When a user makes a request to get the "/show/INVALID" endpoint
    Then the response status code is 200
    And the response contains a form

  Scenario: User opens a pin form
    Given a user has submitted a message "foo" with pin "123456"
    When a user opens a URL returned by the message submit step
    Then the response status code is 200
    And the response contains a form

  Scenario: User opens a message
    Given a user has submitted a message "foo" with pin "123456"
    When a user submits a form with specific values and a CSRF token at the returned URL
      |    pin |
      | 123456 |

     Then the response status code is 200
      And the response contains "foo"

  Scenario: User opens a message twice
    Given a user has submitted a message "foo" with pin "123456"
    When a user submits a form with specific values and a CSRF token at the returned URL
      |    pin |
      | 123456 |

    And a user submits a form with specific values and a CSRF token at the returned URL
      |    pin |
      | 123456 |

     Then the response status code is 404
      And the response does not contain "foo"

  Scenario: User uses an invalid PIN
    Given a user has submitted a message "foo" with pin "123456"
    When a user submits a form with specific values and a CSRF token at the returned URL
      |    pin |
      | 000000 |

     Then the response status code is 200
      And the response does not contain "foo"

  Scenario: User omits the CSRF token
    Given a user has submitted a message "foo" with pin "123456"
    When a user submits a form with specific values at the returned URL
      |    pin |
      | 123456 |

    Then the response status code is 403
    And the response does not contain "foo"
