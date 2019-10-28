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

  @tag
  Scenario Outline: Repetitive stuff
    A nice description
    on multiple lines
    Given a thing with "<thingy>"
    When some action
    Then this happened: <stuff>

    @A
    Examples: A
      Documentation for
      example A
      | thingy  | stuff |
      | AAA     | 123   |
      | BBB     | 456   |

    @B
    Examples: B
      Documentation for example B
      | thingy  | stuff |
      | CCC     | 789   |
      | DDD     | 000   |
