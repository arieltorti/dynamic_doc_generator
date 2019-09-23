# -*- coding: utf-8 -*-

"""Console script for dynamic_doc_generator."""

import argparse
from dynamic_doc_generator import DocGenerator
from dynamic_doc_generator.rules.languages.makefile_rules import CommentRule, PhonyRule, EnvRule

AVAILABLE_RULES = {
    'Comment': CommentRule,
    'Phony': PhonyRule,
    'Env': EnvRule
}


# TODO: Add logic to handle many input files
# TODO: Add autodiscover of rules
# TODO: Add read config from file
def main():
    """Console script for dynamic_doc_generator."""
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='File to be parsed')
    parser.add_argument('-r', '--rules', required=True, action="append", help='Rules to use when parsing')
    parser.add_argument('-o', '--output', help='Output file, if not specified result will be output to stdout')

    args = parser.parse_args()

    rules = []
    for rule in args.rules:
        try:
            rules.append(AVAILABLE_RULES[rule])
        except KeyError:
            print('Rule {} doesnt exist'.format(rule))
            return 1

    dc = DocGenerator(rules, args.output)
    with open('../tests/test_files/makefile/{}Test'.format(args.input)) as f:
        dc.generate(f)

    return 0


if __name__ == "__main__":
    main()
