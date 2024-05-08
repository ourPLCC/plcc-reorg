from .section import parseSections
from .lexical import parseLexicalSpec
from .syntactic import parseSyntacticSpec
from .semantic import parseSemanticSpec


def parseSpec(specLines):
    sections = parseSections(lines)
    lexicalSpec = None
    syntacticSpec = None
    semanticSpecs = []
    if sections:
        section = sections.pop(0)
        lexicalSpec = parseLexicalSpec(section)
    if sections:
        section = sections.pop(0)
        syntacticSpec = parseSyntacticSpec(section)
    while sections:
        section = sections.pop(0)
        s = parseSemantics(section)
        semanticSpecs.append(s)
    return Spec(
        lexicalSpec,
        syntacticSpec,
        semanticSpecs
    )