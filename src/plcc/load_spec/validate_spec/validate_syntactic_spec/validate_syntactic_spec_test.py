from typing import List
from ...load_rough_spec.parse_lines import Line
from .validate_syntactic_spec import validate_syntactic_spec
from ...parse_spec.parse_lexical_spec import LexicalRule, LexicalSpec
from ...parse_spec.parse_syntactic_spec import (
    SyntacticRule,
    SyntacticSpec,
    Symbol,
    LhsNonTerminal,
    Terminal,
    RhsNonTerminal,
)
from .errors import (
    InvalidLhsNameError,
    InvalidRhsNameError,
    InvalidLhsAltNameError,
    InvalidRhsAltNameError,
    InvalidRhsTerminalError,
    DuplicateLhsError,
    UndefinedTerminalError,
)


def test_empty_no_errors():
    syntacticSpec = makeSyntacticSpec([])
    errors = validate(syntacticSpec)
    assert len(errors) == 0


def test_None_no_errors():
    syntacticSpec = makeSyntacticSpec(None)
    errors = validate(syntacticSpec)
    assert len(errors) == 0


def test_valid_line_no_errors():
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([word])
    valid_line = makeLine("<sentence> ::= WORD")
    spec = [
            makeSyntacticRule(
                valid_line, makeLhsNonTerminal("sentence"), [makeTerminal("WORD")]
            )
        ]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 0


def test_distinct_resolved_name():
    verb = makeLexicalRule(name="VERB", pattern="VERB")
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([verb, word])
    line_answer = makeSyntacticRule(
        makeLine("<sentence>:Answer ::= VERB"),
        makeLhsNonTerminal("sentence", "Answer"),
        [makeTerminal("VERB")],
    )
    line_question = makeSyntacticRule(
        makeLine("<sentence>:Question ::= WORD"),
        makeLhsNonTerminal("sentence", "Question"),
        [makeTerminal("WORD")],
    )
    spec = [line_answer, line_question]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 0


def test_valid_lhs_alt_name():
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([word])
    valid_line = makeLine("<sentence>:Name_Version_1 ::= WORD")
    spec = [
            makeSyntacticRule(
                valid_line,
                makeLhsNonTerminal("sentence", "Name_Version_1"),
                [makeTerminal("WORD")],
            )
        ]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 0


def test_number_lhs_terminal():
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([word])
    invalid_nonterminal = makeLine("<1sentence> ::= WORD")
    spec = [
        makeSyntacticRule(
            invalid_nonterminal, makeLhsNonTerminal("1sentence"), [makeTerminal("WORD")]
        )
    ]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsNameFormatError(spec[0])

def test_number_rhs_terminal():
    word = makeLexicalRule(name="1WORD", pattern="1WORD")
    lexicalSpec = makeLexicalSpec([word])
    invalid_terminal = makeLine("<sentence> ::= 1WORD")
    spec = [
        makeSyntacticRule(
            invalid_terminal, makeLhsNonTerminal("sentence"), [makeTerminal("1WORD")]
        )
    ]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidRhsTerminalFormatError(spec[0])

def test_capital_lhs_terminal():
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([word])
    capital_lhs_name = makeLine("<Sentence> ::= WORD")
    spec = [
        makeSyntacticRule(
            capital_lhs_name, makeLhsNonTerminal("Sentence"), [makeTerminal("WORD")]
        )
    ]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsNameFormatError(spec[0])


def test_undercase_lhs_alt_name():
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([word])
    invalid_alt_name = makeLine("<sentence>:name ::= WORD")
    spec = [
        makeSyntacticRule(
            invalid_alt_name,
            makeLhsNonTerminal("sentence", "name"),
            [makeTerminal("WORD")],
        )
    ]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsAltNameFormatError(spec[0])


def test_uppercase_rhs_alt_name():
    invalid_alt_name = makeLine("<sentence> ::= <word>:Name")
    Name1 = [
        makeSyntacticRule(
            invalid_alt_name,
            makeLhsNonTerminal("sentence"),
            [makeRhsNonTerminal("word", "Name")],
        )
    ]
    errors = validate(Name1)
    assert len(errors) == 1
    assert errors[0] == makeInvalidRhsAltNameFormatError(Name1[0])


