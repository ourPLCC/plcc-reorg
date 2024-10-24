import pytest


from plcc.spec.symbol import Symbol


from plcc.code.presenter import JavaPresenter
from plcc.code.presenter import PythonPresenter


from plcc.code import BaseClassName
from plcc.code import ClassName
from plcc.code import TypeName
from plcc.code import VariableName
from plcc.code import ListVariableName
from plcc.code import ListTypeName
from plcc.code import FieldReference
from plcc.code import AssignVariableToField
from plcc.code import Parameter
from plcc.code import Constructor
from plcc.code import FieldDeclaration
from plcc.code import StrClassName
from plcc.code import Class


def test_InJava_Class():
    unrendered = givenClass(name='cat', fields=['tail', 'claws'])
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == '''\
public class Cat {
    public Tail tail;
    public Claws claws;

    public Cat(Tail tail, Claws claws) {
        this.tail = tail;
        this.claws = claws;
    }
}
'''


def test_InJava_Class_with_extends():
    unrendered = givenClass(name='cat', fields=['tail', 'claws'], extends='animal')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == '''\
public class Cat extends Animal {
    public Tail tail;
    public Claws claws;

    public Cat(Tail tail, Claws claws) {
        this.tail = tail;
        this.claws = claws;
    }
}
'''


def test_InPython_Class():
    unrendered = givenClass(name='cat', fields=['tail', 'claws'])
    rendered = whenRenderedWithPython(unrendered)
    assert rendered == '''\
class Cat:
    def __init__(self, tail: Tail, claws: Claws):
        self.tail = tail
        self.claws = claws
'''


def test_InPython_Class_with_extends():
    unrendered = givenClass(name='cat', fields=['tail', 'claws'], extends='animal')
    rendered = whenRenderedWithPython(unrendered)
    assert rendered == '''\
class Cat(Animal):
    def __init__(self, tail: Tail, claws: Claws):
        self.tail = tail
        self.claws = claws
'''


def test_TypeName_resolves_to_capitalized_symbol_name():
    unrendered = givenTypeName(name='cat', givenName='pet')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'Cat'


def test_VariableName_resolves_to_symbol_given_name():
    unrendered = givenVariableName(name='cat', givenName='pet')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'pet'


def test_VariableName_if_no_given_name_resolves_to_symbol_name():
    unrendered = givenVariableName(name='cat', givenName=None)
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'cat'


def test_TypeName_if_terminal_resolves_to_Token():
    unrendered = givenTypeName(name='cat', givenName='pet', isTerminal=True)
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'Token'


def test_ClassName_resolves_to_symbol_given_name():
    unrendered = givenClassName(name='cat', givenName='pet')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'pet'


def test_ClassName_resolves_to_capitalized_symbol_name_if_no_given_name():
    unrendered = givenClassName(name='cat', givenName=None)
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'Cat'


def test_BaseClassName_resolves_to_capitalized_symbol_name():
    unrendered = givenBaseClassName(name='cat', givenName='Pet')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'Cat'


def test_ListVariableName_resolves_to_given_name():
    unrendered = givenListVariableName(name='cat', givenName='fluffy')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'fluffy'


def test_ListVariableName_if_no_given_name_resolves_to_symbol_name_appended_with_List():
    unrendered = givenListVariableName(name='cat', givenName='')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'catList'


def test_in_Java_ListTypeName_resolves_to_List_parameterized_by_its_rendered_type_name():
    unrendered = givenListTypeName(name='cat', givenName='fluffy')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'List<Cat>'


def test_in_Python_ListTypeName_resolves_to_square_brackets_containing_its_rendered_type_name():
    unrendered = givenListTypeName(name='cat', givenName='fluffy')
    rendered = whenRenderedWithPython(unrendered)
    assert rendered == '[Cat]'


def test_inJava_ListTypeName_for_terminals_renders_to_list_of_Token():
    unrendered = givenListTypeName(name='cat', givenName='fluffy', isTerminal=True)
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'List<Token>'
    rendered = whenRenderedWithPython(unrendered)
    assert rendered == '[Token]'


def test_in_Java_FieldReference_resolves_to_this_dot_variable_name():
    unrendered = givenFieldReference('cat')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'this.cat'


def test_in_Python_FieldReference_resolves_to_self_dot_variable_name():
    unrendered = givenFieldReference('cat')
    rendered = whenRenderedWithPython(unrendered)
    assert rendered == 'self.cat'


def test_in_Java_FieldInitialization():
    unrendered = givenAssignVariableToField('cat')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'this.cat = cat;'


def test_in_Python_FieldInitialization():
    unrendered = givenAssignVariableToField('cat')
    rendered = whenRenderedWithPython(unrendered)
    assert rendered == 'self.cat = cat'


