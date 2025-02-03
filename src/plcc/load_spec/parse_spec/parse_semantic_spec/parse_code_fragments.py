
from plcc.load_spec.structs import CodeFragment
from .parse_target_locator import parse_target_locator
from plcc.load_spec.structs import Line
from plcc.load_spec.structs import Block
from plcc.load_spec.structs import Divider
import re

def parse_code_fragments(lines_and_blocks: list[Line | Block]):
    parser = CodeFragmentParser(lines_and_blocks)
    return parser.parse()

class CodeFragmentParser:
    def __init__(self, linesAndBlocks: list[Line | Block]):
        self.linesAndBlocks = linesAndBlocks
        self.codeFragmentList = []
        self.currentCodeFragment = CodeFragment(targetLocator=None, block=None)

    def parse(self):
        for obj in self.linesAndBlocks:
            self._parseLineOrBlock(obj)
            if self._isCurrentCodeFragmentAttributesDefined():
                self._addCurrentCodeFragmentToList()
                self._resetCurrentCodeFragment()

        if self._isCurrentCodeFragmentTargetLocatorDefined() or self._isCurrentCodeFragmentBlockDefined():
            self._addCurrentCodeFragmentToList()

        return self.codeFragmentList

    def _parseLineOrBlock(self, obj):
        handler = {
                Line: self._parseLine,
                Block: self._parseBlock
            }.get(type(obj))

        handler(obj)

    def _parseLine(self, line):
        if self._isCommentOrBlank(line.string):
            return
        if self._isCurrentCodeFragmentTargetLocatorDefined():
            self._addCurrentCodeFragmentToList()
            self._resetCurrentCodeFragment()

        targetLocator = parse_target_locator(line)
        self._setCurrentCodeFragmentTargetLocator(targetLocator)

    def _parseBlock(self, block):
        if not self._isCurrentCodeFragmentTargetLocatorDefined() and self._isCurrentCodeFragmentBlockDefined():
            self._addCurrentCodeFragmentToList()
            self._resetCurrentCodeFragment()

        self.currentCodeFragment.block = block

        if not self._isCurrentCodeFragmentTargetLocatorDefined():
            self._addCurrentCodeFragmentToList()
            self._resetCurrentCodeFragment()

    def _setCurrentCodeFragmentTargetLocator(self, targetLocator):
        self.currentCodeFragment.targetLocator = targetLocator

    def _setCurrentCodeFragmentBlock(self, block):
        self.currentCodeFragment.block = block

    def _isCurrentCodeFragmentAttributesDefined(self):
        return True if self._isCurrentCodeFragmentTargetLocatorDefined() and self._isCurrentCodeFragmentBlockDefined() else False

    def _isCurrentCodeFragmentTargetLocatorDefined(self):
        return True if self.currentCodeFragment.targetLocator != None else False

    def _isCurrentCodeFragmentBlockDefined(self):
        return True if self.currentCodeFragment.block != None else False

    def _addCurrentCodeFragmentToList(self):
        self.codeFragmentList.append(self.currentCodeFragment)

    def _resetCurrentCodeFragment(self):
        self.currentCodeFragment = CodeFragment(targetLocator=None, block=None)

    def _isCommentOrBlank(self, obj_str):
        return True if re.match(r'\s*#', obj_str) or re.match(r'\s*$', obj_str) else False
