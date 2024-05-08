# -*-python-*-

"""
    PLCC: A Programming Languages Compiler-Compiler
    Copyright (C) 2023  Timothy Fossum <plcc@pithon.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import re
import os
import pathlib
import io
import shutil
import tempfile

import plcc.version
from plcc.cl import CommandLineProcessor
from plcc.parse.reader import SpecificationReader

from plcc.stubs.java import JavaStubs
from plcc.stubs.python import PythonStubs
from plcc.stubs.stubs import StubDoesNotExistForHookException

from plcc.specification_file import SpecificationParser


# current file information
Fname = ''          # current file name (STDIN if standard input)
Lno = 0             # current line number in file
Line = ''           # current line in the file
nlgen = None        # next line generator for Fname
STD = []            # reserved names from Std library classes
STDT = []           # token-related files in the Std library directory
STDP = []           # parse/runtime-related files in the Std library directory

flags = {}          # processing flags (dictionary)

lineMode = False    # True if in line mode

startSymbol = ''    # start symbol (first nonterm in rules)
term = set()        # set of term (token) names
termSpecs = []      # term (token) specifications for generating the Token file

nonterms = set()    # set of all nonterms
fields = {}         # maps a non-abstract class name to its list of fields
rules = []          # list of items  of the form (nt, cls, rhs),
                    # one for each grammar rule
extends = {}        # maps a derived class to its abstract base class
derives = {}        # maps an abstract class to a list of its derived classes
cases = {}          # maps a non-abstract class to its set of case terminals
                    # for use in a switch
rrule = {}          # maps a repeating rule class name to its separator string
                    # (or None)

def debug(msg, level=1):
    # print(getFlag('debug'))
    if msg and getFlag('debug') >= level:
        print('%%% {}'.format(msg), file=sys.stderr)
        return True
    return False

def debug2(msg):
    debug(msg, level=2)

def LIBPLCC():
    return str(pathlib.Path(__file__).parent)


class Main():
    def __init__(self):
        self._STDT = ['ILazy','IMatch','IScan','ITrace', 'Trace', 'PLCCException', 'Scan']
        self._STDP = ['ProcessFiles','Parse','Rep','ParseJsonAst']
        self._STD = self._STDT + self._STDP
        self._STD.append('Token')
        self._flags = self._getDefaultFlags()
        self._specificationFilePath = None

    def _getDefaultFlags(self):
        # file-related flags -- can be overwritten
        # by a grammar file '!flag=...' spec
        # or by a '--flag=...' command line argument
        flags = {}
        for fname in self._STD:
            flags[fname] = fname
        flags['libplcc'] = LIBPLCC()
        flags['Token'] = True         # generate scanner-related files
        # behavior-related flags
        flags['debug'] = 0                  # default debug value
        flags['destdir'] = 'Java'           # the default destination directory
        flags['python_destdir'] = 'Python'  # default destination for fourth section semantics (Python)
        flags['pattern'] = True             # create a scanner that uses re. patterns
        flags['LL1'] = True                 # check for LL(1)
        flags['parser'] = True              # create a parser
        flags['semantics'] = True           # create java semantics routines
        flags['python_semantics'] = True    # create python semantics routines
        flags['nowrite'] = False            # when True, produce *no* file output
        flags['version'] = False            # when True, print the version and exit.
        return flags

    def main(self, argv):
        try:
            self._processCommandLine(argv)
            if self._flags['version']:
                self._printVersion()
            else:
                self._loadSpecification()
                self._generateLanguageSystem()
        except ParseException as e:
            self._handleParseException(e)
        except Exception as e:
            self._handleException(e)

    def _processCommandLine(self, argv):
        cl = CommandLineProcessor()
        cl.process(argv)
        fs = cl.getFlags()
        self._flags.update(fs)
        self._specificationFilePath = cl.getSpecificationFilePath()

    def _printVersion(self):
        print(plcc.version.get_version())

    def _loadSpecification(self):
        plcc.spec.load.Loader().load(self._specificationFilePath)

    def _generateLanguageSystem(self):
        builder = Builder()
        builder.build(self._specification)

        if self._flags['nowrite']:
            return
        if not self._flags['Token']:
            return # do not create any automatically generated scanner-related files

        generator.generate(builder)


    def _orphans_from_old_main():
        java = JavaStubs()
        python = PythonStubs()
        par(nxt, java, python)    # LL(1) check and parser generation
        sem(nxt, java, destFlag='destdir', semFlag='semantics', fileExt='.java')
        sem(nxt, python, destFlag='python_destdir', semFlag='python_semantics', fileExt='.py')
        done()

    def _handleParseException(self, exception):
        m = f'{self._line.line:4} [{self._line.file}]: {self._message}\nline: {self._line.text}'
        print(m, file=sys.stderr)
        sys.exit(1)

    def _handleException(self, exception):
        print(str(exception), file=sys.stderr)
        sys.exit(1)



def parFinishUp(java, python):
    global STDP, startSymbol, nonterms, extends, derives, rules
    if not rules:
        print('No grammar rules')
        return
    debug('[parFinishUp] par: finishing up...')
    # check to make sure all RHS nonterms appear as the LHS of at least one rule
    for nt in nonterms:
        debug('[parFinishUp] nt={}'.format(nt))
    for (nt, cls, rhs) in rules:
        rhsString = ''
        for item in rhs:
            debug('[parFinishUp] item={}'.format(item))
            if isNonterm(item):
                rhsString += ' <{}>'.format(item)
                if not item in nonterms:
                    death('nonterm {} appears on the RHS of rule "<{}> ::= {} ..." but not on any LHS'.format(item, nt, rhsString))
            else:
                rhsString += ' {}'.format(item)
        debug('[parFinishUp] rule: "<{}> ::= {}"'.format(nt, rhsString))
    # if debugging, print all of the extends and derives items
    for cls in extends:
        debug('[parFinishUp] class {} extends {}'.format(cls, extends[cls]))
    for base in derives:
        debug('[parFinishUp] base class {} derives {}'.format(base, derives[base]))
    # print the nonterminals
    print('Nonterminals (* indicates start symbol):')
    for nt in sorted(nonterms):
        if nt[-1] == '#':
            continue  # ignore automatically generated repeating rule names
        if nt == startSymbol:
            ss = ' *<{}>'.format(nt)
        else:
            ss = '  <{}>'.format(nt)
        print(ss)
    print()

    # print abstract classes
    print('Abstract classes:')
    for cls in sorted(derives):
        print('  {}'.format(cls))

    # check for LL1
    if getFlag('LL1'):
        checkLL1()

    if getFlag('nowrite'):
        return
    # copy the Std parser-related files
    dst = getFlag('destdir')
    libplcc = getFlag('libplcc')
    std = pathlib.Path(libplcc) / 'lib' / 'Std'
    for fname in STDP:
        if getFlag(fname):
            debug('[parFinishUp] copying {} from {} to {} ...'.format(fname, std, dst))
            try:
                shutil.copy('{}/{}.java'.format(std, fname), '{}/{}.java'.format(dst, fname))
            except:
                death('Failure copying {} from {} to {}'.format(fname, std, dst))

    buildStubsAndStart(java, python, fields, derives, cases, startSymbol)


def buildStubsAndStart(java, python, fields, derives, cases, startSymbol):
    buildStubs(java, fields, derives, cases, startSymbol)
    buildStubs(python, fields, derives, cases, startSymbol)
    buildStart()



def checkLL1():
    global rules, nonterms, cases
    first = {}
    follow = {}
    switch = {}

    def getFirst(form):
        nonlocal first
        # return the first set (of terminals) of this sentential form
        fst = set()
        if len(form) == 0:         # the form is empty, so it only derives Null
            return {'Null'}
        tnt = form[0]              # get the item at the start of the sentential form
        if isTerm(tnt):
            return {tnt}           # the form starts with a terminal, which is clearly its only first set item
        # tnt must be a nonterm -- get the first set for this and add it to our current set
        f = first[tnt]             # get the current first set for tnt (=form[0])
        for t in f:
            # add all non-null stuff from first[tnt] to the current first set
            if t != 'Null':
                fst.update({t})
            else:
                # Null is in the first set for f, so recursively add the nonterms from getFirst(form[1:])
                fst.update(getFirst(form[1:]))
        # debug('first set for {}: {}'.format(form, fst))
        return fst

    for nt in nonterms:
        first[nt] = set()        # initialize all of the first sets
        follow[nt] = set()       # initialize all of the follow sets
        switch[nt] = []          # maps each nonterm to a list of its first sets

    # determine the first sets
    modified = True
    while modified:
        modified = False  # assume innocent
        for (nt, cls, rhs) in rules:
            fst = first[nt]      # the current first set for this nonterminal
            fct = len(fst)       # see if the first set changes
            fst.update(getFirst(rhs))   # add any new terminals to the set
            if len(fst) != fct:
                modified = True
    if debug('[checkLL1] First sets:'):
        for nt in nonterms:
            debug('[checkLL1] {} -> {}'.format(nt, first[nt]))

    # determine the follow sets
    modified = True
    while modified:
        modified = False
        for (nt, cls, rhs) in rules:
            rhs = rhs[:]         # make a copy
            debug('[checkLL1] examining rule {} ::= {}'.format(nt, ' '.join(rhs)))
            while rhs:
                tnt = rhs.pop(0) # remove the first element of the list
                if isNonterm(tnt):
                    # only nonterminals count for determining follow sets
                    fol = follow[tnt]              # the current follow set for tnt
                    fct = len(fol)
                    for t in getFirst(rhs):        # look at the first set of what follows tnt (the current rhs)
                        if t == 'Null':
                            fol.update(follow[nt]) # if the rhs derives the empty string, what follows nt must follow tnt
                        else:
                            fol.update({t})        # otherwise, what the rhs derives must follow tnt
                    if len(fol) != fct:
                        modified = True
    if debug('[checkLL1] Follow sets:'):
        for nt in nonterms:
            debug('[checkLL1]   {}: {}'.format(nt, ' '.join(follow[nt])))

    # determine the switch sets for each nonterm and corresponding rhs
    for (nt, cls, rhs) in rules:
        # print('### nt={} cls={} rhs= {}'.format(nt, cls, ' '.join(rhs)))
        fst = getFirst(rhs)
        if 'Null' in fst:
            # the rhs can derive the empty string, so remove Null from the set
            fst -= {'Null'}
            # add all of the terminals in follow[nt] to this switch set
            fst.update(follow[nt])
        switch[nt].append((fst, rhs))
        if cls != None:
            saveCases(cls, fst)
    if debug('[checkLL1] nonterm switch sets:'):
        for nt in switch:
            debug('[checkLL1] {} => {}'.format(nt, switch[nt]))

    # finally check for LL(1)
    for nt in switch:
        allTerms = set()
        for (fst, rhs) in switch[nt]:
            debug('[checkLL1] nt={} fst={} rhs={}'.format(nt, fst, rhs))
            s = allTerms & fst   # check to see if fst has any tokens already in allTerms
            if s:
                death('''\
not LL(1):
term(s) {} appears in first sets for more than one rule starting with nonterm {}
'''.format(' '.join(fst), nt))
            else:
                allTerms.update(fst)
        if not allTerms:
            death('possibly useless or left-recursive grammar rule for nonterm {}'.format(nt))
        cases[nt] = allTerms
    pass

def saveCases(cls, fst):
    global cases, derives
    if cls in cases:
        death('cases for class {} already accounted for'.format(cls))
    if cls in derives:
        death('{} is an abstract class'.format(cls))
    # print('### class={} cases={}'.format(cls, ' '.join(fst)))
    cases[cls] = fst

class DuplicateAbstractStubException(Exception):
    pass

class UnreachableClassException(Exception):
    pass

class DuplicateStubException(Exception):
    pass

def buildStubs(stubs, fields, derives, cases, startSymbol):
    for cls in derives:
        # make parser stubs for all abstract classes
        if cls in stubs.getStubs():
            raise DuplicateAbstractStubException(f'{cls}')
        for c in derives[cls]:
            if len(cases[c]) == 0:
                raise UnreachableClassException(f'{c}')
        stubs.addAbstractStub(cls, derives, cases, startSymbol, caseIndentLevel=2, ext=' extends _Start')

    for cls in fields:
        # make parser stubs for all non-abstract classes
        if cls in stubs.getStubs():
            raise DuplicateStubException(f'{cls}')
        makeStub(stubs, cls)


def makeStub(stubs, cls):
    global fields, extends, rrule
    # make a stub for the given non-abstract class
    debug('[makeStub] making stub for non-abstract class {}'.format(cls))
    sep = False
    (lhs, rhs) = fields[cls]
    extClass = '' # assume not an extended class
    # two cases: either cls is a repeating rule, or it isn't
    if cls in rrule:
        ruleType = '**='
        sep = rrule[cls]
        arbno = parseArbno(cls, rhs, cases)
        (fieldVars, parseString) = makeArbnoParse(cls, arbno, sep)
        if sep != None:
            rhs = rhs + ['+{}'.format(sep)]
    else:
        ruleType = '::='
        (fieldVars, parseString) = makeParse(cls, rhs)
        # two sub-cases: either cls is an extended class (with abstract base class) or it's a base class
        if cls in extends:
            extClass = extends[cls]
    ruleString = '{} {} {}'.format(lhs, ruleType, ' '.join(rhs))
    stubs.addStub(cls, fieldVars, startSymbol, lhs, extClass, ruleString, parseString)

def indent(n, iList):
    ### make a new list with the old list items prepended with 4*n spaces
    indentString = '    '*n
    newList = []
    for item in iList:
        newList.append('{}{}'.format(indentString, item))
    # print('### str={}'.format(str))
    return newList

def makeParse(cls, rhs):
    args = []
    parseList = []
    fieldVars = []
    fieldSet = set()
    rhsString = ' '.join(rhs)
    for item in rhs:
        (tnt, field) = defangRHS(item)
        if tnt == None:
            # item must be a bare token -- just match it
            parseList.append('scn$.match(Token.Match.{}, trace$);'.format(item))
            continue
        if field in fieldSet:
            deathLNO('duplicate field name {} in rule RHS {}'.format(field, rhsString))
        fieldSet.update({field})
        args.append(field)
        if isTerm(tnt):
            fieldType = 'Token'
            parseList.append(
                'Token {} = scn$.match(Token.Match.{}, trace$);'.format(field, tnt))
        else:
            fieldType = nt2cls(tnt)
            parseList.append(
                '{} {} = {}.parse(scn$, trace$);'.format(fieldType, field, fieldType))
        fieldVars.append((field, fieldType))
    parseList.append('return new {}({});'.format(cls, ', '.join(args)))
    debug('[makeParse] parseList={}'.format(parseList))
    parseString = '\n'.join(indent(2, parseList))
    return (fieldVars, parseString)


def parseArbno(cls, rhs, cases):
    rhsString = ' '.join(rhs)
    fieldSet = set() # the set of field variable names for this RHS
    itemTntFields = []
    for item in rhs:
        (tnt, field) = defangRHS(item)
        if tnt is not None:
            field += 'List'
            if field in fieldSet:
                deathLNO(
                    'duplicate field name {} in RHS rule {}'.format(field, rhsString))
            fieldSet.update({field})
        itemTntFields.append( (item, tnt, field) )
    if len(cases[cls]) == 0:
        deathLNO('class {} is unreachable'.format(cls))
    return itemTntFields


def makeArbnoParse(cls, arbno, sep):
    # print('%%%%%% cls={} rhs="{}" sep={}'.format(cls, ' '.join(rhs), sep))
    global cases
    inits = []       # initializes the List fields
    args = []        # the arguments to pass to the constructor
    loopList = []    # the match/parse code in the Arbno loop
    fieldVars = []   # the field variable names (all Lists), to be returned
    # rhs = rhs[:-1]   # remove the last item from the grammar rule (which has an underscore item)
    # create the parse statements to be included in the loop
    switchCases = [] # the token cases in the switch statement

    for item, tnt, field in arbno:
        if tnt == None:
            loopList.append('scn$.match(Token.Match.{}, trace$);'.format(item))
            continue
        # field is either derived from tnt or is an annotated field name
        if isTerm(tnt):
            # a token
            baseType = 'Token'
            loopList.append(
                '{}.add(scn$.match(Token.Match.{}, trace$));'.format(field, tnt))
        elif isNonterm(tnt):
            baseType = nt2cls(tnt)
            loopList.append('{}.add({}.parse(scn$, trace$));'.format(field, baseType))
        else:
            pass # cannot get here
        args.append(field)
        fieldType = 'List<{}>'.format(baseType)
        fieldVars.append((field, fieldType))
        inits.append('{} {} = new ArrayList<{}>();'.format(fieldType, field, baseType))
    switchCases = []
    for item in cases[cls]:
        switchCases.append('case {}:'.format(item))
    returnItem = 'return new {}({});'.format(cls, ', '.join(args))
    if sep == None:
        # no separator
        parseString = """\
{inits}
        while (true) {{
            Token t$ = scn$.cur();
            Token.Match match$ = t$.match;
            switch(match$) {{
{switchCases}
{loopList}
                continue;
            default:
                {returnItem}
            }}
        }}
