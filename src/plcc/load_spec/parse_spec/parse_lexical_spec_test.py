from pytest import fixture, raises, mark

from .parse_lexical_spec import parse_lexical_spec, LexicalSpec, LexicalRule
from ..load_rough_spec.parse_lines import Line


def test_empty_yields_nothing():
    lexical_spec = parse_lexical_spec([])
    assert lexical_spec.ruleList == []

def test_None_yields_nothing():
    lexical_spec = parse_lexical_spec(None)
    assert lexical_spec.ruleList == []

def test_blank_lines_skipped():
    lexical_spec = parse_lexical_spec([Line('', 1, None)])
    assert lexical_spec.ruleList == []

def test_comment_only_lines_skipped():
    lexical_spec = parse_lexical_spec([Line('#This is a test', 1, None), Line('   #haha look at me  oubweub', 7, None)])
    assert lexical_spec.ruleList == []

def test_one_skip_token_matched():
    lexical_spec = parse_lexical_spec([Line('skip WHITESPACE \',\'', 5, None)])               #is whitespace in the quotations fine?
    assert lexical_spec.ruleList == [LexicalRule(Line('skip WHITESPACE \',\'', 5, None), True, 'WHITESPACE', ',')]

def test_one_token_matches():
    lexical_spec = parse_lexical_spec([Line('token MINUS \'\\-\'', 8, None)])
    assert lexical_spec.ruleList == [LexicalRule(Line('token MINUS \'\\-\'', 8, None), False, 'MINUS', '\\-')]

def test_one_token_no_token_at_start():
    lexical_spec = parse_lexical_spec([Line('MINUS \'\\-\'', 8, None)])
    assert lexical_spec.ruleList == [LexicalRule(Line('MINUS \'\\-\'', 8, None), False, 'MINUS', '\\-')]

def test_tokens_captured_with_trailing_comment():
    lexical_spec = parse_lexical_spec([Line('MINUS \'\\-\'  #This is a test', 8, None), Line('token COMMA \',\' #This is also a test', 9, None)])
    assert lexical_spec.ruleList == [LexicalRule(Line('MINUS \'\\-\'  #This is a test', 8, None), False, 'MINUS', '\\-'), LexicalRule(Line('token COMMA \',\' #This is also a test', 9, None), False, 'COMMA', ',')]

def test_incorrect_format_raises_error():
    with raises(AttributeError):
        lexical_spec = parse_lexical_spec([Line('skip #This one sucks', 12, None)])

