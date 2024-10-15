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
        for rule in self.syntacticSpec:
            self._handleLHS(rule)
        # for rule in self.syntacticSpec:
            # self._handleRHS(rule)
        return self.errorList

    def _handleLHS(self, rule: SyntacticRule | Line):
        if isinstance(rule, SyntacticRule):
            self._checkLHS(rule)
        else:
            self._checkForLine(rule)

    def _checkLHS(self, rule: SyntacticRule):
        resolved_name = rule.lhs.name
        self._checkLHSNonTerminalName(rule)
        if rule.lhs.altName:
            self._checkLHSNonTerminalAltName(rule)
            resolved_name = rule.lhs.altName
        self._appendNonTerminals(resolved_name)

    def _checkLHSNonTerminalName(self, rule: SyntacticRule):
        if not re.match(r"^[a-z][a-zA-Z0-9_]+$", rule.lhs.name):
            self._appendInvalidLhsNameError(rule)

    def _checkLHSNonTerminalAltName(self, rule: SyntacticRule):
        if not re.match(r"^[A-Z][a-zA-Z0-9_]+$", rule.lhs.altName):
            self._appendInvalidLhsAltNameError(rule)

    def _appendNonTerminals(self, resolved_name: str):
        pass

    def _checkForLine(self, line: Line):
        message = f"Invalid rule format found on line: {line.number}"
        self.errorList.append(ValidationError(line=line, message=message))

    def _appendInvalidLhsNameError(self, rule: SyntacticRule):
        message = f"Invalid LHS name format for rule: '{rule.line.string}' (must start with a lower-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))

    def _appendInvalidLhsAltNameError(self, rule: SyntacticRule):
        message = f"Invalid LHS alternate name format for rule: '{rule.line.string}' (must start with a upper-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"
        self.errorList.append(ValidationError(line=rule.line, message=message))
