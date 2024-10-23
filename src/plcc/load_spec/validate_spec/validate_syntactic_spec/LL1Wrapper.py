class LL1Wrapper:
    def __init__(self, name: str, specObject: object):
        self.name = name
        self.specObject = specObject

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, LL1Wrapper):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
