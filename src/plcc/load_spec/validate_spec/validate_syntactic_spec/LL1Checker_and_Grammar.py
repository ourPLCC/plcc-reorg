from .LL1wrapper import LL1Wrapper
from dataclasses import dataclass

@dataclass
class ValidationError:
    message: str

class Grammar:
    def __init__(self):
        self.rules = {}
        self.startSymbol = None
        self.terminals = set()
        self.nonterminals = set()

    def addRule(self, nonterminal: str, form: list[str]):
        self.nonterminals.add(nonterminal)
        if nonterminal not in self.rules:
            self.rules[nonterminal] = []
        self.rules[nonterminal].append(form)

        for symbol in form:
            if self.isTerminal(symbol):
                self.terminals.add(symbol)
            elif self.isNonterminal(symbol):
                self.nonterminals.add(symbol)

        if self.startSymbol is None:
            self.startSymbol = nonterminal

    def getStartSymbol(self) -> str:
        return self.startSymbol

    def isTerminal(self, object: str) -> bool:
        return not symbol[0].islower()

    def isNonterminal(self, object: str) -> bool:
        return symbol[0].islower()

    def getRules(self) -> dict[str, list[list[str]]]:
        return self.rules

    def getTerminals(self) -> set[str]:
        return self.terminals

    def getNonterminals(self) -> set[str]:
        return self.nonterminals

class LL1Checker:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.firstSets = {}
        self.followSets = {}
        self.parsingTable = {}

    def check(self) -> list[ValidationError]:
        pass

    def _generateFirstSets(self):
        pass

    def _generateFollowSets(self):
        pass

    def _buildParsingTable(self):
        pass

    def _checkParsingTable(self):
        pass


