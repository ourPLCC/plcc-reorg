class LL1Wrapper:
    def __init__(self, name: str, specObject: object):
        self.name = name
        self.specObject = specObject

    def __eq__(self, other):
        if self.specObject is None or other.specObject is None:
            return self is other
        return isinstance(other, LL1Wrapper) and self.name == other.name

    def __hash__(self):
        return hash(self.name)
