Feature: Examples

  As a tester
  I want to specify feature files and translate it to RobotFramework
  So I can use the best of both worlds

  Background: A background title
    Given some background stuff


  Scenario: Salutation
    Given a greeter
    When the greeting "Hello World!" is heard
    Then the world smiles

  Scenario: Boring speech
    Given a boring greeter
    When the greeting in form of the following speech is heard
       """
       Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris scelerisque est et ligula bibendum, vitae rutrum neque tristique. 
       Quisque sit amet magna rutrum, maximus diam et, feugiat nibh. Ut tincidunt libero nunc, ut convallis magna maximus id. 
       Cras sit amet ornare nibh, ac suscipit orci. Nunc ut placerat augue, finibus venenatis urna. Ut eget faucibus nisl. 
       Duis non orci quis sapien auctor efficitur. Donec dapibus molestie magna, eu volutpat nulla. 
       In eleifend enim tortor, et aliquam sapien tincidunt ut.
       """
    Then the world is getting very bored

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
