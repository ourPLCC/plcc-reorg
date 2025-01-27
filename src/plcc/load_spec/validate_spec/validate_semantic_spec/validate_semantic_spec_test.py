from pytest import raises, mark, fixture
from .validate_semantic_spec import InvalidClassNameError, UndefinedBlockError, UndefinedTargetLocatorError, validate_semantic_spec
from ...parse_spec.parse_semantic_spec import SemanticSpec, parse_semantic_spec
from ...load_rough_spec.parse_lines import Line, parse_lines
from ...load_rough_spec.parse_dividers import Divider
from ...load_rough_spec.parse_blocks import Block



def test_valid_names_no_errors():
    assertValidClassNames(["Class","CLASS","C_lass_","C123","C", "ClaSs", "C_la55"])

def test_no_code_fragments_no_errors():
    semanticSpec = makeSemanticSpec([])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 0

def test_begin_lowercase_format_error():
    assertInvalidClassName("startsLowerCase")

def test_begin_number_format_error():
    assertInvalidClassName("12MustStartUppercase")

def test_whitespace_name_format_error():
    assertInvalidClassName("White Space")

def test_multiple_errors_all_counted():
    assertMultipleInvalidClassNames(["123StartsWithNumbers", "notuppercase", "InvalidChar`", "Invalid space"])

def test_valid_and_invalid_names():
    invalidNameLine = makeLine("invalid")
    semanticSpec = makeSemanticSpec([makeLine("Class"), makeBlock(), invalidNameLine, makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidClassNameError(invalidNameLine)

def test_invalid_block_and_target_locator_order():
    line = makeLine("Class")
    lines_and_blocks = [makeBlock(), line]
    semanticSpec = makeSemanticSpec(lines_and_blocks)
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 2
    assert errors[0] == makeUndefinedTargetLocatorError(lines_and_blocks[0].lines[0])
    assert errors[1] == makeUndefinedBlockError(line)

def test_invalid_undefined_target_locator():
    lines_and_blocks = [makeBlock()]
    semanticSpec = makeSemanticSpec(lines_and_blocks)
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1
    assert errors[0] == makeUndefinedTargetLocatorError(lines_and_blocks[0].lines[0])

def test_undefined_block_error_multiple_code_fragments():
    line = makeLine("Class")
    semanticSpec = makeSemanticSpec([line, makeLine("AnotherClass"), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1
    assert errors[0] == makeUndefinedBlockError(line)

def test_undefined_block_error_single_code_fragment():
    line = makeLine("Class")
    semanticSpec = makeSemanticSpec([line])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1
    assert errors[0] == makeUndefinedBlockError(line)

def assertValidClassNames(names: list[str]):
    for name in names:
        assertValidClassName(name)

def assertValidClassName(name: str):
    semanticSpec = makeSemanticSpec([makeLine(name), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 0

def assertInvalidClassName(name: str):
    line = makeLine(name)
    semanticSpec = makeSemanticSpec([line, makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidClassNameError(line)

def assertMultipleInvalidClassNames(strings):
    lines_and_blocks = makeLinesAndBlocksFromStrings(strings)
    semanticSpec = makeSemanticSpec(lines_and_blocks)
    errors = validate_semantic_spec(semanticSpec)
    for i, obj in enumerate(lines_and_blocks):
        if type(obj) is Block:
            return
        assert errors[i] == makeInvalidClassNameError(obj)
    else: # pragma: no cover
        pass

def makeLinesAndBlocksFromStrings(strings: list[str]) -> list[Line | Block]:
    lines_and_blocks = []
    for string in strings:
        lines_and_blocks.append(makeLine(string))
        lines_and_blocks.append(makeBlock())
    return lines_and_blocks

def makeInvalidClassNameError(line: Line):
    return InvalidClassNameError(line)

def makeUndefinedBlockError(line: Line):
    return UndefinedBlockError(line)

def makeUndefinedTargetLocatorError(line: Line):
    return UndefinedTargetLocatorError(line)

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