def test_in_Java_Parameter():
    param = givenParameter('cat')
    rendered = whenRenderedWithJava(param)
    assert rendered == 'Cat cat'


def test_in_Python_Parameter():
    param = givenParameter('cat')
    rendered = whenRenderedWithPython(param)
    assert rendered == 'cat: Cat'


def test_in_Java_list_Parameter():
    param = givenListParameter('cat')
    rendered = whenRenderedWithJava(param)
    assert rendered == 'List<Cat> catList'


def test_in_Python_list_Parameter():
    param = givenListParameter('cat')
    rendered = whenRenderedWithPython(param)
    assert rendered == 'catList: [Cat]'


def test_in_Java_constructor():
    constructor = givenConstructor('cat', ['fur', 'tail', 'claws'])
    rendered = whenRenderedWithJava(constructor)
    assert rendered == '''\
public Cat(Fur fur, Tail tail, Claws claws) {
    this.fur = fur;
    this.tail = tail;
    this.claws = claws;
}
'''


def test_in_Python_constructor():
    constructor = givenConstructor('cat', ['fur', 'tail', 'claws'])
    rendered = whenRenderedWithPython(constructor)
    assert rendered == '''\
def __init__(self, fur: Fur, tail: Tail, claws: Claws):
    self.fur = fur
    self.tail = tail
    self.claws = claws
'''


def test_in_Java_FieldDeclaration():
    decl = givenFieldDeclaration('cat')
    rendered = whenRenderedWithJava(decl)
    assert rendered == 'public Cat cat;'


def test_in_Python_FieldDeclaration_is_done_in_constructor_so_empty():
    decl = givenFieldDeclaration('cat')
    rendered = whenRenderedWithPython(decl)
    assert rendered == ''


def test_StrClassName_renders_to_its_name():
    unrendered = StrClassName('cat')
    rendered = whenRenderedWithJava(unrendered)
    assert rendered == 'cat'


def givenClass(name, fields, extends=None):
    fieldDecls = [givenFieldDeclaration(f) for f in fields]
    return Class(
        name=givenClassName(name),
        extends=None if extends is None else givenClassName(extends),
        fields=fieldDecls,
        constructor=givenConstructor(name, fields)
    )

def givenFieldDeclaration(name):
    return FieldDeclaration(
        givenVariableName(name=name),
        givenTypeName(name=name)
    )


def givenFieldReference(name):
    return FieldReference(given(VariableName, name))


def givenParameter(name):
    symbol = makeSymbol(name)
    name = VariableName(symbol)
    type = TypeName(symbol)
    param = Parameter(name, type)
    return param


def givenListParameter(name):
    symbol = makeSymbol(name)
    name = ListVariableName(symbol)
    type = ListTypeName(symbol)
    param = Parameter(name, type)
    return param


def givenConstructor(name, fields):
    className = givenClassName(name=name)
    params = []
    for f in fields:
        p = givenParameter(f)
        params.append(p)
    assignments = []
    for f in fields:
        a = givenAssignVariableToField(f)
        assignments.append(a)
    return Constructor(className, params, assignments)


def givenAssignVariableToField(name):
    fieldRef = givenFieldReference(name)
    param = given(VariableName, name)
    return AssignVariableToField(fieldRef, param)


def givenTypeName(name='', givenName='', isTerminal=False):
    return given(type=TypeName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenVariableName(name='', givenName='', isTerminal=False):
    return given(type=VariableName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenClassName(name='', givenName='', isTerminal=False):
    return given(type=ClassName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenBaseClassName(name='', givenName='', isTerminal=False):
    return given(type=BaseClassName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenListVariableName(name='', givenName='', isTerminal=False):
    return given(type=ListVariableName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenListTypeName(name='', givenName='', isTerminal=False):
    return given(type=ListTypeName, name=name, givenName=givenName, isTerminal=isTerminal)


def given(type, name, givenName='', isTerminal=False):
    symbol = makeSymbol(name=name, given=givenName, isTerminal=isTerminal)
    unrenderedName = type(symbol)
    return unrenderedName


def makeSymbol(name=None, given=None, isTerminal=None):
    return Symbol(
        name=name,
        givenName=given,
        isCapture=None,
        isTerminal=isTerminal
    )


def whenRenderedWithDefault(unrendered):
    return whenRendered(unrendered, Default())


def whenRenderedWithPython(unrendered):
    return whenRendered(unrendered, PythonPresenter())


def whenRenderedWithJava(unrendered):
    return whenRendered(unrendered, JavaPresenter())


def whenRendered(unrendered, withLanguage):
    return withLanguage.present(unrendered)
