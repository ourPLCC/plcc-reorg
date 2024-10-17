from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    NonTerminal, Terminal
)
from .Grammar import Grammar
from .LL1Wrapper import LL1Wrapper

class SpecGrammar(Grammar):
    def __init__(self, syntacticSpec):
        super().__init__()
        self.epsilon = LL1Wrapper("", None)
        self.eof = LL1Wrapper(chr(26), None)
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
        return isinstance(object, Terminal)

    def isNonterminal(self, object):
        return isinstance(object, NonTerminal)

    def getRules(self):
        return self.rules
    
    def getEpsilon(self):
        return self.epsilon
    
    def getEOF(self):
        return self.eof 


