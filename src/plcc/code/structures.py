from __future__ import annotations
from dataclasses import dataclass, field

from ..spec.bnfrule import BnfRule


@dataclass(frozen=True)
class Module:
    classes: [Class] = field(default_factory=list)


@dataclass(frozen=True)
class Class:
    name: UnresolvedClassName | ClassName
    extends: UnresolvedBaseClassName = None
    fields: [FieldDeclaration] = field(default_factory=list)
    constructor: Constructor = None


@dataclass(frozen=True)
class ClassName:
    name: str


@dataclass(frozen=True)
class FieldDeclaration:
    name: UnresolvedVariableName
    type: UnresolvedTypeName


@dataclass(frozen=True)
class Constructor:
    className: UnresolvedClassName
    parameters: [Parameter]
    body: [FieldInitialization]


@dataclass(frozen=True)
class Parameter:
    name: UnresolvedVariableName | UnresolvedListVariableName
    type: UnresolvedTypeName | UnresolvedListTypeName

    def to(self, language):
        name = self.name.to(language)
        type = self.type.to(language)
        return language.toParameter(name=name, type=type)


@dataclass(frozen=True)
class AssignVariableToField:
    lhs: FieldReference
    rhs: UnresolvedVariableName

    def to(self, language):
        field = self.lhs.to(language)
        parameter = self.rhs.to(language)
        return language.toAssignmentStatement(field, parameter)


@dataclass(frozen=True)
class FieldReference:
    name: UnresolvedVariableName

    def to(self, language):
        name = self.name.to(language)
        return language.toFieldReference(name)


@dataclass(frozen=True)
class UnresolvedTypeName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.isTerminal:
            return language.toTypeName('Token')
        else:
            return language.toTypeName(self.symbol.name)


@dataclass(frozen=True)
class UnresolvedListTypeName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.isTerminal:
            return language.toListTypeName('Token')
        else:
            elementTypeName = UnresolvedTypeName(self.symbol).to(language)
            return language.toListTypeName(elementTypeName)


@dataclass(frozen=True)
class UnresolvedVariableName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.toVariableName(self.symbol.name)


@dataclass(frozen=True)
class UnresolvedListVariableName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.toListVariableName(self.symbol.name)


@dataclass(frozen=True)
class UnresolvedClassName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.toClassName(self.symbol.name)


@dataclass(frozen=True)
class UnresolvedBaseClassName:
    symbol: Symbol

    def to(self, language):
        return language.toBaseClassName(self.symbol.name)