""".format(inits='\n'.join(indent(2, inits)),
           switchCases='\n'.join(indent(3, switchCases)),
           loopList='\n'.join(indent(4, loopList)),
           returnItem=returnItem)
    else:
        # there's a separator
        parseString = """\
{inits}
        // first trip through the parse
        Token t$ = scn$.cur();
        Token.Match match$ = t$.match;
        switch(match$) {{
{switchCases}
            while(true) {{
{loopList}
                t$ = scn$.cur();
                match$ = t$.match;
                if (match$ != Token.Match.{sep})
                    break; // not a separator, so we're done
                scn$.match(match$, trace$);
            }}
        }} // end of switch
        {returnItem}
""".format(inits='\n'.join(indent(2, inits)),
           switchCases='\n'.join(indent(2, switchCases)),
           loopList='\n'.join(indent(4, loopList)),
           returnItem=returnItem,
           sep=sep)
    debug('[makeArbnoParse] fieldVars={}'.format(fieldVars))
    return (fieldVars, parseString)

def buildStart():
    global startSymbol
    # build the _Start.java file
    if startSymbol == '':
        death('no start symbol!')
    dst = getFlag('destdir')
    if dst == None or getFlag('nowrite'):
        return
    file = '_Start.java'
    try:
        startFile = open('{}/{}'.format(dst, file), 'w')
    except:
        death('failure opening {} for writing'.format(file))
    startString = """\
