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

def test_is_terminal():
    grammar = Grammar()
    terminal = generateTerminal()
    assert grammar.isTerminal(terminal) == True
    assert grammar.isNonterminal(terminal) == False

def test_is_nonterminal():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    assert grammar.isTerminal(nonterminal) == False
    assert grammar.isNonterminal(nonterminal) == True


def generateNonterminal():
    return 'nonTerminal'

def generateTerminal():
    return 'TERMINAL'