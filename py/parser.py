import sys
from typing import List, Tuple
from enum import Enum
from pprint import pprint
from typing import List
from time import sleep

DIGITS = [chr(c) for c in list(range(ord('0'), ord('9')+1))]
UPPERS = [chr(c) for c in list(range(ord('A'), ord('Z')+1))]
LOWERS = [chr(c) for c in list(range(ord('a'), ord('z')+1))]
ALPHAS = UPPERS + LOWERS
WHITESPACE = [' ', '\t']

indent:int = 0
debug:bool

class TextStream:
    
    name: str
    
    text: str
    lines: list[str]
    index: int

    line: int
    col: int

    gotMatch: str
    rewindIdx: int|None
    
    def __init__(self, filename:str) -> None:

        with open(filename, 'r') as f:
            self.name = filename
            self.text = f.read()
            self.lines = self.text.splitlines()
            self.index = 0
            self.line, self.col = 1, 0 
            self.gotMatch = None
            self.rewindIdx = None

    def pos(self) -> Tuple[int, int]:
        return self.line, self.col

    def at_end(self) -> bool:
        return self.index >= len(self.text)

    def consume(self) -> str|None:
        if self.at_end():
            return None
        
        c = self.text[self.index]
        self.index += 1

        # Update pos
        self.col += 1
        if c == '\n':
            self.line += 1
            self.col = 0

        return c
    
    def look(self, shift) -> str|None:
        try:
            return self.text[self.index + shift]
        except IndexError:
            return None
    
    def look_slice(self, shift) -> str|None:
        try:
            return self.text[self.index : self.index + shift]
        except IndexError:
            return None

    def curr(self) -> str|None:
        return self.look(0)

    def next(self) -> str|None:
        return self.look(1)

    def find(self, cmatch:List[str]|str) -> bool:
        saved = self.index
        while self.curr() not in [None, '\n']:
            if self.is_match(cmatch):
                self.index = saved
                return True
            self.index += 1

        self.index = saved
        return False

    def is_match(self, cmatch:List[str]|str) -> bool|None:
        
        c = self.curr()
        if c is None:
            self.gotMatch = None
            return None
        
        out = False
        if isinstance(cmatch, list):
            for cm in cmatch:
                try:
                    if self.look_slice(len(cm)) == cm:
                        out = True
                        self.gotMatch = cm
                except IndexError:
                    pass

        elif isinstance(cmatch, str):
            try:
                if self.look_slice(len(cmatch)) == cmatch:
                    self.gotMatch = cmatch
                    out = True
            except IndexError:
                pass
        
        if not out:
            self.gotMatch = None
        return out
    
    def match(self, cmatch:List[str]|str, skipSpace:bool=True) -> str|None:

        if not self.is_match(cmatch):
            self.expected(cmatch)

        if isinstance(cmatch, list) and len(cmatch) > 10:
            cmatch = f'[{cmatch[0]}, {cmatch[1]} ... {cmatch[-2]}, {cmatch[-1]}]'

        global indent
        global debug
        shift = '  ' * indent
        if debug:
            print(f'{shift}matched `{repr(self.gotMatch)}` to `{repr(cmatch)}`')
        
        for _ in self.gotMatch:
            out = self.consume()
        
        return out

    def goto(self, cmatch:List[str]|str) -> str|None:
        c = self.curr()

        while c != None:
            if isinstance(cmatch, list):
                if c in cmatch:
                    break
            elif isinstance(cmatch, str):
                if c == cmatch:
                    break
            else:
                return None
            
            c = self.consume()
        
        return c

    def skip(self, cmatch:List[str]|str) -> None:
        while self.is_match(cmatch):
            self.match(cmatch, False)
    
    def skip_space(self, newline:bool=False) -> int:
        count = 0
        skips = [' ', '\t']
        if newline:
            skips.append('\n')
        
        while self.is_match(skips):
            self.match(skips, False)
            count += 1
        return count

    def skip_comment(self):
        if self.is_match('#'):
            self.match('#')
            c = None
            while not self.at_end():
                c = self.curr()
                if c is not None:
                    self.match(c)
                    if c == '\n':
                        break
                else:
                    break               

    def expected(self, cmatch:List[str]|str, got:str|None=None) -> SyntaxError:
        if got is None:
            got = self.curr()

        if isinstance(cmatch, list) and len(cmatch) > 10:
            cmatch = f'[{cmatch[0]}, {cmatch[1]}, ..., {cmatch[-1]}]'

        lineNum = f'[{self.line}] '
        linePrint = lineNum + self.lines[self.line - 1]
        indicator = ('~' * len(lineNum)) + ('~' * (self.col)) + '^'
        
        raise SyntaxError(f'\n{self.name} [{self.line}:{self.col}]\tExpected token: `{cmatch}`\t(got {repr(got)})\n\n{linePrint}\n{indicator}')


class TokAttr(Enum):
    PIPE = 0
    STAR = 1
    TERM = 2
    ASSIGN = 3
    TERM_ASSIGN = 4
    COMP = 5
    TOP_LEVEL = 6
    LITERAL = 7
    TYPE = 8


