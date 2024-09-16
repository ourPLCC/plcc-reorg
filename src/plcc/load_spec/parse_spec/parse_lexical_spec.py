from dataclasses import dataclass
import re

from ..load_rough_spec.parse_lines import Line


###lexical_spec = parse_lexical_spec(list_of_lines)

@dataclass
class LexicalRule:
    line: Line              #This means the whole line object?? OR just the string?
    isSkip: bool
    name: str
    pattern: str      #Remember to remove quotes

@dataclass      #Does it need to be frozen??
class LexicalSpec:
    ruleList: [LexicalRule]

def parse_lexical_spec(lines):
    lexical_spec = LexicalSpec([])
    if lines == []:
        return lexical_spec
    if lines is None:
        return lexical_spec
                                                                            #Should I look out for more possible errors, like a line that starts with random symbols?? Ex: '^wivn #this is now a comment'
                                                                            #^ If I can force only words/digits this would be super easy
    skipToken = re.compile(r'^skip\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*$')
    tokenToken = re.compile(r'^token\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*$')
    for line in lines:
        l = line.string.strip()
        n = len(l)

        #Take out any comments
        for i in range(0, n-1):
            if l[i] == '#':
                l = l[0:n]

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


    return lexical_spec
