from pytest import raises, mark, fixture

from ..load_rough_spec.parse_lines import Line
from ..load_rough_spec.parse_blocks import Block
from .validate_lexical_spec import ValidationError, validate_lexical_spec
from ..parse_spec.parse_lexical_spec import LexicalRule, LexicalSpec

def test_empty_no_errors():
    lexicalSpec = makeLexicalSpec([])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 0

def test_None_no_errors():
    lexicalSpec = makeLexicalSpec(None)
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 0

def test_lowercase_name_format_error():
    invalidName = makeLexicalRule(makeLine("invalid_name \'n\'"), False, "invalid_name", "")
    lexicalSpec = makeLexicalSpec([invalidName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidNameFormatError(invalidName)

def test_whitespace_name_format_error():
    whitespaceName = makeLexicalRule(makeLine("NAME ERROR \'\\s+\'"), False, "NAME ERROR", "\\s+")
    lexicalSpec = makeLexicalSpec([whitespaceName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidNameFormatError(whitespaceName)

def test_empty_name_format_error():
    emptyName = makeLexicalRule(makeLine(""), False, "", "")
    lexicalSpec = makeLexicalSpec([emptyName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidNameFormatError(emptyName)

def test_invalid_character_format_error():
    invalidName = makeLexicalRule(makeLine("TE$T \'T\'"), True, "TE$T", "T")
    lexicalSpec = makeLexicalSpec([invalidName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidNameFormatError(invalidName)

def test_name_start_with_number_format_error():
    numberName = makeLexicalRule(makeLine("skip 1WHITESPACE \'\\s+\'"), True, "1WHITESPACE", "\\s+")
    lexicalSpec = makeLexicalSpec([numberName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidNameFormatError(numberName)

def test_valid_name_no_error():
    validName = makeLexicalRule(makeLine("TEST \'T\'"), False, "TEST", "T")
    lexicalSpec = makeLexicalSpec([validName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 0

def test_skip_rule_no_error():
    skipRule = makeLexicalRule(makeLine("skip WHITESPACE \'\\s+\'"), True, "WHITESPACE", "\\s+")
    lexicalSpec = makeLexicalSpec([skipRule])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 0

def test_duplicate_names_duplicate_error():
    validName = makeLexicalRule(makeLine("VALID \'-\'"), False, "VALID", "-")
    duplicateName = makeLexicalRule(makeLine("VALID \'+\'"), False, "VALID", "+")
    lexicalSpec = makeLexicalSpec([validName, duplicateName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateNameError(duplicateName)

def test_unique_names_no_error():
    validName = makeLexicalRule(makeLine("VALID"), False, "VALID", "-")
    secondValidName = makeLexicalRule(makeLine("VALID_2"), False, "VALID_2", "+")
    lexicalSpec = makeLexicalSpec([validName, secondValidName])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 0

def test_line_invalid_rule_error():
    line = makeLine("gibberish with no pattern or token")
    lexicalSpec = makeLexicalSpec([line])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidRuleError(line)

def test_rule_followed_by_line_invalid_rule_error():
    rule = makeLexicalRule(makeLine("TEST \'\\w+\'"), False, "TEST", "\\w+")
    line = makeLine("there is nothing useful here")
    lexicalSpec = makeLexicalSpec([rule, line])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidRuleError(line)

def test_duplicate_patterns_not_allowed():
    pattern = makeLexicalRule(makeLine("TEST \'\\w+\'"), False, "TEST", "\\w+")
    duplicatePattern = makeLexicalRule(makeLine("TEST2 \'\\w+\'"), False, "TEST2", "\\w+")
    lexicalSpec = makeLexicalSpec([pattern, duplicatePattern])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicatePatternError(duplicatePattern)

def test_patterns_with_closing_quotes_is_an_error():
    closingQuotes = makeLexicalRule(makeLine("TEST \'\\w+\'"), False, "TEST", "\"")
    lexicalSpec = makeLexicalSpec([closingQuotes])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidPatternError(closingQuotes)

def test_multiple_errors():
    validName = makeLexicalRule(makeLine("NAME \'-\'"), False, "NAME", "-")
    invalidName = makeLexicalRule(makeLine("name \'+\'"), False, "name", "+")
    duplicateName = makeLexicalRule(makeLine("NAME \'\\s+\'"), False, "NAME", "\\s+")
    line = makeLine("no rules here")
    lexicalSpec = makeLexicalSpec([validName, invalidName, duplicateName, line])
    errors = validate_lexical_spec(lexicalSpec)
    assert len(errors) == 3
    assert errors[0] == makeInvalidNameFormatError(invalidName)
    assert errors[1] == makeDuplicateNameError(duplicateName)
    assert errors[2] == makeInvalidRuleError(line)

def makeLexicalSpec(ruleList=None):
    return LexicalSpec(ruleList)

def makeLexicalRule(line, isSkip, name, pattern):
    return LexicalRule(line, isSkip, name, pattern)

def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)

def makeInvalidNameFormatError(rule):
    message = f"Invalid name format for rule '{rule.name}' (Must be uppercase letters, numbers, and underscores, and cannot start with a number) on line: {rule.line.number}"
    return makeValidationError(rule.line, message)

def makeDuplicateNameError(rule):
    message = f"Duplicate rule name found '{rule.name}' on line: {rule.line.number}"
    return makeValidationError(rule.line, message)

def makeDuplicatePatternError(rule):
    message = f"Duplicate rule pattern found '{rule.pattern}' on line: {rule.line.number}"
    return makeValidationError(rule.line, message)

def makeInvalidPatternError(rule):
    message = f"Duplicate pattern format found '{rule.pattern}' on line: {rule.line.number} (Patterns can not contain closing closing quotes)"
    return makeValidationError(rule.line, message)

def makeInvalidRuleError(line):
    message = f"Invalid rule format found on line: {line.number}"
    return makeValidationError(line, message)

def makeValidationError(line, message):
    return ValidationError(line, message)
