from gherkin3.parser import Parser
import yaml
import os


def process_feature(feature_filename):
    with open(feature_filename, 'r') as f:
        str = f.read()
    parser = Parser()
    feature = parser.parse(str)

    stepdefinitions_resource = "%s_stepdefinitions.robot" % feature['name']
    stepdefinitions_resource = stepdefinitions_resource.lower().replace(' ', '_')
    FIELD_SEP = "    "

    basedir = os.path.dirname(feature_filename)
    fn = feature['name'].lower().replace(' ', '_') + '.robot'
    out = open(os.path.join(basedir, fn), 'w')

    out.write("*** Settings ***\n")
    out.write(FIELD_SEP.join(["Resource", stepdefinitions_resource]) + '\n')
    out.write('\n')
    out.write("*** Test Cases ***\n")
    for scenario in feature['scenarioDefinitions']:
        print scenario['name']
        for step in scenario['steps']:
            out.write(FIELD_SEP + step['keyword'] + step['text'] + '\n')
        out.write('\n')

    print yaml.dump(feature)

process_feature("example/member_logon.feature")
