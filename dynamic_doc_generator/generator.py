# -*- coding: utf-8 -*-

"""Main module."""
from collections import defaultdict

from dynamic_doc_generator.parser import Parser


# TODO: Add feature to append to file sections
# TODO: Add output to many formats
class DocGenerator:
    def __init__(self, rules=None, output=None, *args, **kwargs):
        if rules:
            self.rules = set(rules)
        else:
            self.rules = set()
        self.file_output = output

    def register_rule(self, rule):
        self.rules.add(rule)

    def generate(self, file, *args, **kwargs):
        parser = Parser(self.rules)
        output = parser.parse(file)

        generated_dict = defaultdict(list)
        for x in output:
            generated_dict[x.name].append(x.to_output())

        if self.file_output is None:
            print(' --- OUTPUT --- ')
            for rule, value in generated_dict.items():
                print("  -- {} --".format(rule))
                for v in value:
                    print("\t{}\n".format(v))
        else:
            with open(self.file_output, 'w+') as f:
                for rule, value in generated_dict.items():
                    f.write("## {}\n\n".format(rule.capitalize()))
                    for v in value:
                        f.write("{}\n\n".format(v))
        return generated_dict
