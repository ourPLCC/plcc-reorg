from dataclasses import dataclass
from typing import List
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
        lhs_error_list, non_terminal_set = SyntacticLhsValidator(self.syntacticSpec).validate()
        if lhs_error_list:
            self.errorList = (lhs_error_list)
        self.nonTerminals = non_terminal_set



class SyntacticLhsValidator:
    syntacticSpec: SyntacticSpec

    def __init__(self, syntacticSpec: SyntacticSpec):
        self.syntacticSpec = syntacticSpec
        self.errorList = []
        self.nonTerminals = set()

    def validate(self):
        for rule in self.syntacticSpec:
            self._check(rule)
        return self.errorList, self.nonTerminals

    def _check(self, rule: SyntacticRule):
        resolved_name = rule.lhs.name.capitalize()
        self._checkName(rule)
        if rule.lhs.altName:
            self._checkAltName(rule)
            resolved_name = rule.lhs.altName
        self._appendNonTerminals(rule, resolved_name)

    def _checkName(self, rule: SyntacticRule):
        if not re.match(r"^[a-z][a-zA-Z0-9_]+$", rule.lhs.name):
            self._appendInvalidLhsNameError(rule)

    def _checkAltName(self, rule: SyntacticRule):
        if not re.match(r"^[A-Z][a-zA-Z0-9_]+$", rule.lhs.altName):
            self._appendInvalidLhsAltNameError(rule)

    def _appendNonTerminals(self, rule: SyntacticRule, non_terminal: str):
        if non_terminal in self.nonTerminals:
            self._appendDuplicateLhsError(rule)
        self.nonTerminals.add(non_terminal)

    def _appendInvalidLhsNameError(self, rule: SyntacticRule):
        message = f"Invalid LHS name format for rule: '{rule.line.string}' (must start with a lower-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))

    def _appendInvalidLhsAltNameError(self, rule: SyntacticRule):
        message = f"Invalid LHS alternate name format for rule: '{rule.line.string}' (must start with a upper-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))

    def _appendDuplicateLhsError(self, rule: SyntacticRule):
        message = f"Duplicate lhs name: '{rule.line.string}' on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))
