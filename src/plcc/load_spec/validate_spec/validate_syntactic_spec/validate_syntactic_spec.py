from dataclasses import dataclass
import re
from ...load_rough_spec.parse_lines import Line
from ...parse_spec.parse_syntactic_spec import SyntacticSpec, SyntacticRule


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

    def validate(self) -> list:
        if not self.syntacticSpec:
            return self.errorList
        for rule in self.syntacticSpec:
            self._handle(rule)
        return self.errorList

    def _handle(self, rule: SyntacticRule | Line):
        if isinstance(rule, SyntacticRule):
            print("todo!")
            # self.checkRuleOne(rule)
            # self._checkRuleTwo(rule)
            # self._checkRuleThree(rule)
        else:
            self._checkForLine(rule)

    def _checkForLine(self, line: Line):
        message = f"Invalid rule format found on line: {line.number}"
        self.errorList.append(ValidationError(line=line, message=message))
