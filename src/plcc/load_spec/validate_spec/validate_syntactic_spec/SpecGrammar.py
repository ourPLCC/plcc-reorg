from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    NonTerminal, Terminal, SyntacticSpec, SyntacticRule
)
from .Grammar import Grammar
from .LL1Wrapper import LL1Wrapper
from .errors import InvalidParameterError

class SpecGrammar(Grammar):
    def __init__(self, syntacticSpec: SyntacticSpec):
        super().__init__()
        self.epsilon = LL1Wrapper("", None)
        self.eof = LL1Wrapper(chr(26), None)
        self.rules = {}
        self.processSyntacticSpec(syntacticSpec)

    def processSyntacticSpec(self, syntacticSpec: SyntacticSpec) -> None:
        self._validateSyntacticSpec(syntacticSpec)
        for rule in syntacticSpec:
            self._processRule(rule)

    def _validateSyntacticSpec(self, syntacticSpec: SyntacticSpec) -> None:
        if not isinstance(syntacticSpec, SyntacticSpec):
            raise InvalidParameterError(str(syntacticSpec))

    def _processRule(self, rule: SyntacticRule) -> None:
        self._validateRuleLHS(rule.lhs)
        nonterminal = LL1Wrapper(rule.lhs.name, rule.lhs)
        rhsWrappers = [self._wrapSymbol(sym) for sym in rule.rhsSymbolList]
        self.addRule(nonterminal, tuple(rhsWrappers))

    def _validateRuleLHS(self, lhs: NonTerminal) -> None:
        if not isinstance(lhs, NonTerminal):
            raise InvalidParameterError(str(lhs))

    def _wrapSymbol(self, sym: Terminal | NonTerminal) -> LL1Wrapper:
        self._validateSymbol(sym)
        return LL1Wrapper(sym.name, sym)

    def _validateSymbol(self, sym: Terminal | NonTerminal) -> None:
        if not isinstance(sym, (Terminal, NonTerminal)):
            raise InvalidParameterError(str(sym))

    def addRule(self, nonterminal: LL1Wrapper, form: tuple[LL1Wrapper]) -> None:
        if nonterminal not in self.rules:
            self.rules[nonterminal] = []
        self.rules[nonterminal].append(form)

    def isTerminal(self, object: object) -> bool:
        return isinstance(object, Terminal)

    def isNonterminal(self, object: object) -> bool:
        return isinstance(object, NonTerminal)

    def getRules(self) -> dict[LL1Wrapper, list[tuple[LL1Wrapper]]]:
        return self.rules

    def getEpsilon(self) -> LL1Wrapper:
        return self.epsilon

    def getEOF(self) -> LL1Wrapper:
        return self.eof