def test_valid_rhs_alt_name():
    invalid_alt_name = makeLine("<sentence> ::= <word>:name")
    Name1 = [
        makeSyntacticRule(
            invalid_alt_name,
            makeLhsNonTerminal("sentence"),
            [makeRhsNonTerminal("word", "name")],
        )
    ]
    errors = validate(Name1)
    assert len(errors) == 0


def test_underscore_lhs_alt_name():
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([word])
    invalid_alt_name = makeLine("<sentence>:_name ::= WORD")
    spec = [
        makeSyntacticRule(
            invalid_alt_name,
            makeLhsNonTerminal("sentence", "_name"),
            [makeTerminal("WORD")],
        )
    ]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsAltNameFormatError(spec[0])


def test_duplicate_lhs_name():
    verb = makeLexicalRule(name="VERB", pattern="VERB")
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([verb, word])
    lhs_sentence = makeLhsNonTerminal("sentence")
    rule_1 = makeSyntacticRule(
        makeLine("<sentence> ::= VERB"),
        lhs_sentence,
        [makeTerminal("VERB")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<sentence> ::= WORD"),
        lhs_sentence,
        [makeTerminal("WORD")],
    )
    spec = [rule_1, rule_2]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def test_duplicate_lhs_alt_name():
    verb = makeLexicalRule(name="VERB", pattern="VERB")
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([verb, word])
    rule_1 = makeSyntacticRule(
        makeLine("<sentence>:Name ::= VERB"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("VERB")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<sentence>:Name ::= WORD"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("WORD")],
    )
    spec = [rule_1, rule_2]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def test_duplicate_resolved_name():
    verb = makeLexicalRule(name="VERB", pattern="VERB")
    word = makeLexicalRule(name="WORD", pattern="WORD")
    lexicalSpec = makeLexicalSpec([verb, word])
    alt_name = makeSyntacticRule(
        makeLine("<sentence>:Name ::= VERB"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("VERB")],
    )
    non_terminal_name = makeSyntacticRule(
        makeLine("<name> ::= WORD"),
        makeLhsNonTerminal("name"),
        [makeTerminal("WORD")],
    )
    spec = [alt_name, non_terminal_name]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def test_invalid_Rhs_error():
    verb = makeLexicalRule(name="VERB", pattern="VERB")
    lexicalSpec = makeLexicalSpec([verb])
    name1 = makeSyntacticRule(
        makeLine("<sentence> ::= VERB"),
        makeLhsNonTerminal("sentence"),
        [makeTerminal("VERB")],
    )
    name2 = makeSyntacticRule(
        makeLine("<name> ::= <VERB>"),
        makeLhsNonTerminal("name"),
        [makeRhsNonTerminal("VERB")],
    )
    spec = [name1, name2]
    errors = validate(spec, lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidRhsNameFormatError(spec[1])


def validate(syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec = []):
    return validate_syntactic_spec(syntacticSpec, lexicalSpec)


def makeSyntacticSpec(ruleList=None):
    return SyntacticSpec(ruleList)


def makeSyntacticRule(line: Line, lhs: LhsNonTerminal, rhsList: List[Symbol]):
    return SyntacticRule(line, lhs, rhsList)

def makeLexicalSpec(ruleList=None):
    return LexicalSpec(ruleList)

def makeLexicalRule(name='TEST', pattern='TEST'):
    return LexicalRule(makeLine('TEST'), False, name, pattern)

def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)


def makeLhsNonTerminal(name: str | None, altName: str | None = None):
    return LhsNonTerminal(name, altName)


def makeRhsNonTerminal(name: str | None, altName: str | None = None):
    return RhsNonTerminal(name, altName)


def makeTerminal(name: str | None):
    return Terminal(name)


def makeInvalidLhsNameFormatError(rule):
    return InvalidLhsNameError(rule)


def makeInvalidRhsNameFormatError(rule):
    return InvalidRhsNameError(rule)

def makeUndefinedTerminalError(rule):
    return UndefinedTerminalError(rule)

def makeInvalidLhsAltNameFormatError(rule):
    return InvalidLhsAltNameError(rule)


def makeInvalidRhsAltNameFormatError(rule):
    return InvalidRhsAltNameError(rule)


def makeDuplicateLhsError(rule):
    return DuplicateLhsError(rule)

def makeInvalidRhsTerminalFormatError(rule):
    return InvalidRhsTerminalError(rule)
