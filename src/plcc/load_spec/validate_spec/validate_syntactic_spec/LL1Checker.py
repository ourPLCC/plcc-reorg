from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ValidationError:
    message: str

class LL1Checker:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.firstSets = defaultdict(set)
        self.followSets = defaultdict(set)
        self.parsingTable = defaultdict(dict)
        self.errorList = []
        self.memoDeriveEmpty = {}
        self.memoFirst = {}

    def check(self) -> list[ValidationError]:
        self._generateFirstSets()
        self._generateFollowSets()
        self._buildParsingTable()
        self._checkParsingTable()
        return self.errorList

    def _generateFirstSets(self):
        pass

    def _computeFirst(self, symbol):
        pass

    def _generateFollowSets(self):
        pass

    def _computeFollow(self, nonterminal):
        pass

    def _canDeriveEmptyString(self, symbol):
        pass

    def _buildParsingTable(self):
        pass

    def _checkParsingTable(self):
        pass


