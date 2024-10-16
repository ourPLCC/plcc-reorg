from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    NonTerminal, Terminal
)
from .LL1Checker_and_Grammar import Grammar

class LL1Wrapper:
    def __init__(self, symbolName: str, specObject):
        self.name = symbolName
        self.specObject = specObject

    def __eq__(self, other):
        return isinstance(other, LL1Wrapper) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class SpecGrammar(Grammar):
    def __init__(self, syntacticSpec):
        super().__init__()
        self.rules = {}
        self.processSyntacticSpec(syntacticSpec)

    def processSyntacticSpec(self, syntacticSpec):
        for rule in syntacticSpec:
            nonterminal = LL1Wrapper(rule.lhs.name, rule.lhs)
            rhsWrappers = []

            for sym in rule.rhsSymbolList:
                wrappedSym = LL1Wrapper(sym.name, sym)
                rhsWrappers.append(wrappedSym)
            self.addRule(nonterminal, tuple(rhsWrappers))

    def addRule(self, nonterminal: LL1Wrapper, form: (LL1Wrapper)):
        if nonterminal not in self.rules:
            self.rules[nonterminal] = []
        self.rules[nonterminal].append(form)

    def isTerminal(self, object):
        return isinstance(specObject, Terminal)

    def isNonterminal(self, object):
        return isinstance(specObject, NonTerminal)

    def getRules(self):
        return self.rules


