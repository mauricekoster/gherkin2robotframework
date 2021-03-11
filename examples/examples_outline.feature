Feature: Examples outline

  As a tester
  I want to specify feature files and translate it to RobotFramework
  So I can use the best of both worlds

  Background:
    Given some background stuff


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

  @tag
  Scenario Outline: More stuff
    A nice description
    on multiple lines
    Given a thing with "<thingy>"
    When some action doing action <action>
    Then this happened: <stuff>

    @A
    Examples: A
      Documentation for
      example A
      | thingy  | action | stuff |
      | AAA     | take   | 123   |
      | BBB     | give   | 456   |