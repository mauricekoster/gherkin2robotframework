# language: en
Feature: Member logon with examples

	A member should be able to logon with his member number and password

Background: Open the login page
		Given login page is shown

Scenario: User with correct credentials should be able to log on

    This is the happy flow

    Given a user with name "123.456.789.0" and password "abcd" is entered
    When user submits credentials
    Then the dashboard page is shown

Scenario Outline: Invalid user credentials should result in error
    Given a user with name "<username>" and password "<password>" is entered
    When user submits credentials
    Then the alert "<message>" is shown

	Examples: Empty values
		| username      | password          | message                                               |
		|               | NONEMPTY          | Please fill out your Fresh & Honest Club number.      |
		| 123.456.789.0 |                   | Please fill out your password.                        |

  Examples: Invalid values
  	| username      | password          | message                                               |  x  |
		| 99999999      | abcd              | Invalid user-id or password.                          |  1  |
    | 123.456.789.0 | xxxx              | Invalid user-id or password.                          |  2  |
