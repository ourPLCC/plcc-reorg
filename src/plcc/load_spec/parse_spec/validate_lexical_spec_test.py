from pytest import raises, mark, fixture

from ..load_rough_spec.parse_lines import Line
from ..load_rough_spec.parse_blocks import Block
from .validate_lexical_spec import ValidationError, validate_lexical_spec
from .parse_lexical_spec import LexicalRule, LexicalSpec

def test_empty_no_errors():
    lexicalSpec = makeLexicalSpec()
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 0

def test_invalid_name_format_error():
    invalidName = makeLexicalRule(makeLine("invalid-name"), False, "invalid-name", "")
    lexicalSpec = makeLexicalSpec([invalidName])
    errors = validate_lexical_spec(lexicalSpec)
    assert errors[0] == makeInvalidNameFormatError(invalidName)

def makeLexicalSpec(ruleList=None):
    return LexicalSpec(ruleList)

def makeLexicalRule(line, isSkip, name, pattern):
    return LexicalRule(line, isSkip, name, pattern)

def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)

def makeInvalidNameFormatError(rule):
    message = f"Invalid name format for rule '{rule.name}': Must be uppercase letters, numbers, and underscores, and cannot start with a number"
    return makeValidationError(rule.line, message)

def makeDuplicateNameError(rule):
    message = f"Duplicate rule name found: {rule.name}"
    return makeValidationError(line.line, message)

def makeValidationError(line, message):
    return ValidationError(line, message)
