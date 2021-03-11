Feature: Examples

  As a tester
  I want to specify feature files and translate it to RobotFramework
  So I can use the best of both worlds

  Background:
    Given some background stuff

  Scenario: Greeter
    Given a greeter
    When greeting the following persons:
      | Name  | Greeting   |
      | Joe   | Hello      |
      | Mary  | Hi, there! |
    Then the wold is a better place
