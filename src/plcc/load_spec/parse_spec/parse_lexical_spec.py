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

    patterns = compilePatterns()
    for line in lines:
        l = line.string.strip()
        blankOrComment = isBlankOrComment(l)
        if blankOrComment:
            continue

        if skipTokenGenerates(l, line, patterns["skipToken"], lexical_spec):
            continue
        elif regularTokenGenerates(l, line, patterns["tokenToken"], lexical_spec):
            continue
        else:
            lexical_spec.ruleList.append(line)

    return lexical_spec



def compilePatterns() -> dict:
    return {
        'skipToken' : re.compile(r'^skip\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$'),
        'tokenToken' : re.compile(r'(?:^token\s+)?(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$')
    }

def isBlankOrComment(line: str) -> bool:
    if line == '':
        return True
    elif line.startswith('#'):
        return True
    else:
        return False

def stripQuotes(pattern: str) -> str:
    pattern = pattern.strip('\'')
    pattern = pattern.strip('\"')
    return pattern

def skipMatches(line, skipPattern):
    if re.match(skipPattern, line):
        return True
    else:
        return False

def skipTokenGenerates(line_str, line, skipPattern, lexical_spec):
    skipMatches = re.match(skipPattern, line_str)
    if skipMatches:
        pattern = stripQuotes(skipMatches['Pattern'])
        newSkipRule = LexicalRule(line=line, isSkip=True, name=skipMatches['Name'], pattern=pattern)
        lexical_spec.ruleList.append(newSkipRule)
        return True
    else:
        return False

def regularTokenGenerates(line_str, line, tokenPattern, lexical_spec):
    tokenMatches = re.match(tokenPattern, line_str)

    if tokenMatches:
        pattern = stripQuotes(tokenMatches['Pattern'])
        newTokenRule = LexicalRule(line=line, isSkip=False, name=tokenMatches['Name'], pattern=pattern)
        lexical_spec.ruleList.append(newTokenRule)
        return True
    else:
        return False
