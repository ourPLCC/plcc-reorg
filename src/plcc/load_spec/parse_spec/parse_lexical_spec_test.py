from pytest import fixture, raises, mark

from .parse_lexical_spec import parse_lexical_spec, LexicalSpec, LexicalRule
from ..load_rough_spec.parse_lines import Line


def test_empty_yields_nothing():
    lexical_spec = parse_lexical_spec([]) #Should this return error or nothing?
    assert lexical_spec.ruleList == []

def test_None_yields_nothing():
    lexical_spec = parse_lexical_spec(None)
    assert lexical_spec.ruleList == []

def test_blank_lines_skipped():          #Am I going to be handed the % or no????
    lexical_spec = parse_lexical_spec([Line('', 1, None)])
    assert lexical_spec.ruleList == []

def test_comment_only_lines_skipped():
    lexical_spec = parse_lexical_spec([Line('#This is a test', 1, None), Line('   #haha look at me  oubweub', 7, None)])
    assert lexical_spec.ruleList == []

def test_one_skip_token_matched():
    lexical_spec = parse_lexical_spec([Line('skip WHITESPACE \',\'', 5, None)])               #is whitespace in the quotations fine?
    assert lexical_spec.ruleList == [LexicalRule(Line('skip WHITESPACE \',\'', 5, None), True, 'WHITESPACE', ',')]
    #The ones above and below give an 'escape' warning when using "\'\s+\'" (Example line 1 in README)??
    #Should I remove the escape characters in the quotes or leave them?

def test_one_token_matches():
    lexical_spec = parse_lexical_spec([Line('token MINUS \'\-\'', 8, None)])
    assert lexical_spec.ruleList == [LexicalRule(Line('token MINUS \'\-\'', 8, None), False, 'MINUS', '\-')]

