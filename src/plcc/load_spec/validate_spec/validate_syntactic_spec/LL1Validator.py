from .LL1Checker_and_Grammar import LL1Checker
from .LL1wrapper_and_SpecGrammar import SpecGrammar

def checkLL1(syntactic_spec):
    LL1Validator(syntactic_spec).validate()

class LL1Validator:
    def __init__(self, syntactic_spec):
        self.syntacticSpec = syntactic_spec

    def validate(self):
        grammar = SpecGrammar(self.syntacticSpec)
        checker = LL1Checker(grammar)
        return checker.check()






