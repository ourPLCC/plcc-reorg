from pytest import raises, mark, fixture
from .LL1Wrapper import LL1Wrapper
from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    LhsNonTerminal, RhsNonTerminal, Terminal, CapturingTerminal
)

@fixture
def lhsWrapped():
    return LL1Wrapper(getDefaultNonterminalName(), getLhsNonTerminal())

@fixture
def rhsWrapped():
    return LL1Wrapper(getDefaultNonterminalName(), getRhsNonTerminal())

@fixture
def terminalWrapped():
    return LL1Wrapper('TERMINAL', getTerminal())

@fixture
def capturingTerminalWrapped():
    return LL1Wrapper('TERMINAL', getCapturingTerminal())

def test_init(lhsWrapped):
    assert lhsWrapped.name == getDefaultNonterminalName()
    assert lhsWrapped.specObject == getLhsNonTerminal()

def test_nonterminal_eq_with_same_name_and_object(lhsWrapped):
    otherWrapped = createWrapper(lhsWrapped.name, lhsWrapped.specObject)
    assert lhsWrapped == otherWrapped

def test_terminal_eq_with_same_name_and_object(terminalWrapped):
    otherWrapped = createWrapper(terminalWrapped.name, terminalWrapped.specObject)
    assert terminalWrapped == otherWrapped

def test_nonterminal_eq_with_same_name_and_diff_object(lhsWrapped, rhsWrapped):
    assert lhsWrapped == rhsWrapped

def test_terminal_eq_with_same_name_and_diff_object(terminalWrapped, capturingTerminalWrapped):
    assert terminalWrapped == capturingTerminalWrapped

def test_nonterminal_not_eq_with_diff_name(lhsWrapped):
    otherWrapped = createWrapper(getOtherName(), lhsWrapped.specObject)
    assert lhsWrapped != otherWrapped

def test_terminal_not_eq_with_diff_name(terminalWrapped):
    otherWrapped = createWrapper(getOtherTerminalName(), terminalWrapped.specObject)
    assert terminalWrapped != otherWrapped

def test_none_objects_eq_when_same_instance():
    wrapped = createWrappedWithNoneObject(getDefaultNonterminalName())
    otherWrapped = wrapped
    assert wrapped == otherWrapped

def test_none_object_not_eq_when_diff_instance():
    wrapped = createWrappedWithNoneObject(getDefaultNonterminalName())
    otherWrapped = createWrappedWithNoneObject(getDefaultNonterminalName())
    assert wrapped != otherWrapped

def test_not_eq_object_and_none(lhsWrapped):
    otherWrapped = createWrappedWithNoneObject(lhsWrapped.name)
    assert lhsWrapped != otherWrapped

def test_hash_nonterminal_same_name_diff_object(lhsWrapped, rhsWrapped):
    assert hash(lhsWrapped) == hash(rhsWrapped)

def test_hash_terminal_same_name_diff_object(terminalWrapped, capturingTerminalWrapped):
    assert hash(terminalWrapped) == hash(capturingTerminalWrapped)

def test_hash_nonterminal_diff_name(lhsWrapped):
    otherWrapped = createWrapper(getOtherName(), lhsWrapped.specObject)
    assert hash(lhsWrapped) != hash(otherWrapped)

def test_hash_terminal_diff_name(terminalWrapped):
    otherWrapped = createWrapper(getOtherTerminalName(), terminalWrapped.specObject)
    assert hash(terminalWrapped) != hash(otherWrapped)

def test_hash_object_and_none_same_name(lhsWrapped):
    otherWrapped = createWrappedWithNoneObject(lhsWrapped.name)
    assert hash(lhsWrapped) == hash(otherWrapped)

def test_hash_object_and_none_diff_name(lhsWrapped):
    otherWrapped = createWrappedWithNoneObject(getOtherName())
    assert hash(lhsWrapped) != hash(otherWrapped)

def createWrapper(name, specObject):
    return LL1Wrapper(name, specObject)

def createWrappedWithNoneObject(name):
    return LL1Wrapper(name, None)

def getDefaultNonterminalName():
    return 'nonTerminal'

def getDefaultTerminalName():
    return 'TERMINAL'

def getOtherName():
    return 'otherName'

def getOtherTerminalName():
    return 'OTHERTERMINAL'

def getLhsNonTerminal():
    return LhsNonTerminal(getDefaultNonterminalName())

def getRhsNonTerminal():
    return RhsNonTerminal(getDefaultNonterminalName())

def getTerminal():
    return Terminal(getDefaultTerminalName())

def getCapturingTerminal():
    return CapturingTerminal(getDefaultTerminalName())
