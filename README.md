# gherkin2robotframework

## Description

This tool can be used to facilitate the usage of Cucumber feature files in a RobotFramework Test Automation solution.
Although RobotFramework supports BDD style test cases, this support is limited to Given/When/Then keywords. 
Features like datatables and docstrings are not supported in RobotFramework.
This tool will 'compile' Gherkin feature files into RobotFramework test cases and scaffolding for step definitions 
aka User Keywords.

## Usage

### First time generation
TBD

### Regeneration
TBD

## Limitations and considerations

### Background support
The `Background` keyword is generated to implement the background part of the feature file. Each test case will
include this keyword. Using `[Test setup]` will not work for `Scenario Outline` with Examples.
In Cucumber the Background is applied to each example and in RobotFramework the `[Test setup]` is only applied to 
the Test case and *NOT* to each line in the test case with `[Test Template]`.

### Language support

`#language:xx` is supported, but because the gherkin3 dependency is not recently updated on PyPI. 
Therefore some keywords (and aliases) are not included.
