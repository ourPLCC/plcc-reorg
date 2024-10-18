from pytest import raises, mark, fixture
from typing import List

from ...load_rough_spec.parse_lines import Line
from .validate_syntactic_spec import ValidationError, validate_syntactic_spec
from ...parse_spec.parse_syntactic_spec import (
    SyntacticRule,
    SyntacticSpec,
    Symbol,
    LhsNonTerminal,
    Terminal,
)
from .errors import (
    ValidationError,
    InvalidLhsNameError,
    InvalidLhsAltNameError,
    DuplicateLhsError,
)


def test_empty_no_errors():
    syntacticSpec = makeSyntacticSpec([])
    errors = validate_syntactic_spec(syntacticSpec)
    assert len(errors) == 0


def test_None_no_errors():
    syntacticSpec = makeSyntacticSpec(None)
    errors = validate_syntactic_spec(syntacticSpec)
    assert len(errors) == 0


def test_valid_line_no_errors():
    line = makeLine("<sentence> ::= WORD WORD WORD")
    terminal = makeTerminal("WORD")
    valid_spec = [
        makeSyntacticRule(
            line, makeLhsNonTerminal("sentence"), [terminal, terminal, terminal]
        )
    ]
    errors = validate_syntactic_spec(valid_spec)
    assert len(errors) == 0


def test_distinct_resolved_name():
    rule_1 = makeSyntacticRule(
        makeLine("<sentence>:Answer ::= VERB PERIOD"),
        makeLhsNonTerminal("sentence", "Answer"),
        [makeTerminal("VERB"), makeTerminal("PERIOD")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<sentence>:Question ::= WORD MARK"),
        makeLhsNonTerminal("sentence", "Question"),
        [makeTerminal("WORD"), makeTerminal("MARK")],
    )
    spec = [rule_1, rule_2]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 0


def test_valid_lhs_alt_name():
    line = makeLine("<sentence>:Name_Version_1 ::= WORD WORD WORD")
    terminal = makeTerminal("WORD")
    spec = [
        makeSyntacticRule(
            line,
            makeLhsNonTerminal("sentence", "Name_Version_1"),
            [terminal, terminal, terminal],
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 0


def test_number_lhs_terminal():
    line = makeLine("<1sentence> ::= WORD WORD WORD")
    terminal = makeTerminal("WORD")
    spec = [
        makeSyntacticRule(
            line, makeLhsNonTerminal("1sentence"), [terminal, terminal, terminal]
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsNameFormatError(spec[0])


def test_capital_lhs_terminal():
    line = makeLine("<Sentence> ::= WORD WORD WORD")
    terminal = makeTerminal("WORD")
    spec = [
        makeSyntacticRule(
            line, makeLhsNonTerminal("Sentence"), [terminal, terminal, terminal]
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsNameFormatError(spec[0])


def test_undercase_lhs_alt_name():
    line = makeLine("<sentence>:name ::= WORD WORD WORD")
    terminal = makeTerminal("WORD")
    spec = [
        makeSyntacticRule(
            line, makeLhsNonTerminal("sentence", "name"), [terminal, terminal, terminal]
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsAltNameFormatError(spec[0])


def test_underscore_lhs_alt_name():
    line = makeLine("<sentence>:_name ::= WORD WORD WORD")
    terminal = makeTerminal("WORD")
    spec = [
        makeSyntacticRule(
            line,
            makeLhsNonTerminal("sentence", "_name"),
            [terminal, terminal, terminal],
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsAltNameFormatError(spec[0])


def test_duplicate_lhs_name():
    rule_1 = makeSyntacticRule(
        makeLine("<sentence> ::= VERB PERIOD"),
        makeLhsNonTerminal("sentence"),
        [makeTerminal("VERB"), makeTerminal("PERIOD")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<sentence> ::= WORD MARK"),
        makeLhsNonTerminal("sentence"),
        [makeTerminal("WORD"), makeTerminal("MARK")],
    )
    spec = [rule_1, rule_2]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def test_duplicate_lhs_alt_name():
    rule_1 = makeSyntacticRule(
        makeLine("<sentence>:Name ::= VERB PERIOD"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("VERB"), makeTerminal("PERIOD")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<sentence>:Name ::= WORD MARK"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("WORD"), makeTerminal("MARK")],
    )
    spec = [rule_1, rule_2]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def test_duplicate_resolved_name():
    rule_1 = makeSyntacticRule(
        makeLine("<sentence>:Name ::= VERB PERIOD"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("VERB"), makeTerminal("PERIOD")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<name> ::= WORD MARK"),
        makeLhsNonTerminal("name"),
        [makeTerminal("WORD"), makeTerminal("MARK")],
    )
    spec = [rule_1, rule_2]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def makeSyntacticSpec(ruleList=None):
    return SyntacticSpec(ruleList)


def makeSyntacticRule(line: Line, lhs: LhsNonTerminal, rhsList: List[Symbol]):
    return SyntacticRule(line, lhs, rhsList)


def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)


def makeLhsNonTerminal(name: str | None, altName: str | None = None):
    return LhsNonTerminal(name, altName)


def makeTerminal(name: str | None):
    return Terminal(name)


def makeValidationError(line, message):
    return ValidationError(line, message)


def makeInvalidLhsNameFormatError(rule):
    return InvalidLhsNameError(rule)


def makeInvalidLhsAltNameFormatError(rule):
    return InvalidLhsAltNameError(rule)


def makeDuplicateLhsError(rule):
    return DuplicateLhsError(rule)
