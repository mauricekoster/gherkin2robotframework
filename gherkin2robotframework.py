from gherkin3.parser import Parser
import os
import re
import argparse
import fnmatch

# - Commandline parsing -------------------------------------------------------

cmdline_parser = argparse.ArgumentParser()
cmdline_parser.add_argument("feature", nargs="?", default="")
cmdline_parser.add_argument("output", nargs="?", default=".")
cmdline_args = cmdline_parser.parse_args()

# - Globals -------------------------------------------------------------------

FIELD_SEP = "    "
settings_lines = []
test_cases_lines = []
keywords_lines = []
seen_steps = set([])


def process_gherkin(gherkin_filename, basedir, output):
    with open(gherkin_filename, 'r') as f:
        content = f.read()
    parser = Parser()
    feature = parser.parse(content)
    global settings_lines, test_cases_lines, keywords_lines, seen_steps
    settings_lines = []
    test_cases_lines = []
    keywords_lines = []
    seen_steps = set([])

    process_feature(feature)

    feature_base = os.path.dirname(gherkin_filename)
    feature_sub = feature_base[len(basedir)+1:]
    generate_robot_script(os.path.join(output, feature_sub), feature['name'])


def write_to_script(outfile, line):
    if type(line) is list:
        outfile.write(FIELD_SEP.join(line) + '\n')
    else:
        outfile.write(line + '\n')


def generate_robot_script(path, feature_name):
    if not os.path.exists(path):
        os.makedirs(path)

    step_definitions_resource = "%s_step_definitions.robot" % feature_name
    step_definitions_resource = step_definitions_resource.lower().replace(' ', '_')

    fn = feature_name.lower().replace(' ', '_') + '.robot'
    with open(os.path.join(path, fn), 'w') as outfile:
        write_to_script(outfile, "*** Settings ***")
        write_to_script(outfile, ["Resource", step_definitions_resource])
        for line in settings_lines:
            write_to_script(outfile, line)

        write_to_script(outfile, '')

        write_to_script(outfile, "*** Test Cases ***")
        for line in test_cases_lines:
            write_to_script(outfile, line)
        write_to_script(outfile, '')

        if keywords_lines:
            write_to_script(outfile, "*** Keywords ***")
            for line in keywords_lines:
                write_to_script(outfile, line)
            write_to_script(outfile, '')

    generate_robot_script_resource(path, step_definitions_resource)


def generate_robot_script_resource(path, step_definitions_resource):
    fn = os.path.join(path, step_definitions_resource)
    if os.path.exists(fn):
        print "existing file " + step_definitions_resource
    else:
        print "new file " + step_definitions_resource
        with open(fn, 'w') as f:
            write_to_script(f, '*** Settings ***')
            write_to_script(f, '*** Keywords ***')
            for l in seen_steps:
                write_to_script(f, l)
                write_to_script(f, ['', 'No Operation'])

    print seen_steps


def process_feature(feature):
    global background_available
    background_available = False
    if 'background' in feature:
        process_background(feature)

    for scenario in feature['scenarioDefinitions']:
        process_scenario(scenario)


def process_background(feature):
    global background_available
    background_available = True

    keywords_lines.append('Background')
    if feature['background']['name']:
        keywords_lines.append(['', '[Documentation]', feature['background']['name']])

    for step in feature['background']['steps']:
        add_step(keywords_lines, step)
    keywords_lines.append('')


def process_scenario(scenario):
    if scenario['type'] == 'Scenario':
        process_scenario_plain(scenario)

    elif scenario['type'] == 'ScenarioOutline':
        process_scenario_outline(scenario)

    else:
        print 'Unknown scenario step ' + scenario['name'] + '>' + scenario['type']


def add_step(output, step):
    text = step['text'].replace('<', '${').replace('>', '}')
    if step['keyword'] == '* ':
        keyword = text
    else:
        keyword = step['keyword'] + text
    seen_steps.add(text)
    output.append(['', keyword])


def process_scenario_plain(scenario):
    test_cases_lines.append(scenario['name'])
    if background_available:
        test_cases_lines.append(['', 'Background'])
    for step in scenario['steps']:
        add_step(test_cases_lines, step)
    test_cases_lines.append('')


def make_empty(x):
    if x == '':
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

    # per example a test case
    for example in scenario['examples']:
        if example['name']:
            test_case_name = scenario['name'] + ': ' + example['name']
        else:
            test_case_name = scenario['name'] + ' example line ' + str(example['location']['line'])

        test_cases_lines.append(test_case_name)
        test_cases_lines.append(['', '[Template]', 'Scenario Outline ' + scenario['name']])

        header_col = {}
        col_nr = 0

        for header_cell in example['tableHeader']['cells']:
            v = header_cell['value']
            header_col[v] = col_nr
            col_nr += 1

        for example_row in example['tableBody']:
            args = []
            for a in variables:
                args.append(example_row['cells'][header_col[a]]['value'])

            args = map(make_empty, args)
            args.insert(0, '')
            test_cases_lines.append(args)

        test_cases_lines.append('')

    # Test Template
    keywords_lines.append('Scenario Outline ' + scenario['name'])
    arguments = ['${' + arg + '}' for arg in variables]
    keywords_lines.append(['', '[Arguments]'] + arguments)
    if background_available:
        keywords_lines.append(['', 'Background'])
    for step in scenario['steps']:
        add_step(keywords_lines, step)
    keywords_lines.append('')


def get_feature_filenames(feature_basedir):
    matches = []
    for root, dirnames, filenames in os.walk(feature_basedir):
        for filename in fnmatch.filter(filenames, '*.feature'):
            matches.append(os.path.join(root, filename))
    return matches


def process_directory(d, output_dir):
    l = get_feature_filenames(d)
    for f in l:
        process_gherkin(f, d, output_dir)

# --------------------------------------------------------------------------------------
# Main part
# --------------------------------------------------------------------------------------

if cmdline_args.feature:
    if os.path.isdir(cmdline_args.feature):
        # glob
        process_directory(cmdline_args.feature, cmdline_args.output)
    else:
        process_gherkin(cmdline_args.feature, '.', cmdline_args.output)
else:
    process_directory('.', '.')
