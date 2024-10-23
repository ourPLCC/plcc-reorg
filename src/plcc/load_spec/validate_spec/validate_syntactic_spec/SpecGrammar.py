from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    NonTerminal, RepeatingSyntacticRule, Terminal, SyntacticSpec, SyntacticRule
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
        self.nonterminals = set()
        self.terminals = set()
        self.startSymbol = None
        self._processSyntacticSpec(syntacticSpec)

    def _processSyntacticSpec(self, syntacticSpec: SyntacticSpec) -> None:
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
        if isinstance(rule, RepeatingSyntacticRule):
            separatorWrapper = self._wrapSymbol(rule.separator) if rule.separator else None
            self.addRule(nonterminal, tuple(rhsWrappers), separatorWrapper)
        else:
            self.addRule(nonterminal, tuple(rhsWrappers))
        self._updateStartSymbol(nonterminal)

    def _validateRuleLHS(self, lhs: NonTerminal) -> None:
        if not isinstance(lhs, NonTerminal):
            raise InvalidParameterError(str(lhs))

    def _wrapSymbol(self, sym: Terminal | NonTerminal) -> LL1Wrapper:
        self._validateSymbol(sym)
        return LL1Wrapper(sym.name, sym)

    def _validateSymbol(self, sym: Terminal | NonTerminal) -> None:
        if not isinstance(sym, (Terminal, NonTerminal)):
            raise InvalidParameterError(str(sym))

    def addRule(self, nonterminal: LL1Wrapper, form: tuple[LL1Wrapper], separator: LL1Wrapper = None) -> None:
        if nonterminal not in self.rules:
            self.rules[nonterminal] = []
        if separator:
            self.rules[nonterminal].append([form, separator])
        else:
            self.rules[nonterminal].append([form])
        self._updateNonterminalsAndTerminals(nonterminal, form)

    def _updateNonterminalsAndTerminals(self, nonterminal: LL1Wrapper, form: tuple[LL1Wrapper]) -> None:
        self.nonterminals.add(nonterminal)
        for sym in form:
            if self.isTerminal(sym.specObject):
                self.terminals.add(sym)
            elif self.isNonterminal(sym.specObject):
                self.nonterminals.add(sym)

    def _updateStartSymbol(self, nonterminal: LL1Wrapper) -> None:
        if self.startSymbol is None:
            self.startSymbol = nonterminal

    def isTerminal(self, object: object) -> bool:
        return isinstance(object, Terminal)

    def isNonterminal(self, object: object) -> bool:
        return isinstance(object, NonTerminal)

    def getRules(self) -> dict[LL1Wrapper, list[tuple[LL1Wrapper]]]:
        return self.rules

    def getStartSymbol(self) -> LL1Wrapper:
        return self.startSymbol

    def getNonterminals(self) -> set[LL1Wrapper]:
        return self.nonterminals

    def getTerminals(self) -> set[LL1Wrapper]:
        return self.terminals

    def getEpsilon(self) -> LL1Wrapper:
        return self.epsilon

    def getEOF(self) -> LL1Wrapper:
        return self.eof


