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

def parse_lexical_spec(lines):
    lexical_spec = LexicalSpec([])
    if lines == []:
        return lexical_spec
    if lines is None:
        return lexical_spec

    skipToken = re.compile(r'^skip\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$')
    tokenToken = re.compile(r'^token\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$')
    otherToken = re.compile(r'^(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$')
    for line in lines:
        l = line.string.strip()

        #Skip blank or empty Lines
        if l == '':
            continue
        if re.match(r'^\s*#.*$', l):
            continue


        skipMatches = re.match(skipToken, l)
        if skipMatches:
            newSkipRule = skipTokenGenerator(line, skipMatches['Name'], skipMatches['Pattern'])
            lexical_spec.ruleList.append(newSkipRule)
            continue

        tokenMatches = re.match(tokenToken, l)
        if tokenMatches:
            newTokenRule = tokenGenerator(line, tokenMatches['Name'], tokenMatches['Pattern'])
            lexical_spec.ruleList.append(newTokenRule)
            continue

        otherTokenMatches = re.match(otherToken, l)
        if otherTokenMatches:
            newTokenRule = tokenGenerator(line, otherTokenMatches['Name'], otherTokenMatches['Pattern'])
            lexical_spec.ruleList.append(newTokenRule)
            continue

        lexical_spec.ruleList.append(line)

    return lexical_spec

def skipTokenGenerator(line, name, pattern):
    pattern = pattern.strip('\'')
    pattern = pattern.strip('\"')
    return LexicalRule(line=line, isSkip=True, name=name, pattern=pattern)

def tokenGenerator(line, name, pattern):
    pattern = pattern.strip('\'')
    pattern = pattern.strip('\"')
    return LexicalRule(line=line, isSkip=False, name=name, pattern=pattern)
