# -*- coding: utf-8 -*-
from collections.abc import Iterable
import logging

from dynamic_doc_generator.rules.rules import State

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: Add optional rules, rules that may or may not be fulfilled
# TODO: Add common operations
# TODO: Add example use cases (Simple and complex)
# TODO: Change the way we store values for a more dynamic one
class Parser:
    def __init__(self, rules, *args, **kwargs):
        self.rules = rules
        self.rules = {
            'initial': rules,
            'active': [],
            'done': []
        }
        self.new_active_rules = []

        if not isinstance(self.rules, Iterable):
            raise ValueError("Rules object must be iterable")

    def parse(self, file):
        # TODO: Find a way to not repeat logic when creating new rules
        # TODO: and feeding lines to existing ones.

        for line in file:
            self.new_active_rules = []

            for rule in self.rules['active']:
                state = rule.next(line)

                if state == State.DONE:
                    self.rules['done'].append(rule)
                elif state == State.ACTIVE:
                    self.new_active_rules.append(rule)

            for rule in self.rules['initial']:
                instance = rule.create(line)

                if instance is not None:
                    if instance.state == State.DONE:
                        self.rules['done'].append(instance)
                    elif instance.state == State.ACTIVE:
                        self.new_active_rules.append(instance)

            self.rules['active'] = self.new_active_rules
        return self.rules['done']
