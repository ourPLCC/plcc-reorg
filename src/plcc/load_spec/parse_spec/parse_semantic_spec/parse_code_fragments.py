from plcc.load_spec.structs import CodeFragment
from plcc.load_spec.structs import TargetLocator
from plcc.load_spec.structs import Line
from plcc.load_spec.structs import Block
from .parse_target_locator import parse_target_locator

def parse_code_fragments(lines_and_blocks):
    locators_and_blocks = parse_locators(lines_and_blocks)
    return list(parse_fragments(locators_and_blocks))

def parse_locators(lines_and_blocks):
    for lob in lines_and_blocks:
        if not isEmpty(lob):
            yield parse_target_locator(lob) if isinstance(lob, Line) else lob

def parse_fragments(lobs):
    lobs = list(lobs)
    i = 0
    while i < len(lobs):
        if isLocator(lobs, i) and isBlock(lobs, i+1):
            yield CodeFragment(lobs[i], lobs[i+1])
            i += 2
        elif isLocator(lobs, i) and isLocator(lobs, i+1):
            yield CodeFragment(lobs[i], None)
            i += 1
        elif isBlock(lobs, i) and isBlock(lobs, i+1):
            yield CodeFragment(None, lobs[i])
            i += 1
        elif isBlock(lobs, i) and isLocator(lobs, i+1):
            yield CodeFragment(None, lobs[i])
            i += 1
        elif isLocator(lobs, i):
            yield CodeFragment(lobs[i], None)
            i += 1
        elif isBlock(lobs, i):
            yield CodeFragment(None, lobs[i])
            i += 1
        else:
            raise TypeError(f'{type(lobs[i])}')

def isBlock(lobs, i):
    return isType(lobs, i, Block)

def isLocator(lobs, i):
    return isType(lobs, i, TargetLocator)

def isType(lobs, i, Type):
    return i < len(lobs) and isinstance(lobs[i], Type)

def isEmpty(lob):
    if lob is None:
        return True
    if isinstance(lob, Line):
        s = lob.string
        return s is None or s.strip() == ''
    return False
