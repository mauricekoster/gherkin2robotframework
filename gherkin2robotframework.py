from gherkin3.parser import Parser
import yaml
import os, re

FIELD_SEP = "    "
settings_lines = []
testcases_lines = []
keywords_lines = []

def process_gherkin(gherkin_filename):
    with open(gherkin_filename, 'r') as f:
        str = f.read()
    parser = Parser()
    feature = parser.parse(str)
    process_feature(feature)

    generate_robot_script(os.path.dirname(gherkin_filename), feature['name'])

def generate_robot_script(path, featurename):
    stepdefinitions_resource = "%s_stepdefinitions.robot" % featurename
    stepdefinitions_resource = stepdefinitions_resource.lower().replace(' ', '_')

    fn = featurename.lower().replace(' ', '_') + '.robot'
    with open(os.path.join(path, fn), 'w') as outfile:
        outfile.write("*** Settings ***\n")
        outfile.write(FIELD_SEP.join(["Resource", stepdefinitions_resource]) + '\n')
        for line in settings_lines:
            outfile.write(line + '\n')

        outfile.write('\n')

        outfile.write("*** Test Cases ***\n")
        for line in testcases_lines:
            outfile.write(line + '\n')
        outfile.write('\n')

        if keywords_lines:
            outfile.write("*** Keywords ***\n")
            for line in keywords_lines:
                outfile.write(line + '\n')
            outfile.write('\n')


def process_feature(feature):
    if feature['background']:
        process_background(feature)

    for scenario in feature['scenarioDefinitions']:
        process_scenario(scenario)

def process_background(feature):
    settings_lines.append(FIELD_SEP.join(['Test Setup','Background']))

    keywords_lines.append('Background')
    if feature['background']['name']:
        keywords_lines.append(FIELD_SEP.join(['','[Documentation]',feature['background']['name']]))

    for step in feature['background']['steps']:
        keywords_lines.append(FIELD_SEP + step['keyword'] + step['text'])
    keywords_lines.append('')

def process_scenario(scenario):
    print scenario['name']
    if scenario['type'] == 'Scenario':
        process_scenario_plain(scenario)

    elif scenario['type'] == 'ScenarioOutline':
        process_scenario_outline(scenario)

    else:
        print 'Unknown scenario step ' + scenario['name'] + '>' + scenario['type']

def process_scenario_plain(scenario):
    testcases_lines.append(scenario['name'])
    for step in scenario['steps']:
        testcases_lines.append(FIELD_SEP + step['keyword'] + step['text'])
    testcases_lines.append('')

def emptyfi(x):
    if x=='':
        return '${EMPTY}'
    else:
        return x

def process_scenario_outline(scenario):
    # collect variables in steps
    variables = []
    for step in scenario['steps']:
        v = re.findall('<([a-zA-Z0-9]+)>', step['text'])
        print step['text'], v
        variables += v
    variables = set(variables)
    print variables

    # per example a test case
    for example in scenario['examples']:
        if example['name']:
            testcasename = scenario['name'] + example['name']
        else:
            testcasename = scenario['name'] + ' example line ' + str(example['location']['line'])

        testcases_lines.append(testcasename)
        testcases_lines.append(FIELD_SEP.join(['', '[Template]', 'Scenario Outline ' + scenario['name']]))

        for example_row in example['tableBody']:
            args = [cell['value'] for cell in example_row['cells']]
            args = map(emptyfi, args)
            args.insert(0, '')
            testcases_lines.append(FIELD_SEP.join(args))

        testcases_lines.append('')



    # Test Template
    keywords_lines.append('Scenario Outline ' + scenario['name'])
    arguments = ['${' + arg + '}' for arg in variables]
    keywords_lines.append(FIELD_SEP.join(['', '[Arguments]'] + arguments))
    for step in scenario['steps']:
        keywords_lines.append(FIELD_SEP + step['keyword'] + step['text'].replace('<','${').replace('>','}'))
    keywords_lines.append('')



process_gherkin("examples/member_logon_with_examples.feature")
