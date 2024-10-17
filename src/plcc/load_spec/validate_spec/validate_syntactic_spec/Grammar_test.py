from pytest import raises, mark, fixture
from .Grammar import Grammar
from .errors import InvalidParameterError

@fixture
def grammar():
    return Grammar()

@fixture
def nonterminal():
    return 'nonTerminal'

@fixture
def terminal():
    return 'TERMINAL'

def test_empty_grammar(grammar):
    assert len(grammar.getRules()) == 0
    assert grammar.getStartSymbol() == None

def test_add_rule(grammar, nonterminal, terminal):
    grammar.addRule(nonterminal, [terminal])
    assert grammar.getRules() == {nonterminal: [[terminal]]}

def test_is_terminal(grammar, terminal):
    assert grammar.isTerminal(terminal) == True
    assert grammar.isNonterminal(terminal) == False

def test_is_nonterminal(grammar, nonterminal):
    assert grammar.isTerminal(nonterminal) == False
    assert grammar.isNonterminal(nonterminal) == True

def test_get_start_symbol_none(grammar):
    assert grammar.getStartSymbol() == None

def test_get_start_symbol(grammar, nonterminal):
    grammar.addRule(nonterminal, [])
    assert grammar.getStartSymbol() == nonterminal

def test_multiple_rules_one_nonterminal(grammar, nonterminal, terminal):
    grammar.addRule(nonterminal, [terminal])
    grammar.addRule(nonterminal, [])
    assert grammar.getRules() == {nonterminal: [[terminal], []]}

def test_add_multiple_nonterminals(grammar, nonterminal, terminal):
    grammar.addRule(nonterminal, [terminal])
    diffNonterminal = nonterminal + 'diff'
    grammar.addRule(diffNonterminal, [])
    assert grammar.getRules() == {nonterminal: [[terminal]], diffNonterminal: [[]]}

def test_add_same_terminal(grammar, nonterminal, terminal):
    grammar.addRule(nonterminal, [terminal])
    grammar.addRule(nonterminal, [terminal])
    assert grammar.getRules() == {nonterminal: [[terminal], [terminal]]}

def test_no_duplicate_terminals(grammar, nonterminal, terminal):
    grammar.addRule(nonterminal, [terminal])
    grammar.addRule(nonterminal, [terminal])
    assert len(grammar.getTerminals()) == 1
    assert terminal in grammar.getTerminals()

def test_no_duplicate_nonterminals(grammar, nonterminal, terminal):
    grammar.addRule(nonterminal, [terminal])
    grammar.addRule(nonterminal, [terminal])
    assert len(grammar.getNonterminals()) == 1
    assert nonterminal in grammar.getNonterminals()

def test_invalid_nonterminal_name_throws_invalid_parameter_error(grammar, terminal):
    with raises(InvalidParameterError):
        grammar.addRule(terminal, [])

def test_invalid_terminal_name_throws_invalid_parameter_error(grammar, nonterminal):
    with raises(InvalidParameterError):
        grammar.addRule(nonterminal, ['1TERMINAL'])

def test_invalid_form_list_throws_invalid_parameter_error(grammar, nonterminal, terminal):
    with raises(InvalidParameterError):
        grammar.addRule(nonterminal, terminal)
