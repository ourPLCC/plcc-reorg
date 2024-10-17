from pytest import raises, mark, fixture
from .Grammar import Grammar

def test_add_rule():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    terminal = generateTerminal()
    grammar.addRule(nonterminal, [terminal])
    assert grammar.getRules() == {nonterminal: [[terminal]]}
    assert nonterminal in grammar.getNonterminals()
    assert terminal in grammar.getTerminals()

def generateNonterminal():
    return 'nonTerminal'

def generateTerminal():
    return 'TERMINAL'