Feature: Examples

  As a tester
  I want to specify feature files and translate it to RobotFramework
  So I can use the best of both worlds

  Background: A background title
    Given some background stuff

  Scenario: Greeter
    Given a greeter
    When greeting the following persons:
      | Name  | Greeting   |
      | Joe   | Hello      |
      | Mary  | Hi, there! |
    Then the world is a better place

  Scenario: Bully Greeter
     Given a bully greeter
     When greeting the following persons:
      | Name  | Greeting   |
      | Pete  | Hi, there! |
    Then the world is getting a bit darker
