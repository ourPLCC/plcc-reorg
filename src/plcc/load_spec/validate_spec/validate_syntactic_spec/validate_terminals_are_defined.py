from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import CapturingTerminal, Terminal
from .errors import UndefinedTerminalError
from ...parse_spec.parse_syntactic_spec import SyntacticSpec
from ...parse_spec.parse_lexical_spec import LexicalSpec

def validate_terminals_are_defined(syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec):
    return TerminalsAreDefinedValidator(syntacticSpec, lexicalSpec).validate()

class TerminalsAreDefinedValidator:
    def __init__(self, syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec):
        self.syntacticSpec = syntacticSpec
        self.lexicalSpec = lexicalSpec
        self.definedTerminals = None
        self.errorList = []

    def validate(self):
        for rule in self.syntacticSpec:
            self._validateTerminalsAreDefined(rule)
        return self.errorList

    def _validateTerminalsAreDefined(self, rule):
        for sym in rule.rhsSymbolList:
            if self._isTerminal(sym) and self._isUndefined(sym):
                self.errorList.append(UndefinedTerminalError(rule))

    def _isTerminal(self, sym):
        return isinstance(sym, (Terminal, CapturingTerminal))

    def _isUndefined(self, sym):
        if self.definedTerminals is None:
            self.definedTerminals = self._getDefinedTerminals(self.lexicalSpec)
        return sym.name not in self.definedTerminals

    def _getDefinedTerminals(self, lexicalSpec):
        if not lexicalSpec:
            return set()
        return {rule.name for rule in lexicalSpec.ruleList}
