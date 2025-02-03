
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
    def __init__(self, lines_and_blocks: list[Line | Block]):
        self.lines_and_blocks = lines_and_blocks
        self.codeFragmentList = []
        self.targetLocator = None

    def parse(self):
        for obj in self.lines_and_blocks:
            self._parse_line_or_block(obj)

        if self._is_target_locator_missing_associated_block():
            self._parse_with_undefined_block()

        return self.codeFragmentList

    def _parse_line_or_block(self, obj):
        handler = {
                Line: self._parse_line,
                Block: self._parse_block
            }.get(type(obj))

        handler(obj)

    def _parse_block(self, block):
        self._add_code_fragment(block)
        self._reset_target_locator_attribute_to_none()

    def _parse_line(self, line):
        if self._is_comment_or_blank(line.string):
            return

        if self.targetLocator != None:
            self._parse_with_undefined_block()
        self.targetLocator = parse_target_locator(line)

    def _add_code_fragment(self, block):
        self.codeFragmentList.append(CodeFragment(targetLocator=self.targetLocator, block=block))

    def _reset_target_locator_attribute_to_none(self):
        self.targetLocator = None

    def _parse_with_undefined_block(self):
        self.codeFragmentList.append(CodeFragment(targetLocator=self.targetLocator, block=None))

    def _is_comment_or_blank(self, obj_str):
        return True if re.match(r'\s*#', obj_str) or re.match(r'\s*$', obj_str) else False

    def _is_target_locator_missing_associated_block(self):
        return True if self.targetLocator != None else False