public abstract class _Start {{

    public static _Start parse(Scan scn, Trace trace) {{
        return {start}.parse(scn, trace);
    }}

    public void $run() {{
        System.out.println(this.toString());
    }}

    public void $ok() {{
        System.out.println("OK");
    }}

}}
""".format(start=nt2cls(startSymbol))
    print(startString, file=startFile)
    startFile.close()

def semFinishUp(stubs, destFlag='destdir', ext='.java'):
    if getFlag('nowrite'):
        return
    global STD
    dst = getFlag(destFlag)
    if not dst:
        death('illegal destdir flag value')
    try:
        os.mkdir(str(dst))
        debug('[semFinishUp] ' + dst + ': destination subdirectory created')
    except FileExistsError:
        debug('[semFinishUp] ' + dst + ': destination subdirectory exists')
    except:
        death(dst + ': error creating destination subdirectory')
    print('\n{} source files created:'.format(dst))
    # print *all* of the generated files
    for cls in sorted(stubs):
        if cls in STD:
            death('{}: reserved class name'.format(cls))
        try:
            fname = '{}/{}{}'.format(dst, cls, ext)
            with open(fname, 'w') as f:
                print(stubs[cls], end='', file=f)
        except:
            death('cannot write to file {}'.format(fname))
        print('  {}{}'.format(cls, ext))

def sem(nxt, stubs, semFlag, destFlag, fileExt):
    global argv
    # print('=== semantic routines')
    if not getFlag(semFlag):
        stubs = stubs.getStubs()
        semFinishUp(stubs, destFlag, fileExt)
        done()
    for line in nxt:
        line = line.strip()
        if line == "%":
            break
        if len(line) == 0 or line[0] == '#':
            # skip comments or blank lines
            continue
        (cls, _, mod) = line.partition(':')
        # print('>>> cls={} mod={}'.format(cls, mod))
        cls = cls.strip()
        codeString = getCode(nxt) # grab the stuff between %%% ... %%%
        if line[-8:] == ':ignore!':
            continue
        # check to see if line has the form Class:mod
        mod = mod.strip() # mod might be 'import', 'top', etc.
        try:
            stubs.addCodeToClass(cls, mod, codeString)
        except StubDoesNotExistForHookException as e:
            deathLNO(str(e))


    stubs = stubs.getStubs()
    semFinishUp(stubs, destFlag, fileExt)


def getCode(nxt):
    code = []
    offset = None
    for line in nxt:
        line = line.rstrip()
        if re.match(r'\s*#', line) or re.match(r'\s*$', line):
            # skip comments or blank lines
            continue
        if re.match(r'%%{', line): # legacy plcc
            stopMatch = r'%%}'
            break
        if re.match(r'%%%', line):
            stopMatch = r'%%%'
            break
        else:
            deathLNO('expecting a code segment')
    lineMode = True # switch on line mode
    for line in nxt:
        if re.match(stopMatch, line):
            break
        if offset == None:
            offset = getOffset(line)
        line = removeOffset(line, offset)
        code.append(line)
    else:
        deathLNO('premature end of file')
    lineMode = False # switch off line mode
    if len(code)>0 :
        while len(code[0]) == 0:
            code.pop(0)
        while len(code[-1]) == 0:
            code.pop()
    return code


#####################
# utility functions #
#####################

def getFlag(s):
    global flags
    if s in flags:
        return flags[s]
    else:
        return None


def push(struct, item):
    struct.append(item)


def removeOffset(ln, offset):
    check = ln.strip()
    if len(check) == 0:
        return ln
    s = re.sub(offset,"",ln,count=1)
    return s

def getOffset(line):
    check = line.lstrip()
    if len(check) == 0 or check[0] == '#':
        return None
    s = re.search(r"\S", line).start()
    return line[0:s]

if __name__ == '__main__':
    main()
