from pytest import raises, mark, fixture
from plcc.load_spec.load_rough_spec.parse_dividers import parse_dividers
from plcc.load_spec.load_rough_spec.parse_lines import Line
from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    NonTerminal, Terminal, SyntacticSpec, SyntacticRule, RhsNonTerminal, LhsNonTerminal, RepeatingSyntacticRule, CapturingTerminal
)
from .LL1Wrapper import LL1Wrapper
from .SpecGrammar import SpecGrammar
from plcc.load_spec.parse_spec.parse_syntactic_spec.parse_syntactic_spec import parse_syntactic_spec
from .errors import InvalidParameterError


def test_init():
    syntacticSpec = parse_syntactic_spec([makeDivider()])
    grammar = makeSpecGrammar(syntacticSpec)
    assert grammar.getEpsilon() == grammar.getEpsilon()
    assert grammar.getEOF() == getEOF()
    assert len(grammar.getRules()) == 0
    assert grammar.getStartSymbol() == None

def test_process_syntactic_spec():
    syntacticSpec = parse_syntactic_spec([makeDivider(), makeLine('<exp> ::= VAR')])
    grammar = makeSpecGrammar(syntacticSpec)
    assert len(grammar.getRules()) == 1


def test_invalid_syntactic_spec_handling():
    with raises(InvalidParameterError):
        makeSpecGrammar("syntactic_spec")

def parseSyntacticSpec(lines):
    return parse_syntactic_spec(lines)

def makeDivider(string="%", lineNumber=0, file=""):
    return parse_dividers([makeLine(string, lineNumber, file)])

def makeSpecGrammar(syntacticSpec):
    return SpecGrammar(syntacticSpec)

def getEpsilon():
    return LL1Wrapper("", None)

def getEOF():
    return LL1Wrapper(chr(26), None)

def makeLine(string, lineNumber=0, file=""):
    return Line(string, lineNumber, file)

def genLhsNonterminal(name):
    return LhsNonTerminal(name)

def genTerminal(name):
    return Terminal(name)

def genRhsNonTerminal(name):
    return RhsNonTerminal(name)

def genCapturingTerminal(name):
    return CapturingTerminal(name)


