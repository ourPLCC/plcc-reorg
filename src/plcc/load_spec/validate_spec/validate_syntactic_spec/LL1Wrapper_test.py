from pytest import raises, mark, fixture
from .LL1Wrapper import LL1Wrapper
from plcc.load_spec.parse_spec.parse_syntactic_spec.structs import (
    LhsNonTerminal, RhsNonTerminal, Terminal, Symbol
)

@fixture
def lhsNonTerminal():
    return LhsNonTerminal(getDefaultNonterminalName())

@fixture
def rhsNonTerminal():
    return RhsNonTerminal(getDefaultNonterminalName())

@fixture
def lhsWrapped(lhsNonTerminal):
    return LL1Wrapper(getDefaultNonterminalName(), lhsNonTerminal)

@fixture
def rhsWrapped(rhsNonTerminal):
    return LL1Wrapper(getDefaultNonterminalName(), rhsNonTerminal)

def test_init(lhsWrapped, lhsNonTerminal):
    assert lhsWrapped.name == getDefaultNonterminalName()
    assert lhsWrapped.specObject == lhsNonTerminal

def test_eq_with_same_name_and_object(lhsWrapped, lhsNonTerminal):
    otherWrapped = createWrapper(lhsWrapped.name, lhsNonTerminal)
    assert lhsWrapped == otherWrapped

def test_eq_with_same_name_and_diff_object(lhsWrapped, rhsWrapped):
    assert lhsWrapped == rhsWrapped

def test_not_eq_with_diff_name(lhsWrapped):
    otherWrapped = createWrapper(getOtherName(), lhsWrapped.specObject)
    assert lhsWrapped != otherWrapped

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

def test_hash_same_name_diff_object(lhsWrapped, rhsWrapped):
    assert hash(lhsWrapped) == hash(rhsWrapped)

def test_hash_diff_name(lhsWrapped):
    otherWrapped = createWrapper(getOtherName(), lhsWrapped.specObject)
    assert hash(lhsWrapped) != hash(otherWrapped)

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

def getOtherName():
    return 'otherName'
