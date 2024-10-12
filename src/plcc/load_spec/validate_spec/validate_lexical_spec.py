from dataclasses import dataclass
import re
from ..load_rough_spec.parse_lines import Line
from ..parse_spec.parse_lexical_spec import LexicalSpec, LexicalRule

@dataclass
class ValidationError:
    line: Line
    message: str

def validate_lexical_spec(lexicalSpec: LexicalSpec):
    return LexicalValidator(lexicalSpec).validate()

class LexicalValidator:
    def __init__(self, lexicalSpec: LexicalSpec):
        self.lexicalSpec = lexicalSpec
        self.errorList = []
        self.names = set()
        self.patterns = set()
        self.namePattern = re.compile(r'^[A-Z_][A-Z0-9_]*$')

    def validate(self) -> list:
        if not self.lexicalSpec or not self.lexicalSpec.ruleList:
            return self.errorList
        for rule in self.lexicalSpec.ruleList:
            self._handle(rule)
        return self.errorList

    def _handle(self, rule: LexicalRule | Line):
        if isinstance(rule, LexicalRule):
            self._checkNameFormat(rule)
            self._checkDuplicates(rule)
            self._checkPatternFormat(rule)
        else:
            self._checkForLine(rule)

    def _checkNameFormat(self, rule: LexicalRule):
        if not self.namePattern.match(rule.name):
            message = f"Invalid name format for rule '{rule.name}' (Must be uppercase letters, numbers, and underscores, and cannot start with a number) on line: {rule.line.number}"
            self.errorList.append(ValidationError(line=rule.line, message=message))

    def _checkDuplicates(self, rule: LexicalRule):
        hasDuplicateName = self._checkDuplicateNames(rule)
        hasDuplicateRule = self._checkDuplicateRules(rule)
        if hasDuplicateName:
            message = f"Duplicate rule name found '{rule.name}' on line: {rule.line.number}"
            self.errorList.append(ValidationError(line=rule.line, message=message))
        if hasDuplicateRule:
            message = f"Duplicate rule pattern found '{rule.pattern}' on line: {rule.line.number}"
            self.errorList.append(ValidationError(line=rule.line, message=message))

    def _checkDuplicateNames(self, rule: LexicalRule) -> bool:
        if rule.name in self.names:
            return True
        else:
            self.names.add(rule.name)
            return False

    def _checkDuplicateRules(self, rule: LexicalRule) -> bool:
        if rule.pattern in self.patterns:
            return True
        else:
            self.patterns.add(rule.pattern)
            return False

    def _checkPatternFormat(self, rule: LexicalRule):
        if rule.pattern == '\"' or rule.pattern == '\'':
            message = f"Duplicate pattern format found '{rule.pattern}' on line: {rule.line.number} (Patterns can not contain closing closing quotes)"
            self.errorList.append(ValidationError(line=rule.line, message=message))


    def _checkForLine(self, line: Line):
        message = f"Invalid rule format found on line: {line.number}"
        self.errorList.append(ValidationError(line=line, message=message))
