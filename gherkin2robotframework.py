from gherkin3.parser import Parser
import yaml
import os, re
import argparse
import glob, fnmatch

# - Commandline parsing -------------------------------------------------------

cmdlineparser =  argparse.ArgumentParser()
cmdlineparser.add_argument("feature", nargs="?", default="")
cmdline_args = cmdlineparser.parse_args()
print cmdline_args

# - Globals -------------------------------------------------------------------

FIELD_SEP = "    "
settings_lines = []
testcases_lines = []
keywords_lines = []
seen_steps = set([])

def process_gherkin(gherkin_filename):
    with open(gherkin_filename, 'r') as f:
        str = f.read()
    parser = Parser()
    feature = parser.parse(str)
    global settings_lines, testcases_lines, keywords_lines, seen_steps
    settings_lines = []
    testcases_lines = []
    keywords_lines = []
    seen_steps = set([])

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
    if 'background' in feature:
        process_background(feature)

    for scenario in feature['scenarioDefinitions']:
        process_scenario(scenario)

def process_background(feature):
    settings_lines.append(FIELD_SEP.join(['Test Setup','Background']))

    keywords_lines.append('Background')
    if feature['background']['name']:
        keywords_lines.append(FIELD_SEP.join(['','[Documentation]',feature['background']['name']]))

    for step in feature['background']['steps']:
        if step['keyword'] == '* ':
            keyword = step['text']
        else:
            keyword = step['keyword'] + step['text']
        keywords_lines.append(FIELD_SEP.join(['', keyword]))
    keywords_lines.append('')

def process_scenario(scenario):
    if scenario['type'] == 'Scenario':
        process_scenario_plain(scenario)

    elif scenario['type'] == 'ScenarioOutline':
        process_scenario_outline(scenario)

    else:
        print 'Unknown scenario step ' + scenario['name'] + '>' + scenario['type']

def process_scenario_plain(scenario):
    testcases_lines.append(scenario['name'])
    for step in scenario['steps']:
        if step['keyword'] == '* ':
            keyword = step['text']
        else:
            keyword = step['keyword'] + step['text']
        testcases_lines.append(FIELD_SEP.join(['', keyword]))
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
        variables += v
    variables = set(variables)

    example_data = {}

    # per example a test case
    for example in scenario['examples']:
        if example['name']:
            testcasename = scenario['name'] + ': '+ example['name']
        else:
            testcasename = scenario['name'] + ' example line ' + str(example['location']['line'])

        testcases_lines.append(testcasename)
        testcases_lines.append(FIELD_SEP.join(['', '[Template]', 'Scenario Outline ' + scenario['name']]))

        header_col = {}
        colnr = 0
        for header_cell in example['tableHeader']['cells']:
            v = header_cell['value']
            header_col[v] = colnr
            colnr += 1


        for example_row in example['tableBody']:
            args = []
            for a in variables:
                args.append(example_row['cells'][header_col[a]]['value'])

            args = map(emptyfi, args)
            args.insert(0, '')
            testcases_lines.append(FIELD_SEP.join(args))

        testcases_lines.append('')



    # Test Template
    keywords_lines.append('Scenario Outline ' + scenario['name'])
    arguments = ['${' + arg + '}' for arg in variables]
    keywords_lines.append(FIELD_SEP.join(['', '[Arguments]'] + arguments))
    for step in scenario['steps']:
        if step['keyword'] == '* ':
            keyword = step['text']
        else:
            keyword = step['keyword'] + step['text']
        keyword = keyword.replace('<','${').replace('>','}')
        keywords_lines.append(FIELD_SEP.join(['', keyword]))
    keywords_lines.append('')

def get_feature_filenames(feature_basedir):
    matches = []
    for root, dirnames, filenames in os.walk(feature_basedir):
        for filename in fnmatch.filter(filenames, '*.feature'):
            matches.append(os.path.join(root, filename))
    return matches

def process_directory(d):
    l = get_feature_filenames(d)
    for f in l:
        print f
        process_gherkin(f)

if cmdline_args.feature:
    if os.path.isdir(cmdline_args.feature):
        # glob
        process_directory(cmdline_args.feature)
    else:
        process_gherkin(cmdline_args.feature)
else:
    process_directory('.')