class TokType(Enum):
    PROGRAM =       ['PROGRAM',     None]
    EOF =           ['EOF',         None]
    LINEBREAK =     ['LINEBREAK',   '\n']
    STMT_BREAK =    ['STMT_BREAK',  ';']
    COMMENT =       ['COMMENT',     '#']

    FUNC =          ['FUNC',        'func',     TokAttr.TOP_LEVEL]    
    STRUCT =        ['STRUCT',      'struct',   TokAttr.TOP_LEVEL]
    ENUM =          ['ENUM',        'enum',     TokAttr.TOP_LEVEL]
    CONST =         ['CONST',       'const',    TokAttr.TOP_LEVEL]
    IMPORT =        ['IMPORT',      'import',   TokAttr.TOP_LEVEL]

    BLOCK =         ['BLOCK',       '{']

    RETURN =        ['RETURN',      'return'] 
    CONTINUE =      ['CONTINUE',    'continue']
    BREAK =         ['BREAK',       'break']

    SUBST =         ['SUBST',       '=>']
    VAR =           ['VAR',         'var',      TokAttr.TOP_LEVEL]

    ASSIGN =        ['ASSIGN',      '=',        TokAttr.ASSIGN]
    ASSIGN_ADD =    ['ASSIGN_ADD',  '+=',       TokAttr.ASSIGN]
    ASSIGN_SUB =    ['ASSIGN_SUB',  '-=',       TokAttr.ASSIGN]
    ASSIGN_MULT =   ['ASSIGN_MULT', '*=',       [TokAttr.ASSIGN, TokAttr.TERM_ASSIGN]]
    ASSIGN_DIV =    ['ASSIGN_DIV',  '/=',       [TokAttr.ASSIGN, TokAttr.TERM_ASSIGN]]
    ASSIGN_MOD =    ['ASSIGN_MOD',  '%=',       [TokAttr.ASSIGN, TokAttr.TERM_ASSIGN]]

    STMT_SEQ =      ['STMT_SEQ',        None]
    WHILE_STMT =    ['WHILE_STMT',      'while']
    FOR_STMT =      ['FOR_STMT',        'for']
    IF_STMT =       ['IF_STMT',         'if']
    ELSE_IF_STMT =  ['ELSE_IF_STMT',    'else if']
    ELSE_STMT =     ['ELSE_STMT',       'else']

    PIPE_DIST =     ['PIPE_DIST',       '|<',   TokAttr.PIPE]
    PIPE_FUNNEL =   ['PIPE_FUNNEL',     '|>',   TokAttr.PIPE]
    PIPE_PAIR =     ['PIPE_PAIR',       '|:',   TokAttr.PIPE]
    PIPE_MAP =      ['PIPE_MAP',        '|@',   TokAttr.PIPE]
    PIPE_FILTER =   ['PIPE_FILTER',     '|?',   TokAttr.PIPE]
    PIPE_REDUCE =   ['PIPE_REDUCE',     '|-',   TokAttr.PIPE]
    PIPE_MEMBER =   ['PIPE_MEMBER',     '|.',   TokAttr.PIPE]
    PIPE_ZIP =      ['PIPE_ZIP',        '|~',   TokAttr.PIPE]
    PIPE_FLATTEN =  ['PIPE_FLATTEN',    '|_',   TokAttr.PIPE]
    PIPE_ANY =      ['PIPE_ANY',        '|*',   TokAttr.PIPE]
    PIPE_EACH =     ['PIPE_EACH',       '|%',   TokAttr.PIPE]
    PIPE_SUM =      ['PIPE_SUM',        '|+',   TokAttr.PIPE]
    PIPE =          ['PIPE',            '|']

    EXPR_SEQ =      ['EXPR_SEQ',    None]
    LAMBDA_EXPR =   ['LAMBDA_EXPR', ':>']

    LOG_TERN =      ['LOG_TERN',    '?']
    LOG_OR =        ['LOG_OR',      'or']
    LOG_AND =       ['LOG_AND',     'and']
    LOG_NOT =       ['LOG_NOT',     'not']

    COMP_EQ =       ['COMP_EQ',     '==',       TokAttr.COMP]
    COMP_NEQ =      ['COMP_NEQ',    '!=',       TokAttr.COMP]
    COMP_LT =       ['COMP_LT',     '<',        TokAttr.COMP]
    COMP_GT =       ['COMP_GT',     '>',        TokAttr.COMP]
    COMP_LTE =      ['COMP_LTE',    '<=',       TokAttr.COMP]
    COMP_GTE =      ['COMP_GTE',    '>=',       TokAttr.COMP]

    BIT_NOT =       ['BIT_NOT',     '*~',       TokAttr.STAR]
    BIT_OR =        ['BIT_OR',      '*|',       TokAttr.STAR]
    BIT_XOR =       ['BIT_XOR',     '*^',       TokAttr.STAR]
    BIT_AND =       ['BIT_AND',     '*&',       TokAttr.STAR]
    BIT_SHR =       ['BIT_SHR',     '>>']
    BIT_SHL =       ['BIT_SHL',     '<<']

    RANGE =         ['RANGE',       '..']

    SUM =           ['SUM',         None]
    ADD =           ['ADD',         '+']
    SUB =           ['SUB',         '-']

    TERM =          ['TERM',        None]
    MULT =          ['MULT',        '*',        TokAttr.TERM]
    DIV =           ['DIV',         '/',        TokAttr.TERM]
    MOD =           ['MOD',         '%',        TokAttr.TERM]
    
    FACTOR =        ['FACTOR',      None]
    POSATE =        ['POSATE',      '+']
    NEGATE =        ['NEGATE',      '-']
    
    POWER =         ['POWER',       '**']
    
    CREMENT =       ['CREMENT',     None]
    INCREMENT =     ['INCREMENT',   '++']
    DECREMENT =     ['DECREMENT',   '--']

    PRIMARY =       ['PRIMARY',         None]
    STREAM =        ['STREAM',          '$']
    STREAMINDEX =   ['STREAMINDEX',     None]
    STRUCTMEMBER =  ['STRUCTMEMBER',    '.']
    SELFMEMBER =    ['SELFMEMBER',      '@']
    MEMBER =        ['MEMBER',          '.']
    DICT_KEY =      ['DICT_KEY',        '::']
    INDEX =         ['INDEX',           '[']
    CALL =          ['CALL',            '(']

    ARGS =          ['ARGS',        None]
    ATOM =          ['ATOM',        None]
    LIST_RAW =      ['LIST_RAW',    None]
    PARAM_SEQ =     ['PARAM_SEQ',   None]
    PARAM =         ['PARAM',       None]
    ID =            ['ID',          None]

    TYPE_LIST =     ['TYPE_LIST',   'List',     TokAttr.TYPE]
    TYPE_DICT =     ['TYPE_DICT',   'Dict',     TokAttr.TYPE]

    TYPE_INT =      ['TYPE_INT',    'int',      TokAttr.TYPE]
    TYPE_FLOAT =    ['TYPE_FLOAT',  'float',    TokAttr.TYPE]
    TYPE_STRING =   ['TYPE_STRING', 'String',   TokAttr.TYPE]
    TYPE_BOOL =     ['TYPE_BOOL',   'bool',     TokAttr.TYPE]
    TYPE_NULL =     ['TYPE_NULL',   'null',     TokAttr.TYPE]
    TYPE_ANY =      ['TYPE_ANY',    'any',      TokAttr.TYPE]
    TYPE_DEF =      ['TYPE_DEF',    None,       TokAttr.TYPE]

    LIT_INT =       ['LIT_INT',     None,       TokAttr.LITERAL]  
    LIT_FLOAT =     ['LIT_FLOAT',   None,       TokAttr.LITERAL]
    LIT_STRING =    ['LIT_STRING',  None,       TokAttr.LITERAL]
    LIT_TRUE =      ['LIT_TRUE',    'True',     TokAttr.LITERAL]
    LIT_FALSE =     ['LIT_FALSE',   'False',    TokAttr.LITERAL]
    ESC_CHAR =      ['ESC_CHAR',    None,       TokAttr.LITERAL]
    STR_BASE =      ['STR_BASE',    None,       TokAttr.LITERAL]

    def get_dict() -> dict:
        return {t.value[1] : t for t in TokType}
    
    def lookup(t) -> str:
        assert isinstance(t, TokType)
        return t.value[1]

    def raw(t) -> str:
        assert isinstance(t, TokType)
        return t.value[2]

    def with_attr(a:TokAttr) -> list:
        # return [t.value[1] for t in TokType if len(t.value) > 2 and t.value[2] == a]
        out = []
        for t in TokType:
            if len(t.value) > 2:
                if (isinstance(t.value[2], list) and a in t.value[2]) or a == t.value[2]:
                    out.append(t.value[1])                    
        return out

    def has_attr(self, a:TokAttr) -> bool:
        if len(self.value) < 3:
            return False
        if isinstance(self.value[2], list):
            return a in self.value[2]
        return a == self.value[2]


