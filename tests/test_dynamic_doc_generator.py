#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dynamic_doc_generator` package."""

from dynamic_doc_generator import DocGenerator
from dynamic_doc_generator.rules.languages.makefile_rules import CommentRule, PhonyRule, EnvRule

# TODO: This are just PoC tests, we should create a large unit/integration tests suite.


def test_comment_extractor():
    dc = DocGenerator()
    dc.register_rule(CommentRule)
    rule_name = CommentRule.name

    with open("tests/test_files/makefile/CommentTest") as f:
        output = dc.generate(f)

    assert len(output[rule_name]) == 4
    assert output[rule_name] == ["A", "B", "C", "D"]


def test_phony_extractor():
    dc = DocGenerator()
    dc.register_rule(PhonyRule)
    rule_name = PhonyRule.name

    with open("tests/test_files/makefile/PhonyTest") as f:
        output = dc.generate(f)

    assert len(output[rule_name]) == 1
    assert output[rule_name][0] == "**valid**: A valid target"


def test_env_extractor():
    dc = DocGenerator()
    dc.register_rule(EnvRule)
    rule_name = EnvRule.name

    with open("tests/test_files/makefile/EnvTest") as f:
        output = dc.generate(f)

    assert len(output[rule_name]) == 1
    assert output[rule_name][0] == """**valid_variable**: A valid env variable. With some extra comment
Default: 456"""
