from pytest import raises, mark, fixture
from .validate_semantic_spec import InvalidClassNameError, validate_semantic_spec
from ...parse_spec.parse_semantic_spec import SemanticSpec, parse_semantic_spec
from ...load_rough_spec.parse_lines import Line, parse_lines
from ...load_rough_spec.parse_dividers import Divider
from ...load_rough_spec.parse_blocks import Block


def test_empty_no_errors():
    semanticSpec = makeSemanticSpec([])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 0

def test_valid_name_no_error():
    semanticSpec = makeSemanticSpec([makeLine("Class"), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 0

def test_multiple_errors(): #UPDATE REGEX
    semanticSpec = makeSemanticSpec([makeLine("123Class"), makeBlock(), makeLine("invalidClass"), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 2


def test_target_locator_must_start_uppercase(): #UPDATE REGEX
    semanticSpec = makeSemanticSpec([makeLine("class"), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1

# def test_multiple_invalid_target_locators_returned():
#     semanticSpec = makeSemanticSpec()


def makeSemanticSpec(linesAndBlocks: list[Line | Block]):
    return parse_semantic_spec([makeDivider('Java', 'Java', makeLine("%"))] + linesAndBlocks)


def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)

def makeBlock():
    return  Block(list(parse_lines('''\
%%%
block
%%%
''')))

def makeDivider(tool, language, line):
    return Divider(tool=tool, language=language, line=line)
