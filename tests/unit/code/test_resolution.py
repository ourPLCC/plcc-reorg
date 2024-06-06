import pytest


from plcc.spec.symbol import Symbol

from plcc.code.translator.default import DefaultTranslator
from plcc.code.translator.java import JavaTranslator
from plcc.code.translator.python import PythonTranslator
from plcc.code.structures import UnresolvedBaseClassName
from plcc.code.structures import UnresolvedClassName
from plcc.code.structures import UnresolvedTypeName
from plcc.code.structures import UnresolvedVariableName
from plcc.code.structures import UnresolvedListVariableName
from plcc.code.structures import UnresolvedListTypeName
from plcc.code.structures import FieldReference
from plcc.code.structures import AssignVariableToField
from plcc.code.structures import Parameter


def test_UnresolvedTypeName_resolves_to_capitalized_symbol_name():
    unresolved = givenUnresolved(of=UnresolvedTypeName, name='cat', givenName='pet')
    resolved = whenResolvedByDefault(unresolved)
    assert resolved == 'Cat'


def test_UnresolvedVariableName_resolves_to_symbol_given_name():
    unresolved = givenUnresolved(of=UnresolvedVariableName, name='cat', givenName='pet')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'pet'


def test_UnresolvedVariableName_if_no_given_name_resolves_to_symbol_name():
    unresolved = givenUnresolved(of=UnresolvedVariableName, name='cat', givenName=None)
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'cat'


def test_UnresolvedTypeName_if_terminal_resolves_to_Token():
    unresolved = givenUnresolved(of=UnresolvedTypeName, name='cat', givenName='pet', isTerminal=True)
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'Token'


def test_UnresolvedClassName_resolves_to_symbol_given_name():
    unresolved = givenUnresolved(of=UnresolvedClassName, name='cat', givenName='pet')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'pet'


def test_UnresolvedClassName_resolves_to_capitalized_symbol_name_if_no_given_name():
    unresolved = givenUnresolved(of=UnresolvedClassName, name='cat', givenName=None)
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'Cat'


def test_UnresolvedBaseClassName_resolves_to_capitalized_symbol_name():
    unresolved = givenUnresolved(of=UnresolvedBaseClassName, name='cat', givenName='Pet')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'Cat'


def test_UnresolvedListVariableName_resolves_to_given_name():
    unresolved = givenUnresolved(of=UnresolvedListVariableName, name='cat', givenName='fluffy')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'fluffy'


def test_UnresolvedListVariableName_if_no_given_name_resolves_to_symbol_name_appended_with_List():
    unresolved = givenUnresolved(of=UnresolvedListVariableName, name='cat', givenName='')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'catList'


def test_in_Java_UnresolvedListTypeName_resolves_to_List_parameterized_by_its_resolved_type_name():
    unresolved = givenUnresolved(of=UnresolvedListTypeName, name='cat', givenName='fluffy')
    resolved = whenResolve(unresolved, using=JavaTranslator())
    assert resolved == 'List<Cat>'


def test_in_Python_UnresolvedListTypeName_resolves_to_square_brackets_containing_its_resolved_type_name():
    unresolved = givenUnresolved(of=UnresolvedListTypeName, name='cat', givenName='fluffy')
    resolved = whenResolve(unresolved, using=PythonTranslator())
    assert resolved == '[Cat]'


def test_in_Java_FieldReference_resolves_to_this_dot_variable_name():
    unresolved = givenFieldReference('cat')
    resolved = whenResolvedByJava(unresolved)
    assert resolved == 'this.cat'


def test_in_Python_FieldReference_resolves_to_self_dot_variable_name():
    unresolved = givenFieldReference('cat')
    resolved = whenResolvedByPython(unresolved)
    assert resolved == 'self.cat'


def test_in_Java_FieldInitialization():
    unresolved = givenFieldInitialization('cat')
    resolved = whenResolvedByJava(unresolved)
    assert resolved == 'this.cat = cat;'


def test_in_Python_FieldInitialization():
    unresolved = givenFieldInitialization('cat')
    resolved = whenResolvedByPython(unresolved)
    assert resolved == 'self.cat = cat'


def givenFieldInitialization(name):
    fieldRef = givenFieldReference(name)
    param = givenUnresolved(UnresolvedVariableName, name)
    return AssignVariableToField(fieldRef, param)


def givenFieldReference(name):
    return FieldReference(givenUnresolved(UnresolvedVariableName, name))


def test_in_Java_Parameter():
    param = givenParameter('cat')
    resolved = whenResolvedByJava(param)
    assert resolved == 'Cat cat'


def test_in_Python_Parameter():
    param = givenParameter('cat')
    resolved = whenResolvedByPython(param)
    assert resolved == 'cat: Cat'


def test_in_Java_list_Parameter():
    param = givenListParameter('cat')
    resolved = whenResolvedByJava(param)
    assert resolved == 'List<Cat> catList'


def test_in_Python_list_Parameter():
    param = givenListParameter('cat')
    resolved = whenResolvedByPython(param)
    assert resolved == 'catList: [Cat]'


def givenParameter(name):
    symbol = makeSymbol(name)
    name = UnresolvedVariableName(symbol)
    type = UnresolvedTypeName(symbol)
    param = Parameter(name, type)
    return param


def givenListParameter(name):
    symbol = makeSymbol(name)
    name = UnresolvedListVariableName(symbol)
    type = UnresolvedListTypeName(symbol)
    param = Parameter(name, type)
    return param


def givenUnresolved(of, name, givenName='', isTerminal=False):
    symbol = makeSymbol(name=name, given=givenName, isTerminal=isTerminal)
    unresolvedName = of(symbol)
    return unresolvedName


def makeSymbol(name=None, given=None, isTerminal=None):
    return Symbol(
        name=name,
        givenName=given,
        isCapture=None,
        isTerminal=isTerminal
    )


def whenResolvedByDefault(unresolved):
    return whenResolve(unresolved, DefaultTranslator())


def whenResolvedByPython(unresolved):
    return whenResolve(unresolved, PythonTranslator())


def whenResolvedByJava(unresolved):
    return whenResolve(unresolved, JavaTranslator())


def whenResolve(unresolved, using):
    return unresolved.to(using)