class Tok:
    t:TokType

    line:int    
    col:int

    def __init__(self, t:TokType, line:int, col:int) -> None:
        self.t, self.line, self.col = t, line, col

    def __str__(self) -> str:
        return f'{self.t:20}\t({self.line}:{self.col})'

    def printer(self, indent:int=0) -> None:
        shift = ' ' * indent
        print(f'{shift}{str(self)}')


class Tree:
    tok: Tok
    leaves: list[any]

    def __init__(self, tok:Tok, leaves:List=None) -> None:
        self.tok = tok
        if leaves == None:
            self.leaves = []
        else:
            self.leaves = leaves
    
    def add(self, leaves) -> None:
        self.leaves.append(leaves)

    def printer(self, indent:int=0) -> None:
        shift = ' ' * indent
        print(f'{shift}{str(self.tok)}')

        for leaf in self.leaves:
            if isinstance(leaf, (Tree, Tok)):
                leaf.printer(indent + 1)
            else:
                shift = ' ' * (indent + 1)
                print(f'{shift}{leaf}')  

    def __str__(self) -> str:
        return '{' + f'{self.tok}: {str(self.leaves)}' + '}'


class Parser:

    tree:Tree
    s:TextStream

    def _trace(func:callable):
        def wrapper(*args, **kwargs):
            global indent
            global debug
            shift = '  ' * indent
            indent += 1
            if debug:
                print(f'{shift}[[{func.__name__}]]')
            result = func(*args, **kwargs)
            indent -= 1
            return result
        return wrapper
    
    def __init__(self, filename, showDebug:bool=False) -> None:
        self.s = TextStream(filename)
        global debug 
        debug = showDebug
        self.tree = Tree(Tok(TokType.PROGRAM, 0, 0))

        while not self.s.at_end():
            self.s.skip([' ', '\n', '\t'])
            if self.s.at_end():
                return
            self.tree.add(self.begin())

    def begin(self):
        return self.top_level()
    
    @_trace
    def block(self):
        
        vals = []
        pos = self.s.pos()

        self.s.skip_space()
        self.s.match(TokType.BLOCK.lookup())
        self.s.skip_space(newline=True)

        while not self.s.is_match('}'):
            if self.s.is_match('\n'):
                self.s.match('\n')
                # vals.append(Tok(TokType.LINEBREAK, *self.s.pos()))

            elif self.s.is_match(';'):
                self.s.match(';')
                vals.append(Tok(TokType.STMT_BREAK, *self.s.pos()))
                
            elif self.s.is_match(TokType.COMMENT.lookup()):
                self.s.skip_comment()

            elif self.s.is_match(' '):
                self.s.skip_space()

            else:
                vals.append(self.subst())
                if not self.s.is_match('}'):
                    self.s.match([';', '\n'])
            
        self.s.match('}')

        return Tree(Tok(TokType.BLOCK, *pos), vals)


    '''
    Top Level
    '''

    @_trace
    def top_level(self):
        
        if self.s.is_match(TokType.COMMENT.lookup()):
            pos = self.s.pos()
            self.s.skip_comment()
            return Tree(Tok(TokType.COMMENT, *pos))
            
        if self.s.is_match(TokType.with_attr(TokAttr.TOP_LEVEL)):
            if self.s.is_match(TokType.FUNC.lookup()):
                return self.func_def()
            elif self.s.is_match(TokType.STRUCT.lookup()):
                return self.struct_def()
            elif self.s.is_match(TokType.ENUM.lookup()):
                return self.enum_def()
            elif self.s.is_match(TokType.CONST.lookup()):
                return self.const_def()
            elif self.s.is_match(TokType.VAR.lookup()):
                return self.var_def()
            elif self.s.is_match(TokType.IMPORT.lookup()):
                return self.import_def()
            
        else:
            self.s.expected(TokType.with_attr(TokAttr.TOP_LEVEL))
        
    @_trace
    def func_def(self):
        pos = self.s.pos()
        self.s.match(TokType.FUNC.lookup())
        self.s.skip_space()

        name = self.id()
        self.s.skip_space()

        params = None
        pipe = None
        if self.s.is_match('('):
            pipe = Tok(TokType.PIPE_PAIR, *self.s.pos())
            self.s.match('(')
            self.s.skip_space()
            if self.s.is_match(')'):
                self.s.match(')')
            else:
                params = self.param_seq()
                self.s.match(')')
        
        elif self.s.is_match([TokType.PIPE_DIST.lookup(), TokType.PIPE_FUNNEL.lookup(), TokType.PIPE_PAIR.lookup()]):
            pipePos = self.s.pos()
            if self.s.is_match(TokType.PIPE_DIST.lookup()):
                self.s.match(TokType.PIPE_DIST.lookup())
                pipe = Tok(TokType.PIPE_DIST, *pipePos)
            elif self.s.is_match(TokType.PIPE_FUNNEL.lookup()):
                self.s.match(TokType.PIPE_FUNNEL.lookup())
                pipe = Tok(TokType.PIPE_FUNNEL, *pipePos)
            elif self.s.is_match(TokType.PIPE_PAIR.lookup()):
                self.s.match(TokType.PIPE_PAIR.lookup())
                pipe = Tok(TokType.PIPE_PAIR, *pipePos)
            
            self.s.skip_space()
            params = self.param_seq()
            anyType = Tree(Tok(TokType.TYPE_ANY, params.tok.line, params.tok.col), [])

            # Convert everything to a param seq (of params)
            if params.tok.t in [TokType.PARAM, TokType.ID]:
                if params.tok.t == TokType.ID:
                    params = Tree(Tok(TokType.PARAM_SEQ, params.tok.line, params.tok.line), 
                                  [Tree(Tok(TokType.PARAM, params.tok.line, params.tok.col), [params, anyType, None])])
                elif params.tok.t == TokType.PARAM:
                    params = Tree(Tok(TokType.PARAM_SEQ, params.tok.line, params.tok.line), [params])

            elif params.tok.t == TokType.PARAM_SEQ:
                newLeaves = []
                for p in params.leaves:
                    if p.tok.t == TokType.ID:
                        newLeaves.append(Tree(Tok(TokType.PARAM, params.tok.line, params.tok.col), [p, anyType, None]))
                    else:
                        newLeaves.append(p)

                params.leaves = newLeaves
                    
        self.s.skip_space()
        retType = None
        if self.s.is_match('->'):
            self.s.match('->')
            self.s.skip_space()
            retType = self.type_comp()
        
        self.s.skip_space()
        block = self.block()

        return Tree(Tok(TokType.FUNC, *pos), [name, params, pipe, retType, block])

    @_trace
    def struct_def(self):
        pos = self.s.pos()
        self.s.match(TokType.STRUCT.lookup())
        self.s.skip_space()

        name = self.id()
        self.s.skip_space()
        block = self.block()

        return Tree(Tok(TokType.STRUCT, *pos), [name, block])

    @_trace
    def enum_def(self):
        pos = self.s.pos()
        self.s.match(TokType.ENUM.lookup())
        self.s.skip_space()

        name = self.id()
        self.s.skip_space()

        members = []
        self.s.match('{')
        self.s.skip_space(newline=True)
        while not self.s.is_match('}'):
            if self.s.is_match(TokType.FUNC.lookup()):
                members.append(self.func_def())
            else:
                members.append(self.id())
                
            self.s.skip_space(newline=True)
            
        self.s.match('}')

        return Tree(Tok(TokType.ENUM, *pos), [name, *members])

    @_trace
    def const_def(self):
        pos = self.s.pos()
        self.s.match(TokType.CONST.lookup())
        self.s.skip_space()
        
        if self.s.is_match('{'):
            left = []
            self.s.match('{')
            self.s.skip_space(newline=True)

            while not self.s.is_match('}'):
                left.append(self.param_seq())
                self.s.skip([' ', ';', '\n'])

            self.s.match('}')
            return Tree(Tok(TokType.CONST, *pos), [*left])

        left = self.param_seq(False)
        self.s.skip_space()

        right = None
        if self.s.is_match('='):
            self.s.skip_space()
            self.s.match('=')
            self.s.skip_space()
            right = self.pipeline()
        
        return Tree(Tok(TokType.CONST, *pos), [left, right])
        
    @_trace
    def import_def(self):
        pos = self.s.pos()
        self.s.match(TokType.IMPORT.lookup())
        self.s.skip_space()

        if self.s.is_match('{'):
            left = []
            self.s.match('{')
            self.s.skip_space(newline=True)

            while not self.s.is_match('}'):
                iPos = self.s.pos()
                name, alias = self.import_name()

                left.append(Tree(Tok(TokType.IMPORT, *iPos), [name, alias]))
                self.s.skip_space(newline=True)
                
            self.s.match('}')
            return Tree(Tok(TokType.IMPORT, *pos), [*left])

        name, alias = self.import_name()
        return Tree(Tok(TokType.IMPORT, *pos), [name, alias])

    @_trace
    def import_name(self) -> Tuple:
        left = self.id()
        self.s.skip_space()

        right = None
        if self.s.is_match(TokType.SUBST.lookup()):
            self.s.skip_space()
            self.s.match(TokType.SUBST.lookup())
            self.s.skip_space()
            right = self.id()

        return left, right

    '''
    Statements
    '''
    
    @_trace
    def subst(self):
        
        left = self.stmt()
        # self.s.skip_space()
        if self.s.is_match(TokType.SUBST.lookup()):
            pos = self.s.pos()
            self.s.match(TokType.SUBST.lookup())
            self.s.skip_space()
            right = self.id()
            return Tree(Tok(TokType.SUBST, *pos), [left, right])

        return left

    @_trace
    def stmt(self):    
        if self.s.is_match(TokType.with_attr(TokAttr.TOP_LEVEL)):
            return self.top_level()
        
        elif self.s.is_match(TokType.RETURN.lookup()):
            self.s.match(TokType.RETURN.lookup())
            self.s.skip_space()
            retval = None
            if not self.s.is_match('\n'):
                retval = self.expr_seq()
            return Tree(Tok(TokType.RETURN, *self.s.pos()), [retval])

        elif self.s.is_match(TokType.CONTINUE.lookup()):
            self.s.match(TokType.CONTINUE.lookup())
            self.s.skip_space()
            return Tree(Tok(TokType.CONTINUE, *self.s.pos()), [])

        elif self.s.is_match(TokType.BREAK.lookup()):
            self.s.match(TokType.BREAK.lookup())
            self.s.skip_space()
            breakLabel = None
            if not self.s.is_match('\n'):
                breakLabel = self.id()
            return Tree(Tok(TokType.BREAK, *self.s.pos()), [breakLabel])

        return self.while_stmt()

    @_trace
    def while_stmt(self):

        if self.s.is_match(TokType.WHILE_STMT.lookup()):
            whilePos = self.s.pos()
            self.s.match(TokType.WHILE_STMT.lookup())
            self.s.skip_space()

            cond = self.log_tern()
            self.s.skip_space()

            post = None
            if self.s.is_match(':'):
                self.s.match(':')
                self.s.skip_space()

                post = self.sum()
                self.s.skip_space()
            
            block = self.block()

            return Tree(Tok(TokType.WHILE_STMT, *whilePos), [cond, post, block])

        return self.for_stmt()
    
    @_trace
    def for_stmt(self):

        if self.s.is_match(TokType.FOR_STMT.lookup()):
            
            forPos = self.s.pos()
            self.s.match(TokType.FOR_STMT.lookup())
            self.s.skip_space()

            captures = self.param_seq(False)
            self.s.skip_space()
           
            self.s.match('in')
            self.s.skip_space()

            iterable = self.pipeline()
            # iterable = self.primary()
            # iterable = self.data_range()
            self.s.skip_space()

            block = self.block()

            return Tree(Tok(TokType.FOR_STMT, *forPos), [iterable, captures, block])
        
        return self.if_stmt()

    @_trace
    def if_stmt(self):
        
        if self.s.is_match(TokType.IF_STMT.lookup()):
            self.s.match(TokType.IF_STMT.lookup())
            ifPos = self.s.pos()
            self.s.skip_space()

            cond = self.log_tern()
            self.s.skip_space()

            ifBlock = self.block()
            self.s.skip_space()
            elseIfs = []

            while self.s.is_match(TokType.ELSE_IF_STMT.lookup()):
                elseIfs.append(self.else_if_stmt())
                self.s.skip_space()
            
            if self.s.is_match(TokType.ELSE_STMT.lookup()):
                elseIfs.append(self.else_stmt())
                self.s.skip_space()

            return Tree(Tok(TokType.IF_STMT, *ifPos), [cond, ifBlock, *elseIfs])
            
        return self.assign()
    
    @_trace
    def else_if_stmt(self):
        self.s.match(TokType.ELSE_IF_STMT.lookup())
        self.s.skip_space()
        pos = self.s.pos()
        cond = self.log_tern()
        elseIfBlock = self.block()

        return Tree(Tok(TokType.ELSE_IF_STMT, *pos), [cond, elseIfBlock])
    
    @_trace
    def else_stmt(self):
        self.s.match(TokType.ELSE_STMT.lookup())
        self.s.skip_space()
        elsePos = self.s.pos()
        elseBlock = self.block()

        return Tree(Tok(TokType.ELSE_STMT, *elsePos), [elseBlock])

    @_trace
    def var_def(self):
        pos = self.s.pos()
        self.s.match(TokType.VAR.lookup())
        self.s.skip_space()

        if self.s.is_match('{'):
            left = []
            self.s.match('{')
            self.s.skip_space(newline=True)

            while not self.s.is_match('}'):
                left.append(self.param_seq())
                self.s.skip([' ', ';', '\n'])
                
            self.s.match('}')
            return Tree(Tok(TokType.VAR, *pos), [*left])

        left = self.param_seq(False)
        self.s.skip_space()

        right = None
        if self.s.is_match('='):
            self.s.skip_space()
            self.s.match('=')
            self.s.skip_space()
            right = self.pipeline()
        
        return Tree(Tok(TokType.VAR, *pos), [left, right])

    @_trace
    def assign(self):

        left = self.pipeline()
        self.s.skip_space()

        # Ignore substitution definitions
        if self.s.is_match(TokType.SUBST.lookup()):
            return left

        pos = self.s.pos()
        assign = None
        if self.s.is_match(TokType.ASSIGN.lookup()):
            self.s.match(TokType.ASSIGN.lookup())
            assign = TokType.ASSIGN
        elif self.s.is_match(TokType.ASSIGN_ADD.lookup()):
            self.s.match(TokType.ASSIGN_ADD.lookup())
            assign = TokType.ASSIGN_ADD
        elif self.s.is_match(TokType.ASSIGN_SUB.lookup()):
            self.s.match(TokType.ASSIGN_SUB.lookup())
            assign = TokType.ASSIGN_SUB
        elif self.s.is_match(TokType.ASSIGN_MULT.lookup()):
            self.s.match(TokType.ASSIGN_MULT.lookup())
            assign = TokType.ASSIGN_MULT
        elif self.s.is_match(TokType.ASSIGN_DIV.lookup()):
            self.s.match(TokType.ASSIGN_DIV.lookup())
            assign = TokType.ASSIGN_DIV
        elif self.s.is_match(TokType.ASSIGN_MOD.lookup()):
            self.s.match(TokType.ASSIGN_MOD.lookup())
            assign = TokType.ASSIGN_MOD
        else:
            return left
        
        self.s.skip_space()
        return Tree(Tok(assign, *pos), [left, self.pipeline()])
    
    '''
    Expressions
    '''

    @_trace
    def pipeline(self):
        left = self.expr_seq()
        self.s.skip_space()
        tokType = None

        while self.s.is_match(TokType.with_attr(TokAttr.PIPE)):
            pos = self.s.pos()

            if self.s.is_match(TokType.PIPE_DIST.lookup()):
                self.s.match(TokType.PIPE_DIST.lookup())
                tokType = TokType.PIPE_DIST
            elif self.s.is_match(TokType.PIPE_FUNNEL.lookup()):
                self.s.match(TokType.PIPE_FUNNEL.lookup())
                tokType = TokType.PIPE_FUNNEL
            elif self.s.is_match(TokType.PIPE_PAIR.lookup()):
                self.s.match(TokType.PIPE_PAIR.lookup())
                tokType = TokType.PIPE_PAIR
            elif self.s.is_match(TokType.PIPE_MAP.lookup()):
                self.s.match(TokType.PIPE_MAP.lookup())
                tokType = TokType.PIPE_MAP
            elif self.s.is_match(TokType.PIPE_FILTER.lookup()):
                self.s.match(TokType.PIPE_FILTER.lookup())
                tokType = TokType.PIPE_FILTER
            elif self.s.is_match(TokType.PIPE_REDUCE.lookup()):
                self.s.match(TokType.PIPE_REDUCE.lookup())
                tokType = TokType.PIPE_REDUCE
            elif self.s.is_match(TokType.PIPE_MEMBER.lookup()):
                self.s.match(TokType.PIPE_MEMBER.lookup())
                tokType = TokType.PIPE_MEMBER
            elif self.s.is_match(TokType.PIPE_ZIP.lookup()):
                self.s.match(TokType.PIPE_ZIP.lookup())
                tokType = TokType.PIPE_ZIP
            elif self.s.is_match(TokType.PIPE_FLATTEN.lookup()):
                self.s.match(TokType.PIPE_FLATTEN.lookup())
                tokType = TokType.PIPE_FLATTEN
            elif self.s.is_match(TokType.PIPE_ANY.lookup()):
                self.s.match(TokType.PIPE_ANY.lookup())
                tokType = TokType.PIPE_ANY
            elif self.s.is_match(TokType.PIPE_EACH.lookup()):
                self.s.match(TokType.PIPE_EACH.lookup())
                tokType = TokType.PIPE_EACH
            elif self.s.is_match(TokType.PIPE_SUM.lookup()):
                self.s.match(TokType.PIPE_SUM.lookup())
                tokType = TokType.PIPE_SUM

            self.s.skip_space()
            right = self.expr_seq()
            self.s.skip_space()

            left = Tree(Tok(tokType, *pos), [left, right])

        return left

    @_trace
    def expr_seq(self, allowNewline:bool=False):

        left = self.expr()
        self.s.skip_space()
        pos = self.s.pos()
        right = []

        while self.s.is_match(','):
            self.s.match(',')
            self.s.skip_space(allowNewline)
            right.append(self.expr())
        
        if len(right) == 0:
            return left
        
        right.insert(0, left)
        
        return Tree(Tok(TokType.EXPR_SEQ, *pos), right)

    @_trace
    def expr(self):
        if self.s.is_match(TokType.LAMBDA_EXPR.lookup()):
            return self.lambda_expr()
        else:
            return self.pipe()

    @_trace
    def pipe(self) -> Tree:
        left = self.pipe_side()
        
        while not self.s.is_match(TokType.with_attr(TokAttr.PIPE)) \
                and self.s.is_match(TokType.PIPE.lookup()):
            self.s.match(TokType.PIPE.lookup())
            self.s.skip_space()
            right = self.pipe_side()

            pos = self.s.pos()
            left = Tree(Tok(TokType.PIPE, *pos), [left, right])
        
        return left

    @_trace
    def lambda_expr(self):
        
        pos = self.s.pos()

        self.s.match(TokType.LAMBDA_EXPR.lookup())
        self.s.skip_space()

        params = self.param_seq(False)
        self.s.skip_space()

        right = self.block()
        self.s.skip_space()

        return Tree(Tok(TokType.LAMBDA_EXPR, *pos), [params, right])

    @_trace
    def pipe_side(self):
        left = None
        if self.s.is_match('{'):
            left = self.block()
        else:
            left = self.log_tern()
        self.s.skip_space()
        return left

    @_trace
    def log_tern(self):
        left = self.log_or()
        self.s.skip_space()

        if self.s.is_match(TokType.LOG_TERN.lookup()):
            self.s.match(TokType.LOG_TERN.lookup())
            self.s.skip_space()
            
            pos = self.s.pos()
            ifTrue = self.log_tern()
            self.s.skip_space()

            self.s.match(':')
            self.s.skip_space()

            ifFalse = self.log_tern()
            self.s.skip_space()

            left = Tree(Tok(TokType.LOG_TERN, *pos), [left, ifTrue, ifFalse])
        
        return left
    
    @_trace
    def log_or(self):
        left = self.log_and()
        self.s.skip_space()

        while self.s.is_match(TokType.LOG_OR.lookup()):
            self.s.match(TokType.LOG_OR.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.LOG_OR, *pos), [left, self.log_and()])

        return left

    @_trace
    def log_and(self):
        left = self.log_not()
        self.s.skip_space()

        while self.s.is_match(TokType.LOG_AND.lookup()):
            self.s.match(TokType.LOG_AND.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.LOG_AND, *pos), [left, self.log_not()])

        return left

    @_trace
    def log_not(self):
        
        left = None
        while self.s.is_match(TokType.LOG_NOT.lookup()):
            self.s.match(TokType.LOG_NOT.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.LOG_NOT, *pos), [self.log_not()])

        self.s.skip_space()
        if left is None:
            left = self.comp()
            self.s.skip_space()

        return left

    @_trace
    def comp(self):
        
        left = self.b_not()
        self.s.skip_space()
        pos = self.s.pos()

        while self.s.is_match(TokType.with_attr(TokAttr.COMP)):
            if self.s.is_match(TokType.COMP_EQ.lookup()):
                self.s.match(TokType.COMP_EQ.lookup())
                self.s.skip_space()
                left = Tree(Tok(TokType.COMP_EQ, *pos), [left, self.b_not()])

            elif self.s.is_match(TokType.COMP_NEQ.lookup()):
                self.s.match(TokType.COMP_NEQ.lookup())
                self.s.skip_space()
                left = Tree(Tok(TokType.COMP_NEQ, *pos), [left, self.b_not()])

            elif self.s.is_match(TokType.COMP_LT.lookup()):
                self.s.match(TokType.COMP_LT.lookup())
                self.s.skip_space()
                left = Tree(Tok(TokType.COMP_LT, *pos), [left, self.b_not()])

            elif self.s.is_match(TokType.COMP_GT.lookup()):
                self.s.match(TokType.COMP_GT.lookup())
                self.s.skip_space()
                left = Tree(Tok(TokType.COMP_GT, *pos), [left, self.b_not()])

            elif self.s.is_match(TokType.COMP_LTE.lookup()):
                self.s.match(TokType.COMP_LTE.lookup())
                self.s.skip_space()
                left = Tree(Tok(TokType.COMP_LTE, *pos), [left, self.b_not()])

            elif self.s.is_match(TokType.COMP_GTE.lookup()):
                self.s.match(TokType.COMP_GTE.lookup())
                self.s.skip_space()
                left = Tree(Tok(TokType.COMP_GTE, *pos), [left, self.b_not()])

        self.s.skip_space()
        return left

    @_trace
    def b_not(self):
        
        left = None
        while self.s.is_match(TokType.BIT_NOT.lookup()):
            self.s.match(TokType.BIT_NOT.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_NOT, *pos), [self.b_not()])
        
        if left is None:
            left = self.b_or()

        self.s.skip_space()
        return left

    @_trace
    def b_or(self):
        left = self.b_xor()
        self.s.skip_space()

        while self.s.is_match(TokType.BIT_OR.lookup()):
            self.s.match(TokType.BIT_OR.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_OR, *pos), [left, self.b_xor()])
        
        return left

    @_trace
    def b_xor(self):
        left = self.b_and()
        self.s.skip_space()

        while self.s.is_match(TokType.BIT_XOR.lookup()):
            self.s.match(TokType.BIT_XOR.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_XOR, *pos), [left, self.b_and()])
        
        return left

    @_trace
    def b_and(self):
        left = self.b_shift()
        self.s.skip_space()

        while self.s.is_match(TokType.BIT_AND.lookup()):
            self.s.match(TokType.BIT_AND.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_AND, *pos), [left, self.b_shift()])

        return left

    @_trace
    def b_shift(self):
        
        left = self.data_range()
        self.s.skip_space()

        if self.s.is_match(TokType.BIT_SHL.lookup()):
            self.s.match(TokType.BIT_SHL.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_SHL, *pos), [left, self.b_shift()])
    
        elif self.s.is_match(TokType.BIT_SHR.lookup()):
            self.s.match(TokType.BIT_SHR.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_SHR, *pos), [left, self.b_shift()])
        
        return left

    @_trace
    def data_range(self):
        left = self.sum()
        self.s.skip_space()
        if self.s.is_match(TokType.RANGE.lookup()):
            self.s.match(TokType.RANGE.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.RANGE, *pos), [left, self.sum()])

        return left
    
    @_trace
    def sum(self):

        pos = self.s.pos()
        left = self.term()
        self.s.skip_space()

        while not self.s.is_match('->') \
                and not self.s.is_match(TokType.with_attr(TokAttr.ASSIGN)) \
                and self.s.is_match([TokType.ADD.lookup(), TokType.SUB.lookup()]):

            if self.s.is_match(TokType.ADD.lookup()):
                self.s.match(TokType.ADD.lookup())
                self.s.skip_space()
                pos = self.s.pos()
                left = Tree(Tok(TokType.ADD, *pos), [left, self.term()])

            elif self.s.is_match(TokType.SUB.lookup()):
                self.s.match(TokType.SUB.lookup())
                self.s.skip_space()
                pos = self.s.pos()
                left = Tree(Tok(TokType.SUB, *pos), [left, self.term()])

        return left

    @_trace
    def term(self):

        left = self.factor()
        self.s.skip_space()

        while not self.s.is_match(TokType.with_attr(TokAttr.STAR)) \
                and not self.s.is_match(TokType.with_attr(TokAttr.TERM_ASSIGN)) \
                and self.s.is_match(TokType.with_attr(TokAttr.TERM)):
            
            if self.s.is_match(TokType.MULT.lookup()):
                self.s.match(TokType.MULT.lookup())
                self.s.skip_space()
                pos = self.s.pos()
                left = Tree(Tok(TokType.MULT, *pos), [left, self.factor()])
            
            elif self.s.is_match(TokType.DIV.lookup()):
                self.s.match(TokType.DIV.lookup())
                self.s.skip_space()
                pos = self.s.pos()
                left = Tree(Tok(TokType.DIV, *pos), [left, self.factor()])
            
            elif self.s.is_match(TokType.MOD.lookup()):
                self.s.match(TokType.MOD.lookup())
                self.s.skip_space()
                pos = self.s.pos()
                left = Tree(Tok(TokType.MOD, *pos), [left, self.factor()])
                
        return left

    @_trace
    def factor(self):

        left = None

        if not self.s.is_match(TokType.INCREMENT.lookup()) and self.s.is_match(TokType.POSATE.lookup()):
            self.s.match(TokType.POSATE.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.POSATE, *pos), [self.power()])

        elif not self.s.is_match(TokType.DECREMENT.lookup()) and self.s.is_match(TokType.NEGATE.lookup()):
            self.s.match(TokType.NEGATE.lookup())
            self.s.skip_space()
            pos = self.s.pos()
            left = Tree(Tok(TokType.NEGATE, *pos), [self.power()])
        
        else:
            left = self.power()
            
        return left

    @_trace
    def power(self):

        left = self.crement()
        if self.s.is_match(TokType.POWER.lookup()):
            self.s.match(TokType.POWER.lookup())
            self.s.skip_space()
            pPos = self.s.pos()
            right = self.factor()
            left = Tree(Tok(TokType.POWER, *pPos), [left, right])

        return left

    @_trace
    def crement(self):

        left = self.primary()

        if self.s.is_match(TokType.INCREMENT.lookup()):
            self.s.match(TokType.INCREMENT.lookup())
            left = Tree(Tok(TokType.INCREMENT, *self.s.pos()), [left])
        elif self.s.is_match(TokType.DECREMENT.lookup()):
            self.s.match(TokType.DECREMENT.lookup())
            left = Tree(Tok(TokType.DECREMENT, *self.s.pos()), [left])
        
        return left

    @_trace
    def primary(self):

        left = None
        if self.s.is_match(TokType.SELFMEMBER.lookup()):     # @mem
            self.s.match(TokType.SELFMEMBER.lookup())
            left = Tree(Tok(TokType.SELFMEMBER, *self.s.pos()), [self.primary()])
        elif self.s.is_match(TokType.STRUCTMEMBER.lookup()): # .mem
            self.s.match(TokType.STRUCTMEMBER.lookup())
            left = Tree(Tok(TokType.STRUCTMEMBER, *self.s.pos()), [self.id()])
        elif self.s.is_match(TokType.STREAM.lookup()):       # $$ or $...
            sPos = self.s.pos()
            self.s.match(TokType.STREAM.lookup())
            if self.s.is_match(TokType.STREAM.lookup()):
                self.s.match(TokType.STREAM.lookup())
                left = Tree(Tok(TokType.STREAM, *sPos))
            else:
                left = Tree(Tok(TokType.STREAMINDEX, *sPos), [self.lit_int()])
        elif not self.s.is_match(TokType.LAMBDA_EXPR.lookup()) and \
                self.s.is_match(TokType.DICT_KEY.lookup()):    # :"key"
            self.s.match(TokType.DICT_KEY.lookup())
            if not self.s.is_match(TokType.DICT_KEY.lookup()):
                left = Tree(Tok(TokType.DICT_KEY, *self.s.pos()), [self.primary()])
            else:
                raise SyntaxError("dict key")
        else:
            left = self.atom()

        self.s.skip_space()
        if self.s.is_match(TokType.CALL.lookup()):          # call()
            cPos = self.s.pos()
            self.s.skip_space()
            self.s.match(TokType.CALL.lookup())
            self.s.skip_space(True)

            args = None
            if self.s.is_match(')'):                        # No args call
                self.s.skip_space()
                self.s.match(')')
            else:
                args = self.expr_seq(True)
                self.s.skip_space(True)
                self.s.match(')')
            left = Tree(Tok(TokType.CALL, *cPos), [left, args])

        self.s.skip_space()
        while not self.s.is_match(TokType.RANGE.lookup()) \
                and self.s.is_match([TokType.MEMBER.lookup(), TokType.INDEX.lookup()]):
            self.s.skip_space()
            if self.s.is_match(TokType.MEMBER.lookup()):    # .mem
                self.s.skip_space()
                mPos = self.s.pos()
                self.s.match(TokType.MEMBER.lookup())
                self.s.skip_space()

                member = self.primary()
                left = Tree(Tok(TokType.MEMBER, *mPos), [left, member])
            
            elif self.s.is_match('['):                      # index[]
                cPos = self.s.pos()
                self.s.skip_space()
                self.s.match('[')
                self.s.skip_space()

                args = None
                if self.s.is_match(']'):
                    self.s.skip_space()
                    self.s.match(']')
                else:
                    args = self.expr_seq()
                    self.s.skip_space()
                    self.s.match(']')
                left = Tree(Tok(TokType.INDEX, *cPos), [left, args])

        return left

    @_trace
    def atom(self):
        left = None
        if self.s.is_match(ALPHAS + ['_']):
            left = self.id()                        
        elif self.s.is_match('['):
            left = self.list_raw()
        else:
            left = self.literal()

        return left

    @_trace
    def list_raw(self):
        pos = self.s.pos()
        self.s.match('[')
        self.s.skip_space(True)
        args = None
        if self.s.is_match(']'):
            self.s.match(']')
            self.s.skip_space(True)
        else:
            args = self.expr_seq(True)
            self.s.match(']')
            self.s.skip_space(True)

        return Tree(Tok(TokType.LIST_RAW, *pos), [args])

    @_trace
    def param_seq(self, allowDefault:bool=True):
        
        pos = self.s.pos()
        left = self.param(allowDefault)
        params = []
                
        while self.s.is_match(','):
            self.s.match(',')
            self.s.skip_space(newline=True)
            params.append(self.param(allowDefault))
        
        if len(params) == 0:
            return left
        
        params.insert(0, left)
        return Tree(Tok(TokType.PARAM_SEQ, *pos), params)
    
    @_trace
    def param(self, allowDefault:bool=True):
        
        pos = self.s.pos()
        left = self.id()
        tComp = TokType.TYPE_ANY
        default = None

        if self.s.find(':'):
            self.s.skip_space()
        
        if self.s.is_match(':'):
            self.s.match(':')
            self.s.skip_space()
            tComp = self.type_comp()
            self.s.skip_space()
        
        if self.s.find('='):
            self.s.skip_space()

        if allowDefault and self.s.is_match('='):
            self.s.match('=')
            self.s.skip_space()
            default = self.expr()
        
        return Tree(Tok(TokType.PARAM, *pos), [left, tComp, default])
    
    @_trace
    def type_comp(self):

        pos = self.s.pos()
        inType = None

        if self.s.is_match(TokType.TYPE_LIST.lookup()):
            self.s.match(TokType.TYPE_LIST.lookup())
            if self.s.is_match('<'):
                self.s.match('<')
                self.s.skip_space()
                inType = self.type_comp()
                self.s.skip_space()
                self.s.match('>')
            return Tree(Tok(TokType.TYPE_LIST, *pos), [inType])

        elif self.s.is_match(TokType.TYPE_DICT.lookup()):
            self.s.match(TokType.TYPE_DICT.lookup())
            if self.s.is_match('<'):
                self.s.match('<')
                self.s.skip_space()
                inType = self.type_comp()
                self.s.skip_space()
                inType2 = None
                if self.s.is_match(','):
                    self.s.match(',')
                    self.s.skip_space()
                    inType2 = self.type_comp()
                    self.s.skip_space()
                self.s.match('>')
            return Tree(Tok(TokType.TYPE_DICT, *pos), [inType])

        else:
            return self.type_prim()

    @_trace
    def type_prim(self):

        pos = self.s.pos()
        # name = self.id()
        name = self.primary()   # TODO verify this
        
        # TODO make this not terrible (use lookup)
        if name.leaves[0] == TokType.TYPE_INT.lookup():
            return Tree(Tok(TokType.TYPE_INT, *pos), [])
        elif name.leaves[0] == TokType.TYPE_FLOAT.lookup():
            return Tree(Tok(TokType.TYPE_FLOAT, *pos), [])
        elif name.leaves[0] == TokType.TYPE_STRING.lookup():
            return Tree(Tok(TokType.TYPE_STRING, *pos), [])
        elif name.leaves[0] == TokType.TYPE_BOOL.lookup():
            return Tree(Tok(TokType.TYPE_BOOL, *pos), [])
        elif name.leaves[0] == TokType.TYPE_NULL.lookup():
            return Tree(Tok(TokType.TYPE_NULL, *pos), [])
        elif name.leaves[0] == TokType.TYPE_ANY.lookup():
            return Tree(Tok(TokType.TYPE_ANY, *pos), [])
        
        else:
            return Tree(Tok(TokType.TYPE_DEF, *pos), [name])
        
    @_trace
    def id(self):
        val = ''
        line, col = self.s.pos()

        val += self.s.match(ALPHAS + ['_'])
        while self.s.is_match(ALPHAS + DIGITS + ['_']):
            val += self.s.match(ALPHAS + DIGITS + ['_'])
        
        tokType = TokType.ID
        
        # TODO make this not terrible (use toktype dict lookup)
        if val == TokType.TYPE_LIST.lookup():
            tokType = TokType.TYPE_LIST
        elif val == TokType.TYPE_DICT.lookup():
            tokType = TokType.TYPE_DICT

        elif val == TokType.LIT_TRUE.lookup():
            tokType = TokType.LIT_TRUE
        elif val == TokType.LIT_FALSE.lookup():
            tokType = TokType.LIT_FALSE

        elif val == TokType.TYPE_INT.lookup():
            tokType = TokType.TYPE_INT
        elif val == TokType.TYPE_FLOAT.lookup():
            tokType = TokType.TYPE_FLOAT
        elif val == TokType.TYPE_STRING.lookup():
            tokType = TokType.TYPE_STRING
        elif val == TokType.TYPE_BOOL.lookup():
            tokType = TokType.TYPE_BOOL
        elif val == TokType.TYPE_NULL.lookup():
            tokType = TokType.TYPE_NULL
        elif val == TokType.TYPE_ANY.lookup():
            tokType = TokType.TYPE_ANY

        elif val in [t.lookup() for t in TokType]:
            raise SyntaxError(f'id: reserved keyword:\t`{val}`')

        return Tree(Tok(tokType, line, col), [val])
    
    @_trace
    def literal(self):
        if self.s.is_match('\"'):
            val = self.lit_string()
        else:
            val = self.lit_float()
        
        return val

    @_trace
    def lit_string(self):
        val = []
        line, col = self.s.pos()

        self.s.match('\"')
        while not self.s.is_match('\"'):
            if self.s.is_match('\n') or self.s.at_end():
                self.s.expected('\"')
            elif self.s.is_match('{'):
                val.append(self.block())
            elif self.s.is_match('\\'):
                val.append(self.esc_char())
            else:
                val.append(self.str_base())
        self.s.match('\"')
        
        return Tree(Tok(TokType.LIT_STRING, line, col), val)

    @_trace
    def str_base(self):
        val = ''
        line, col = self.s.pos()

        while not self.s.is_match(['\"', '{', '\\', '\n']):
            temp = self.s.consume()
            if temp is None:
                break
            else:
                val += temp

        return Tree(Tok(TokType.STR_BASE, line, col), [val])

    @_trace
    def esc_char(self):
        val = ''
        line, col = self.s.pos()
        
        val += self.s.match('\\')
        val += self.s.match(['\\', 'b', 't', 'f', 'b', 'n', '\"'])
        
        return Tree(Tok(TokType.ESC_CHAR, line, col), [val])

    @_trace
    def lit_float(self) -> Tree:
        val = ''
        line, col = self.s.pos()
        left = self.lit_int()

        # Ignore ranges
        if self.s.is_match(TokType.RANGE.lookup()):
            return left

        # Float
        if self.s.is_match('.'):
            dot = self.s.match('.')
            right = self.lit_int()
            val = str(left.leaves[0] + dot + right.leaves[0])
            return Tree(Tok(TokType.LIT_FLOAT, line, col), [val])
        
        # Otherwise just the int
        return left

    @_trace
    def lit_int(self) -> Tree:
        val = ''
        line, col = self.s.pos()

        if self.s.is_match('('):
            self.s.match('(')
            left = None
            if self.s.is_match('{'):
                left = self.block()
            else:
                left = self.pipeline()
            self.s.match(')')
            return left

        if self.s.at_end():
            raise NotImplementedError('at end')
            return

        if self.s.is_match(DIGITS):
            val += self.s.match(DIGITS)
        else:
            raise SyntaxError(f'Unexpected token: `{self.s.curr()}` \tat line {self.s.line}, col {self.s.col}')

        while self.s.is_match(DIGITS):
            val += self.s.match(DIGITS)
        
        return Tree(Tok(TokType.LIT_INT, line, col), [val])


def main():

    # sys.tracebacklimit = 0
    
    if len(sys.argv) > 1:
        f = sys.argv[1]
        p = Parser(f, False)
        p.tree.printer()

if __name__ == '__main__':
    main()