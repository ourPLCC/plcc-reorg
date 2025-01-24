from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import CapturingTerminal, Terminal
from .errors import UndefinedTerminalError
from ...parse_spec.parse_syntactic_spec import SyntacticSpec
from ...parse_spec.parse_lexical_spec import LexicalSpec

def validate_terminals(syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec):
    return TerminalValidator(syntacticSpec, lexicalSpec).validate()

class TerminalValidator:
    def __init__(self, syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec):
        self.syntacticSpec = syntacticSpec
        self.lexicalSpec = lexicalSpec
        self.definedTerminals = self._getDefinedTerminals()
        self.errorList = []

    def validate(self):
        for rule in self.syntacticSpec:
            self._validateTerminal(rule)
        return self.errorList

    def _getDefinedTerminals(self):
        if not self.lexicalSpec:
            return set()
        return {rule.name for rule in self.lexicalSpec.ruleList}

    def _validateTerminal(self, rule):
        for sym in rule.rhsSymbolList:
            if self._isTerminalOrCapturingTerminal(sym) and not self._isDefinedTerminal(sym):
                self.errorList.append(UndefinedTerminalError(rule))

    def _isDefinedTerminal(self, sym):
        return sym.name in self.definedTerminals

    def _isTerminalOrCapturingTerminal(self, sym):
        return isinstance(sym, (Terminal, CapturingTerminal))

