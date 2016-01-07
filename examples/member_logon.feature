Feature: Member logon

	A member should be able to logon with his member number and password

Scenario: User with correct credentials should be able to log on
    Given login page is shown
    And a user with name "123.456.789.0" and password "abcd" is entered
    When user submits credentials
    Then the dashboard page is shown

Scenario: User with no username should result in error
    Given login page is shown
    And a user with name "" and password "NOTEMPTY" is entered
    When user submits credentials
    Then the alert "Please fill out your Fresh & Honest Club number." is shown

Scenario: User with no password should result in error
    Given login page is shown
    And a user with name "123.456.789.0" and password "" is entered
    When user submits credentials
    Then the alert "Please fill out your password." is shown

Scenario: User with invalid username should result in error
    Given login page is shown
    And a user with name "99999999" and password "abcd" is entered
    When user submits credentials
    Then the alert "Invalid user-id or password." is shown

Scenario: User with invalid password should result in error
    Given login page is shown
    And a user with name "123.456.789.0" and password "xxxx" is entered
    When user submits credentials
    Then the alert "Invalid user-id or password." is shown
