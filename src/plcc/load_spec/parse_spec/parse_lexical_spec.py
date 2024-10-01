from dataclasses import dataclass
import re

from ..load_rough_spec.parse_lines import Line

@dataclass
class LexicalRule:
    line: Line
    isSkip: bool
    name: str
    pattern: str

@dataclass
class LexicalSpec:
    ruleList: [LexicalRule|Line]

def parse_lexical_spec(lines: list[Line]) -> LexicalSpec:
    lexical_spec = LexicalSpec([])

    if not lines:
        return lexical_spec

    patterns = compile_patterns()
    for line in lines:
        line_str = line.string.strip()
        blankOrComment = is_blank_or_comment(line_str)
        if blankOrComment:
            continue

        if skip_token_generates(line_str, line, patterns["skipToken"], lexical_spec):
            continue
        elif regular_token_generates(line_str, line, patterns["tokenToken"], lexical_spec):
            continue
        else:
            lexical_spec.ruleList.append(line)

    return lexical_spec

def compile_patterns() -> dict:
    return {
        'skipToken' : re.compile(r'^skip\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$'),
        'tokenToken' : re.compile(r'(?:^token\s+)?(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$')
    }

def is_blank_or_comment(line: str) -> bool:
    if line == '':
        return True
    elif line.startswith('#'):
        return True
    else:
        return False

def strip_quotes(pattern: str) -> str:
    pattern = pattern.strip('\'')
    pattern = pattern.strip('\"')
    return pattern

def skip_token_generates(line_str, line, skipPattern, lexical_spec) -> bool:
    skipMatches = re.match(skipPattern, line_str)
    if skipMatches:
        pattern = strip_quotes(skipMatches['Pattern'])
        newSkipRule = LexicalRule(line=line, isSkip=True, name=skipMatches['Name'], pattern=pattern)
        lexical_spec.ruleList.append(newSkipRule)
        return True
    else:
        return False

def regular_token_generates(line_str, line, tokenPattern, lexical_spec) -> bool:
    tokenMatches = re.match(tokenPattern, line_str)

    if tokenMatches:
        pattern = strip_quotes(tokenMatches['Pattern'])
        newTokenRule = LexicalRule(line=line, isSkip=False, name=tokenMatches['Name'], pattern=pattern)
        lexical_spec.ruleList.append(newTokenRule)
        return True
    else:
        return False
