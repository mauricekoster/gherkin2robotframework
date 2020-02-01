# gherkin2robotframework

## Description

This tool can be used to facilitate the usage of Cucumber feature files in a RobotFramework Test Automation solution.
Although RobotFramework supports BDD style test cases, this support is limited to Given/When/Then keywords. 
Features like datatables and docstrings are not supported in RobotFramework.
This tool will 'compile' Gherkin feature files into RobotFramework test cases and scaffolding for step definitions 
aka User Keywords.

## Usage

### Example feature

```gherkin
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

```

### First time generation
After creating your feature files you can translate these into RobotFramework test scripts with the following command:

    gherkin2robotframework example.feature


Two files will be generated: *example.robot* containing the test cases and *example_step_definitions.robot* containing 
the user keywords implement the steps. For the default english gherkins the Given/When/Then will be stripped 
from the keyword names.

*example.robot*
```robotframework
*** Settings ***
Documentation    As a tester
...      I want to specify feature files and translate it to RobotFramework
...      So I can use the best of both worlds
Resource    ./examples_step_definitions.robot
Metadata    Feature    Examples
Metadata    Generated by    _gherkin2robotframework on 2020-01-31T13:23:34.958405_

*** Test Cases ***
Greeter
    Background
    Given a greeter
    ${DataTable}=    Create List
    FOR    ${Name}    ${Greeting}    IN
    ...    Joe    Hello
    ...    Mary    Hi, there!
        ${entry}=    Create Dictionary    Name=${Name}    Greeting=${Greeting}
        Append To List    ${DataTable}    ${entry}
    END
    When greeting the following persons:    @{DataTable}
    Then the wold is a better place

Repetitive stuff: A
    [Documentation]    Documentation for
    ...    example A
    [Tags]    tag    A
    [Template]    Scenario Outline Repetitive stuff
    AAA    123
    BBB    456

Repetitive stuff: B
    [Documentation]    Documentation for example B
    [Tags]    tag    B
    [Template]    Scenario Outline Repetitive stuff
    CCC    789
    DDD    000


*** Keywords ***
Background
    Given some background stuff

Scenario Outline Repetitive stuff
    [Documentation]    A nice description
    ...    on multiple lines
    [Arguments]    ${thingy}    ${stuff}
    Background
    Given a thing with "${thingy}"
    When some action
    Then this happened: ${stuff}

```

*example_step_definitions.robot*
```robotframework
*** Settings ***
Documentation    Generated by    _gherkin2robotframework on 2020-01-31T12:14:13.397524_
Library    Collections

*** Keywords ***
some background stuff
    Fail    Keyword "some background stuff" Not Implemented Yet

a greeter
    Fail    Keyword "a greeter" Not Implemented Yet

greeting the following persons:
    [Arguments]    @{DataTable}
    Fail    Keyword "greeting the following persons:" Not Implemented Yet

the wold is a better place
    Fail    Keyword "the wold is a better place" Not Implemented Yet

a thing with "${thingy}"
    Fail    Keyword "a thing with "${thingy}"" Not Implemented Yet

some action
    Fail    Keyword "some action" Not Implemented Yet

this happened: ${stuff}
    Fail    Keyword "this happened: ${stuff}" Not Implemented Yet

```

### Regeneration

In case your feature file is changed the .robot files needs to be regenerated.

```gherkin
...
    Scenario: Greeter
        Given a greeter
        When greeting the following persons:
          | Name  | Greeting   |
          | Joe   | Hello      |
          | Mary  | Hi, there! |
        Then the wold is a better place
        And the sun will shine                    #  <-- New step
...

```

The files can be regenerated with the same command:

    gherkin2robotframework example.feature


However, only the example.robot file will be generated (overwritten). The step definition will be parsed and 
missing keywords will be generated to the console. 

```
Processing gherkin: E:\GitHubProjects\gherkin2robotframework\examples\examples.feature

Missing keywords for: E:\GitHubProjects\gherkin2robotframework\examples\examples_step_definitions.robot

the sun will shine
    Fail    Keyword "the sun will shine" Not Implemented Yet

```

## Limitations and considerations

### Background support
The `Background` keyword is generated to implement the background part of the feature file. Each test case will
include this keyword. Using `[Test setup]` will not work for `Scenario Outline` with Examples.
In Cucumber the Background is applied to each example and in RobotFramework the `[Test setup]` is only applied to 
the Test case and *NOT* to each line in the test case with `[Test Template]`.

### Language support

`#language:xx` is supported, but because the gherkin3 dependency is not recently updated on PyPI. 
Therefore some keywords (and aliases) are not included.
