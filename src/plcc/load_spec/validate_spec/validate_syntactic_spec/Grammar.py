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

        self._populateTerminalsAndNonterminals(form)

        if self.startSymbol is None:
            self.startSymbol = nonterminal
    
    def _populateTerminalsAndNonterminals(self, form: list[str]):
        for symbol in form:
            if self.isTerminal(symbol):
                self.terminals.add(symbol)
            elif self.isNonterminal(symbol):
                self.nonterminals.add(symbol)

    def getStartSymbol(self) -> str:
        return self.startSymbol

    def isTerminal(self, object: str) -> bool:
        return not object[0].islower()

    def isNonterminal(self, object: str) -> bool:
        return object[0].islower()

    def getRules(self) -> dict[str, list[list[str]]]:
        return self.rules

    def getTerminals(self) -> set[str]:
        return self.terminals

    def getNonterminals(self) -> set[str]:
        return self.nonterminals