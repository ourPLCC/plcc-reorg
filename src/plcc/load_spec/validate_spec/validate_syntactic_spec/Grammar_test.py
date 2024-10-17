from pytest import raises, mark, fixture
from .Grammar import Grammar
from .errors import ValidationError

def test_empty_grammar():
    grammar = Grammar()
    assert grammar.getRules() == {}
    assert grammar.getNonterminals() == set()
    assert grammar.getTerminals() == set()
    assert grammar.getStartSymbol() == None

def test_add_rule():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    terminal = generateTerminal()
    grammar.addRule(nonterminal, [terminal])
    assert grammar.getRules() == {nonterminal: [[terminal]]}

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

def test_get_start_symbol_none():
    grammar = Grammar()
    assert grammar.getStartSymbol() == None

def test_get_start_symbol():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    grammar.addRule(nonterminal, [generateTerminal()])
    assert grammar.getStartSymbol() == nonterminal

def test_multiple_rules_one_nonterminal():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    grammar.addRule(nonterminal, [generateTerminal()])
    grammar.addRule(nonterminal, [])
    assert grammar.getRules() == {nonterminal: [[generateTerminal()], []]}

def test_add_multiple_nonterminals():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    grammar.addRule(nonterminal, [generateTerminal()])
    nonterminal2 = generateNonterminal() + 'diff'
    grammar.addRule(nonterminal2, [])
    assert grammar.getRules() == {nonterminal: [[generateTerminal()]], nonterminal2: [[]]}

def test_add_same_terminal():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    grammar.addRule(nonterminal, [generateTerminal()])
    grammar.addRule(nonterminal, [generateTerminal()])
    assert grammar.getRules() == {nonterminal: [[generateTerminal()], [generateTerminal()]]}

def test_no_duplicate_terminals():
    grammar = Grammar()
    terminal = generateTerminal()
    grammar.addRule(generateNonterminal(), [terminal])
    grammar.addRule(generateNonterminal(), [terminal])
    assert len(grammar.getTerminals()) == 1
    assert terminal in grammar.getTerminals()

def test_no_duplicate_nonterminals():
    grammar = Grammar()
    nonterminal = generateNonterminal()
    grammar.addRule(nonterminal, [generateTerminal()])
    grammar.addRule(nonterminal, [generateTerminal()])
    assert len(grammar.getNonterminals()) == 1
    assert nonterminal in grammar.getNonterminals()



def generateNonterminal():
    return 'nonTerminal'

def generateTerminal():
    return 'TERMINAL'