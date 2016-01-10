from gherkin3.parser import Parser
import yaml

def dump_gherkin(gherkin_filename):
    with open(gherkin_filename, 'r') as f:
        str = f.read()
    parser = Parser()
    feature = parser.parse(str)

    print yaml.dump(feature)

dump_gherkin('examples/member_logon_with_examples.feature')
