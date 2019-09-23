import re

from dynamic_doc_generator.rules.exceptions import InvalidRule


def extract_default(line, instance):
    default_assign = "?="

    if default_assign in line:
        regex_assign = re.escape(default_assign)
        match = re.match(".*{}\s(.*)".format(regex_assign), line)

        if match is None:
            raise InvalidRule
        return match.group(1)
    else:
        raise InvalidRule


def extract_var(value, instance):
    words = value.split()
    var_name = words[0]

    if words[0] == "export":
        var_name = words[1]
    return "**{}**".format(var_name)


def default_var(value, instance):
    return "Default: `{}`".format(value)
