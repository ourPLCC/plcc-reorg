from pytest import raises, mark, fixture
from typing import List

from ...load_rough_spec.parse_lines import Line
from .validate_syntactic_spec import ValidationError, validate_syntactic_spec
from ...parse_spec.parse_syntactic_spec import SyntacticRule, SyntacticSpec, Symbol, LhsNonTerminal


def test_empty_no_errors():
    syntacticSpec = makeSyntacticSpec([])
    errors = validate_syntactic_spec(syntacticSpec)
    assert len(errors) == 0


def test_None_no_errors():
    syntacticSpec = makeSyntacticSpec(None)
    errors = validate_syntactic_spec(syntacticSpec)
    assert len(errors) == 0


def makeSyntacticSpec(ruleList=None):
    return SyntacticSpec(ruleList)


def makeSyntacticRule(line: Line, lhs: LhsNonTerminal, rhsList: List[Symbol]):
    return SyntacticRule(line, lhs, rhsList)


def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)


def makeValidationError(line, message):
    return ValidationError(line, message)

def makeInvalidTerminalFormatError(rule):
    message = f"Invalid terminal format for rule: '{rule.line.str}' (must be all upper-case letters, numbers, and underscore and cannot start with a number) on line: {rule.line.number}"
    return makeValidationError(rule.line, message)
