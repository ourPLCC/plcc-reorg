from .default import DefaultTranslator


class PythonTranslator(DefaultTranslator):
    def toListTypeName(self, name):
        return f'[{name}]'

    def toFieldReference(self, name):
        return f'self.{name}'

    def toAssignmentStatement(self, lhs, rhs):
        return f'{lhs} = {rhs}'

    def toParameter(self, name, type):
        return f'{name}: {type}'