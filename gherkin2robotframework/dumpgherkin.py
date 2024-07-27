from gherkin.parser import Parser

import yaml
import argparse


def dump_gherkin(gherkin_filename):
    with open(gherkin_filename, 'r') as f:
        content = f.read()
    parser = Parser()
    feature = parser.parse(content)

    print(yaml.dump(feature))


def main():
    cmdlineparser = argparse.ArgumentParser()
    cmdlineparser.add_argument("feature")
    cmdline_args = cmdlineparser.parse_args()
    dump_gherkin(cmdline_args.feature)


if __name__ == '__main__':
    main()
