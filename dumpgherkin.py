from gherkin3.parser import Parser
import yaml
import argparse

cmdlineparser =  argparse.ArgumentParser()
cmdlineparser.add_argument("feature")
cmdline_args = cmdlineparser.parse_args()
print cmdline_args

def dump_gherkin(gherkin_filename):
    with open(gherkin_filename, 'r') as f:
        str = f.read()
    parser = Parser()
    feature = parser.parse(str)

    print yaml.dump(feature)

dump_gherkin(cmdline_args.feature)
