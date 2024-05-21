from __future__ import annotations
from dataclasses import dataclass, replace
import pathlib
import re


def readLinesFromSpecFile(pathStr):
    lines = readLinesFromFile(pathStr)
    lines = markBlocks(lines)
    lines = ignoreCommentLines(lines)
    lines = ignoreBlankLines(lines)
    lines = processIncludes(lines, basePathStr=pathStr)
    return lines


def readLinesFromFile(pathStr):
    pathStr = resolveRelativePath(pathStr, pathlib.Path.cwd())
    path = pathlib.Path(pathStr)
    with path.open(mode='r') as file:
        for number, line in enumerate(file, start=1):
            yield Line(path,number,line.rstrip())


def markBlocks(lines, brackets=None):
    brackets = {
        '%%%': '%%%',
        '%%{': '%%}'
    } if brackets is None else brackets
    isInBlock = False
    close = None

    def mark(line):
        nonlocal isInBlock
        nonlocal close
        nonlocal brackets

        s = line.string.strip()
        if not close:
            if s in brackets:
                close = brackets[s]
        elif s == close:
            close = None
        else:
            line = line.markIsInBlock()
        return line

    return map(mark, lines)


def ignoreCommentLines(lines):
    def isComment(line):
        s = line.string.strip()
        return not line.isInBlock and s and s[0] == '#'
    return filter(lambda line: not isComment(line), lines)


def ignoreBlankLines(lines):
    def isBlankLine(line):
        s = line.string.strip()
        return not line.isInBlock and not s
    return filter(lambda line: not isBlankLine(line), lines)


INCLUDE = re.compile(r'^%include\s+(?P<path>.*)$')
def processIncludes(lines, basePathStr, stack=None, pattern=None):
    if pattern is None:
        pattern = INCLUDE
    if stack is None:
        stack = [ str(pathlib.Path(basePathStr).resolve()) ]
    for line in lines:
        m = pattern.match(line.string)
        if m:
            pathStr = resolveRelativePath(m['path'], basePathStr)
            if pathStr in stack:
                raise CircularIncludeException(line)
            stack.append(pathStr)
            with path.open(mode='r') as f:
                yield from processIncludes(readLinesFromFile(f, s), s, stack, pat)
            stack.pop()
        else:
            yield line


@dataclass(frozen=True)
class Line:
    path: str
    number: int
    string: str
    isInBlock: bool = False

    def markIsInBlock(self) -> Line:
        return replace(self, isInBlock=True)


def strToLines(string):
    path='// string //'
    for i, s in enumerate(string.splitlines(), start=1):
        yield Line(path, i, s, isInBlock=False)


def resolveRelativePath(pathStr, basePathStr):
    path = Path(pathStr)
    if path.is_absolute():
        return pathStr
    return str((Path(basePathStr).resolve() / path).resolve())
