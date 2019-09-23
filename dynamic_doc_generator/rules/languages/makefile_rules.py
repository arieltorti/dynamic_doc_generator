import itertools

from dynamic_doc_generator.rules.languages.makefile_operators import extract_var, extract_default, default_var
from dynamic_doc_generator.rules.operators import (
    startswith_remove,
    times,
    bold_markdown,
    any_line,
    chain)
from dynamic_doc_generator.rules.rules import BaseRule


class CommentRule(BaseRule):
    name = 'comment'

    phases = [
        startswith_remove('#'),
    ]


class PhonyRule(BaseRule):
    name = 'phony'

    phases = [
        startswith_remove('# @TARGET: ', case_insensitive=True),
        times(startswith_remove('#'), -1),
        (startswith_remove('.PHONY: ', case_insensitive=True), bold_markdown),
    ]

    def to_output(self):
        return "{}: {}".format(*self.value[2], ' '.join(itertools.chain(self.value[0], self.value[1])))
        # return "{}: {}".format(self.value[-1], ' '.join(self.value[:-1]))


class EnvRule(BaseRule):
    name = 'env'

    def create_phases(self):
        self.phases = [
            startswith_remove('# @ENV: ', case_insensitive=True),
            times(startswith_remove('#'), -1),
            chain((any_line, extract_var), (extract_default, default_var))
        ]

    def to_output(self):
        return "{}: {}\n{}".format(self.value[2][0], ' '.join(itertools.chain(self.value[0], self.value[1])),
                                                              self.value[2][1])
