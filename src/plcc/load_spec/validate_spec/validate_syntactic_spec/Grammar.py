import re
from .errors import InvalidParameterError

class Grammar:
    def __init__(self):
        self.rules = {}
        self.startSymbol = None
        self.terminals = set()
        self.nonterminals = set()

    def addRule(self, nonterminal: str, form: list[str]):
        self._checkParametersForErrors(nonterminal, form)
        self._handleRule(nonterminal, form)
        self._populateTerminalsAndNonterminals(form)
        self._updateStartSymbol(nonterminal)

    def _checkParametersForErrors(self, nonterminal: str, form: list[str]):
        if not self.isNonterminal(nonterminal):
            raise InvalidParameterError(str(nonterminal))
        if not isinstance(form, list):
            raise InvalidParameterError(str(form))
        for symbol in form:
            if not (self.isNonterminal(symbol) or self.isTerminal(symbol)):
                raise InvalidParameterError(str(symbol))

    def _handleRule(self, nonterminal: str, form: list[str]):
        self.nonterminals.add(nonterminal)
        if nonterminal not in self.rules:
            self.rules[nonterminal] = []
        self.rules[nonterminal].append(form)

    def _populateTerminalsAndNonterminals(self, form: list[str]):
        for symbol in form:
            if self.isTerminal(symbol):
                self.terminals.add(symbol)
            elif self.isNonterminal(symbol):
                self.nonterminals.add(symbol)

    def _updateStartSymbol(self, nonterminal: str):
        if self.startSymbol is None:
            self.startSymbol = nonterminal

    def getStartSymbol(self) -> str:
        return self.startSymbol

    def isTerminal(self, object: str) -> bool:
        pattern = r'^[A-Z_][A-Z0-9_]*$'
        return bool(re.match(pattern, object))

    def isNonterminal(self, object: str) -> bool:
        pattern = r'^[a-z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, object))

    def getRules(self) -> dict[str, list[list[str]]]:
        return self.rules

    def getTerminals(self) -> set[str]:
        return self.terminals

    def getNonterminals(self) -> set[str]:
        return self.nonterminals
