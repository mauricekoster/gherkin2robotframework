from gherkin3.parser import Parser
import yaml
import os, re
import argparse
import glob, fnmatch

# - Commandline parsing -------------------------------------------------------

cmdlineparser =  argparse.ArgumentParser()
cmdlineparser.add_argument("feature", nargs="?", default="")
cmdlineparser.add_argument("outputdir", nargs="?", default=".")
cmdline_args = cmdlineparser.parse_args()

# - Globals -------------------------------------------------------------------

FIELD_SEP = "    "
settings_lines = []
testcases_lines = []
keywords_lines = []
seen_steps = set([])

def process_gherkin(gherkin_filename, basedir, outputdir):
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

    feature_base = os.path.dirname(gherkin_filename)
    feature_sub = feature_base[len(basedir)+1:]
    generate_robot_script(os.path.join(outputdir, feature_sub), feature['name'])

def writetoscript(outfile, line):
    if type(line) is list:
        outfile.write(FIELD_SEP.join(line) + '\n')
    else:
        outfile.write(line + '\n')

def generate_robot_script(path, featurename):
    if not os.path.exists(path):
        os.makedirs(path)

    stepdefinitions_resource = "%s_stepdefinitions.robot" % featurename
    stepdefinitions_resource = stepdefinitions_resource.lower().replace(' ', '_')

    fn = featurename.lower().replace(' ', '_') + '.robot'
    with open(os.path.join(path, fn), 'w') as outfile:
        writetoscript(outfile, "*** Settings ***")
        writetoscript(outfile, ["Resource", stepdefinitions_resource])
        for line in settings_lines:
            writetoscript(outfile, line)

        writetoscript(outfile, '')

        writetoscript(outfile, "*** Test Cases ***")
        for line in testcases_lines:
            writetoscript(outfile, line)
        writetoscript(outfile, '')

        if keywords_lines:
            writetoscript(outfile, "*** Keywords ***")
            for line in keywords_lines:
                writetoscript(outfile, line)
            writetoscript(outfile, '')

    generate_robot_script_resource(path,stepdefinitions_resource)

def generate_robot_script_resource(path, stepdefinitions_resource):
    fn = os.path.join(path, stepdefinitions_resource)
    if os.path.exists(fn):
        print "existing file " + stepdefinitions_resource
    else:
        print "new file " + stepdefinitions_resource
        with open(fn, 'w') as f:
            writetoscript(f, '*** Settings ***')
            writetoscript(f, '*** Keywords ***')
            for l in seen_steps:
                writetoscript(f, l)
                writetoscript(f, ['','No Operation'])

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
        keywords_lines.append(['','[Documentation]',feature['background']['name']])

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
    text = step['text'].replace('<','${').replace('>','}')
    if step['keyword'] == '* ':
        keyword = text
    else:
        keyword = step['keyword'] + text
    seen_steps.add(text)
    output.append(['', keyword])

def process_scenario_plain(scenario):
    testcases_lines.append(scenario['name'])
    if background_available:
        testcases_lines.append(['','Background'])
    for step in scenario['steps']:
        add_step(testcases_lines, step)
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
        testcases_lines.append(['', '[Template]', 'Scenario Outline ' + scenario['name']])

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
            testcases_lines.append(args)

        testcases_lines.append('')

    # Test Template
    keywords_lines.append('Scenario Outline ' + scenario['name'])
    arguments = ['${' + arg + '}' for arg in variables]
    keywords_lines.append(['', '[Arguments]'] + arguments)
    if background_available:
        keywords_lines.append(['','Background'])
    for step in scenario['steps']:
        add_step(keywords_lines, step)
    keywords_lines.append('')

def get_feature_filenames(feature_basedir):
    matches = []
    for root, dirnames, filenames in os.walk(feature_basedir):
        for filename in fnmatch.filter(filenames, '*.feature'):
            matches.append(os.path.join(root, filename))
    return matches

def process_directory(d, outputdir):
    l = get_feature_filenames(d)
    for f in l:
        process_gherkin(f, d, outputdir)

if cmdline_args.feature:
    if os.path.isdir(cmdline_args.feature):
        # glob
        process_directory(cmdline_args.feature, cmdline_args.outputdir)
    else:
        process_gherkin(cmdline_args.feature, '.', cmdline_args.outputdir)
else:
    process_directory('.', '.')
