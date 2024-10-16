from collections import defaultdict


class BnfSpec:
    def __init__(self, bnfRules):
        self.rules = bnfRules

    def getTerminals(self):
        for rule in self.rules:
            for tnt in rule.rightHandSymbols:
                if tnt.isTerminal:
                    yield rule, tnt
            if rule.separator:
                yield rule, rule.separator

    def getRules(self):
        for rule in self.rules:
            yield rule

    def getRulesWithDuplicateLhsNames(self):
        rulesByLhsName = defaultdict(list)
        for r in self.getRules():
            rulesByLhsName[r.leftHandSymbol.name].append(r)
        for name in rulesByLhsName:
            if len(rulesByLhsName[name]) > 1:
                for rule in rulesByLhsName[name]:
                    yield rule

    def getLhsNames(self):
        lhsNames = set()
        for r in self.getRules():
            lhsNames.add(r.leftHandSymbol.name)
        return lhsNames

    def getRhsNonterminals(self):
        for r in self.getRules():
            for t in r.rightHandSymbols:
                if not t.isTerminal:
                    yield r, t

    def getRulesThatHaveSep(self):
        for r in self.getRules():
            if r.separator:
                yield r

    def getNonrepeatingRules(self):
        for r in self.getRules():
            if not r.isRepeating:
                yield r


