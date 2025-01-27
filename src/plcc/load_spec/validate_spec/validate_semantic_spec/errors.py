from dataclasses import dataclass
from ...load_rough_spec.parse_lines import Line
from ...parse_spec.parse_semantic_spec import SemanticSpec, CodeFragment


@dataclass
class ValidationError:
    line: Line
    message: str

@dataclass
class InvalidClassNameError(ValidationError):
    def __init__(self, line):
        self.line = line
        self.message = f"Invalid name format for ClassName {self.line.string} on line: {self.line.number} (Must start with an upper case letter, and may contain upper or lower case letters, numbers, and underscores)."

@dataclass
class UndefinedBlockError(ValidationError):
    def __init__(self, line):
        self.line = line
        self.message = f"Undefined Block for {self.line.string} on line: {self.line.number}"

@dataclass
class UndefinedTargetLocatorError(ValidationError):
    def __init__(self, line):
        self.line = line
        self.message = f"Undefined class name for the Block on line: {self.line.number}"
