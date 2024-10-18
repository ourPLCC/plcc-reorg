from dataclasses import dataclass
import re
from ...load_rough_spec.parse_lines import Line
from ...parse_spec.parse_syntactic_spec import SyntacticSpec, SyntacticRule, LhsNonTerminal


@dataclass
class ValidationError:
    line: Line
    message: str


def validate_syntactic_spec(syntacticSpec: SyntacticSpec):
    return SyntacticValidator(syntacticSpec).validate()


class SyntacticValidator:
    syntacticSpec: SyntacticSpec

    def __init__(self, syntacticSpec: SyntacticSpec):
        self.syntacticSpec = syntacticSpec
        self.errorList = []
        self.nonTerminals = set()

    def validate(self) -> list:
        if not self.syntacticSpec:
            return self.errorList
        self._validateLhs()
        return self.errorList

    def _validateLhs(self):
        lhs_error_list, non_terminal_set = SyntacticLhsValidator(self.syntacticSpec.copy()).validate()
        if lhs_error_list:
            self.errorList = (lhs_error_list)
        self.nonTerminals = non_terminal_set



class SyntacticLhsValidator:
    spec: SyntacticSpec

    def __init__(self, syntacticSpec: SyntacticSpec):
        self.spec = syntacticSpec
        self.errorList = []
        self.nonTerminals = set()

    def validate(self):
        while len(self.spec) > 0:
            self.rule = self.spec.pop(0)
            self._checkLine()
        return self.errorList, self.nonTerminals

    def _checkLine(self):
        name, alt_name = self._getNames()
        self._checkName(name)
        if alt_name:
            self._checkAltName(alt_name)
        self._checkDuplicates()

    def _getNames(self):
        return (
            self.rule.lhs.name,
            self.rule.lhs.altName
        )

    def _checkName(self, name: str):
        if not re.match(r"^[a-z][a-zA-Z0-9_]+$", name):
            self._appendInvalidLhsNameError()

    def _checkAltName(self, alt_name: str):
        if not re.match(r"^[A-Z][a-zA-Z0-9_]+$", alt_name):
            self._appendInvalidLhsAltNameError()

    def _getResolvedName(self):
        name, alt_name = self._getNames()
        return alt_name if alt_name else name.capitalize()

    def _checkDuplicates(self):
        name = self._getResolvedName()
        if name in self.nonTerminals:
            self._appendDuplicateLhsError()
        self.nonTerminals.add(name)

    def _appendInvalidLhsNameError(self):
        rule = self.rule
        message = f"Invalid LHS name format for rule: '{rule.line.string}' (must start with a lower-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))

    def _appendInvalidLhsAltNameError(self):
        rule = self.rule
        message = f"Invalid LHS alternate name format for rule: '{rule.line.string}' (must start with a upper-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))

    def _appendDuplicateLhsError(self):
        rule = self.rule
        message = f"Duplicate lhs name: '{rule.line.string}' on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))
