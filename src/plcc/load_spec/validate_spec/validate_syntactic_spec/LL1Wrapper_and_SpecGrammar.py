from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    NonTerminal, Terminal
)
from .LL1Checker_and_Grammar import Grammar

class LL1Wrapper:
    def __init__(self, symbolName: str, specObject: Object):
        self.name = symbolName
        self.specObject = specObject

    def __eq__(self, other):
        return isinstance(other, LL1Wrapper) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class SpecGrammar(Grammar):
    def __init__(self):
        super().__init__()
        self.rules = {}

    def addRule(self, nonterminal: LL1Wrapper, form: (LL1Wrapper, LL1Wrapper)):
        wrappedNonterminal = Wrapper(nonterminal.name, nonterminal)
        wrappedForm = tuple(Wrapper(symbol.name, symbol) for symbol in form)

        if wrappedNonterminal not in self.rules:
            self.rules[wrappedNonterminal] = []
        self.rules[wrappedNonterminal].append(wrappedForm)

    def isTerminal(self, object):
        return isinstance(object.specObject, Terminal)

    def isNonterminal(self, object):
        return isinstance(object.specObject, NonTerminal)

    def getRules(self):
        return self.rules


