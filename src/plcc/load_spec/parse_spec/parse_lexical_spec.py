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
    ruleList: [LexicalRule]

def parse_lexical_spec(lines):
    lexical_spec = LexicalSpec([])
    if lines == []:
        return lexical_spec
    if lines is None:
        return lexical_spec

    skipToken = re.compile(r'^skip\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*$')
    tokenToken = re.compile(r'^token\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*$')
    otherToken = re.compile(r'^(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*$')
    for line in lines:
        l = line.string.strip()
        l = l.split("#")[0]

        #Skips Comment only lines completely
        if l == '':
            continue

        skipTokenMatch = re.match(skipToken, l)
        if skipTokenMatch:
            patternRule = skipTokenMatch['Pattern']
            patternRule = patternRule.strip('\'')
            patternRule = patternRule.strip('\"')
            newSkipRule = LexicalRule(line=line, isSkip=True, name=skipTokenMatch['Name'], pattern=patternRule)
            lexical_spec.ruleList.append(newSkipRule)
            continue

        tokenTokenMatch = re.match(tokenToken, l)
        if tokenTokenMatch:
            patternRule = tokenTokenMatch['Pattern']
            patternRule = patternRule.strip('\'')
            patternRule = patternRule.strip('\"')
            newTokenRule = LexicalRule(line=line, isSkip=False, name=tokenTokenMatch['Name'], pattern=patternRule)
            lexical_spec.ruleList.append(newTokenRule)
            continue

        otherTokenMatch = re.match(otherToken, l)
        if otherTokenMatch:
            patternRule = otherTokenMatch['Pattern']
            patternRule = patternRule.strip('\'')
            patternRule = patternRule.strip('\"')
            newTokenRule = LexicalRule(line=line, isSkip=False, name=otherTokenMatch['Name'], pattern=patternRule)
            lexical_spec.ruleList.append(newTokenRule)
            continue

        raise AttributeError("Line is not in correct format!!!")

    return lexical_spec
