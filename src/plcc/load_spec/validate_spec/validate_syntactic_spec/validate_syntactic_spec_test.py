from pytest import raises, mark, fixture

from ...load_rough_spec.parse_lines import Line
from .validate_syntactic_spec import ValidationError, validate_syntactic_spec
from ...parse_spec.parse_syntactic_spec import SyntacticRule, SyntacticSpec


def test_empty_no_errors():
    syntacticSpec = makeSyntacticSpec([])
    errors = validate_syntactic_spec(syntacticSpec)
    assert len(errors) == 0


def makeSyntacticSpec(ruleList=None):
    return SyntacticSpec(ruleList)


def makeSyntacticRule(line, lhs, rhs):
    return SyntacticRule(line, lhs, rhs)


def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)


def makeValidationError(line, message):
    return ValidationError(line, message)
