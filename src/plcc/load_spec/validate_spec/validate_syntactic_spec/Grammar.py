import re
from .errors import InvalidParameterError

class Grammar:
    def __init__(self):
        self.rules = {}
        self.startSymbol = None
        self.terminals = set()
        self.nonterminals = set()
        self.nonterminal = None
        self.form = None

    def addRule(self, nonterminal: str, form: list[str]):
        self.nonterminal = nonterminal
        self.form = form
        self._checkParametersForErrors()
        self._handleRule()
        self._populateTerminalsAndNonterminals(form)
        self._updateStartSymbol()
    
    def _checkParametersForErrors(self):
        if not self.isNonterminal(self.nonterminal):
            raise InvalidParameterError(str(self.nonterminal))
        if not isinstance(self.form, list):
            raise InvalidParameterError(str(self.form))
        for symbol in self.form:
            if not (self.isNonterminal(symbol) or self.isTerminal(symbol)):
                raise InvalidParameterError(str(symbol))
            
    def _handleRule(self):
        self.nonterminals.add(self.nonterminal)
        if self.nonterminal not in self.rules:
            self.rules[self.nonterminal] = []
        self.rules[self.nonterminal].append(self.form)

    def _populateTerminalsAndNonterminals(self, form: list[str]):
        for symbol in form:
            if self.isTerminal(symbol):
                self.terminals.add(symbol)
            elif self.isNonterminal(symbol):
                self.nonterminals.add(symbol)

    def _updateStartSymbol(self):
        if self.startSymbol is None:
            self.startSymbol = self.nonterminal

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