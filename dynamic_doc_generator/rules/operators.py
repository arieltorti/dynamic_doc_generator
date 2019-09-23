# -*- coding: utf-8 -*-
import re

from dynamic_doc_generator.rules.exceptions import InvalidRule


def startswith(prefix, *args, **kwargs):
    remove = kwargs.pop('remove', False)
    case_insensitive = kwargs.pop('case_insensitive', False)

    def _startswith(line, instance, **kwargs):
        if case_insensitive:
            # Using regex is faster than using lower, it's also more flexible, for example
            # prefix AaA will match when using regex while lower will not.
            valid = bool(re.match(prefix, line, re.I))
        else:
            valid = line.startswith(prefix)

        if valid:
            if remove:
                value = line[len(prefix):].strip()
            else:
                value = line
            return value
        raise InvalidRule()
    return _startswith


def startswith_remove(prefix, *args, **kwargs):
    return startswith(prefix, remove=True, *args, **kwargs)


def bold_markdown(value, instance):
    return "**{}**".format(value)


def times(func, n):
    remaining_times = n

    def _times(line, instance, *args, **kwargs):
        nonlocal remaining_times
        try:
            value = func(line, instance, *args, **kwargs)
            # In case it's valid we lower the counter and either
            # move the func pointer back to us or don't do anything and
            # the parser will move it to the next
            if remaining_times == -1:
                # TODO: This could be wrong, we need to find out which phase we are in
                instance.current_phase -= 1
            elif remaining_times > 1:
                remaining_times -= 1
                instance.current_phase -= 1
        except InvalidRule as e:
            if remaining_times != -1 and remaining_times >= 1:
                raise e

            if remaining_times == -1:
                return instance._run_next(line)
        return value
    return _times


def any_line(line, instance):
    return line


def chain(*funcs):
    def _chain(line, instance, *args, **kwargs):
        for func in funcs:
            value = instance._execute_func(func, line, *args, **kwargs)
            instance.add_value(value)
        return None
    return _chain
