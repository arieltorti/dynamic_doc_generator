# -*- coding: utf-8 -*-
import itertools
from collections import defaultdict
from collections.abc import Iterable

from dynamic_doc_generator.rules.exceptions import InvalidRule, DoneRule
from dynamic_doc_generator.state import State


class BaseRule:
    InvalidRule = InvalidRule
    DoneRule = DoneRule

    def __init__(self):
        phases = getattr(self, 'phases', None)
        if phases is None:
            create_phases = getattr(self, 'create_phases', None)
            if create_phases is None:
                raise ValueError('`phases` attributes must be set in order for Rules to work.')
            create_phases()

        name = getattr(self, 'name', None)
        if name is None:
            raise ValueError('Rules must have a `name` attribute')

        _phases = []
        for phase in self.phases:
            if isinstance(phase, BaseRule):
                _phases.extend(phase.phases)
            else:
                _phases.append(phase)

        self.phases = _phases
        self.current_phase = 0

        self.state = State.ACTIVE
        self.value = defaultdict(list)

        verbose_name = getattr(self, 'verbose_name', None)
        if verbose_name is None:
            self.verbose_name = self.name

    def next(self, line, *args, **kwargs):
        try:
            value = self._run_next(line, *args, **kwargs)
            if value is not None:
                self.add_value(value)
            self.check_next_is_done()
        except InvalidRule:
            self.set_invalid()
        except DoneRule:
            pass
        return self.state

    def check_next_is_done(self):
        # If we are in the last phase and succeeded then mark the rule as done.
        if len(self.phases) <= self.current_phase and self.state == State.ACTIVE:
            self.set_done()

    def set_done(self):
        self.state = State.DONE

    def set_invalid(self):
        self.state = State.INVALID

    def set_active(self):
        self.state = State.ACTIVE

    def add_value(self, value):
        # Append value to the current phase
        # TODO: It may not be current_phase - 1, maybe an operator changed
        # TODO: the current_phase and we will be wreaking havoc
        # TODO: maybe we can use some kind of label
        self.value[self.current_phase-1].append(value)

    def to_output(self):
        return ''.join(*itertools.chain(self.value.values()))

    def _run_next(self, line, *args, **kwargs):
        func = self._get_next_func()

        # Advance phase in case condition doesn't
        self.current_phase += 1

        return self._execute_func(func, line, *args, **kwargs)

    def _get_next_func(self):
        try:
            func = self.phases[self.current_phase]
        except IndexError:
            # A condition may have advanced the current_phase to much
            # and produced an IndexError
            self.set_done()
            raise DoneRule()
        return func

    def _execute_func(self, func, line, *args, **kwargs):
        if isinstance(func, Iterable):
            func, *modifiers = func

            # Chain modifiers
            value = func(line, self, *args, **kwargs)
            for modifier in modifiers:
                value = modifier(value, self, *args, **kwargs)
        else:
            value = func(line, self, *args, **kwargs)
        return value

    @classmethod
    def create(cls, line, *args, **kwargs):
        instance = cls()
        instance.next(line)
        return instance
