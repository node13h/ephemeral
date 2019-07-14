Feature: Adding messages

  Scenario: User adds new message
    When a user submits a form with specific values and a CSRF token at the "/add" endpoint
      | body |    pin |
      | foo  | 123456 |

    Then the response status code is 200
    And the response contains a link

  Scenario: User omits the CSRF token
    When a user submits a form with specific values at the "/add" endpoint
      | body |    pin |
      | foo  | 123456 |

    Then the response status code is 403
    And the response does not contain a link

  Scenario: User omits the message
    When a user submits a form with specific values and a CSRF token at the "/add" endpoint
      |    pin |
      | 123456 |

    Then the response status code is 400
    And the response does not contain a link

  Scenario: User omits the PIN
    When a user submits a form with specific values and a CSRF token at the "/add" endpoint
      | body |
      | foo  |

    Then the response status code is 400
    And the response does not contain a link
