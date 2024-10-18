from pytest import raises, mark, fixture
from .LL1Wrapper import LL1Wrapper

@fixture
def specObject():
    return object()

@fixture
def symbolName():
    return 'symbolName'

def test_wrapper_init(symbolName, specObject):
    wrapper = createWrapper(symbolName, specObject)
    assert wrapper.name == symbolName
    assert wrapper.specObject == specObject



def createWrapper(symbolName, specObject):
    return LL1Wrapper(symbolName, specObject)
