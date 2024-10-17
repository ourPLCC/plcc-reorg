from dataclasses import dataclass

@dataclass
class ValidationError:
    message: str

class InvalidParameterError(Exception):
    def __init__(self, param):
        super().__init__(param)