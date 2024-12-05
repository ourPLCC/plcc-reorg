from ...parse_spec.parse_lexical_spec import LexicalSpec
from ...parse_spec.parse_syntactic_spec import (
    SyntacticSpec,
    CapturingSymbol,
    Terminal,
    RepeatingSyntacticRule
)
from .errors import (
    DuplicateRhsSymbolError,
    ValidationError,
    InvalidRepeatingRuleSeparatorError
)

def validate_rhs(syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec, nonTerminals: set()):
    return SyntacticRhsValidator(syntacticSpec.copy(), lexicalSpec, nonTerminals).validate()

class SyntacticRhsValidator:
    spec: SyntacticSpec

    def __init__(self, syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec, nonTerminals: set()):
        self.syntacticSpec = syntacticSpec
        self.lexicalSpec = lexicalSpec
        self.errorList = []
        self.nonTerminals = set()

    def validate(self) -> tuple[list[ValidationError], set[str]]:
        while len(self.syntacticSpec) > 0:
            self.rule = self.syntacticSpec.pop(0)
            self._checkLine()
        return self.errorList, self.nonTerminals

    def _checkLine(self):
        self._validateResolvedNames()
        if self._isRepeatingRule():
            self._validateSeparator()

    def _validateResolvedNames(self):
        for resolvedName in self._getResolvedNames():
            if resolvedName in self.nonTerminals:
                self._appendDuplicateRhsSymbolError()
            self.nonTerminals.add(resolvedName)

    def _getResolvedNames(self) -> list[str]:
        resolvedNames = []
        for symbol in self.rule.rhsSymbolList:
            if self._isCapturingSymbol(symbol):
                self._addResolvedNameToList(symbol, resolvedNames)
        return resolvedNames

    def _addResolvedNameToList(self, symbol, resolvedNames):
        resolvedName = self._getResolvedName(symbol)
        resolvedNames.append(resolvedName)

    def _getResolvedName(self, symbol) -> str:
        return symbol.altName if symbol.altName else symbol.name

    def _isRepeatingRule(self):
        return True if isinstance(self.rule, RepeatingSyntacticRule) else False

    def _validateSeparator(self):
        if not self._isSeparatorTerminal():
            self._appendInvalidRepeatingRuleSeparatorError()

    def _isSeparatorTerminal(self):
        return True if isinstance(self.rule.separator, Terminal) else False

    def _isCapturingSymbol(self, symbol):
        return True if isinstance(symbol, CapturingSymbol) else False

    def _appendInvalidRepeatingRuleSeparatorError(self):
        self.errorList.append(InvalidRepeatingRuleSeparatorError(self.rule))

    def _appendDuplicateRhsSymbolError(self):
        self.errorList.append(DuplicateRhsSymbolError(self.rule))

