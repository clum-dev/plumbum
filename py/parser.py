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

indent = 0

'''
TEST STRINGS:

a()[].b()--**+2++..c().d()

'''

class TextStream:
    
    name: str
    
    text: str
    index: int

    line: int
    col: int

    gotMatch: str
    
    def __init__(self, filename:str) -> None:

        with open(filename, 'r') as f:
            self.name = filename
            self.text = f.read()
            self.index = 0
            self.line, self.col = 0, 0 
            self.gotMatch = None

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
    
    def match(self, cmatch:List[str]|str) -> str|None:
        if not self.is_match(cmatch):
            self.expected(cmatch)

        if isinstance(cmatch, list) and len(cmatch) > 10:
            cmatch = f'[{cmatch[0]}, {cmatch[1]} ... {cmatch[-2]}, {cmatch[-1]}]'

        global indent
        shift = '  ' * indent
        print(f'{shift}matched {self.gotMatch} to {cmatch}')
        
        for _ in self.gotMatch:
            out = self.consume()

        self.skip(' ')  # TODO get this to skip spaces properly

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
        c = self.curr()
        
        while c != None:
            if isinstance(cmatch, list):
                if c not in cmatch:
                    break
            elif isinstance(cmatch, str):
                if c != cmatch:
                    break    
            c = self.consume()
        
        return c

    def expected(self, cmatch:List[str]|str, got:str|None=None) -> SyntaxError:
        if got is None:
            got = self.curr()

        if isinstance(cmatch, list) and len(cmatch) > 10:
            cmatch = f'[{cmatch[0]}, {cmatch[1]} ... {cmatch[-2]}, {cmatch[-1]}]'
        
        raise SyntaxError(f'{self.name} [{self.line}:{self.col}]\tExpected token: {cmatch}\t(got {repr(got)})')


class TokType(Enum):
    PROGRAM =       ['PROGRAM', None]
    EOF =           ['EOF', None]
    LINEBREAK =     ['LINEBREAK', '\n']

    BLOCK =         ['BLOCK', None]

    LOG_TERN =      ['LOG_TERN', '?']
    LOG_OR =        ['LOG_OR', 'or']
    LOG_AND =       ['LOG_AND', 'and']
    LOG_NOT =       ['LOG_NOT', 'not']

    COMP_EQ =       ['COMP_EQ', '==']
    COMP_NEQ =      ['COMP_NEQ', '!=']
    COMP_LT =       ['COMP_LT', '<']
    COMP_GT =       ['COMP_GT', '>']
    COMP_LTE =      ['COMP_LTE', '<=']
    COMP_GTE =      ['COMP_GTE', '>=']

    BIT_NOT =       ['BIT_NOT', '*~']
    BIT_OR =        ['BIT_OR', '*|']
    BIT_XOR =       ['BIT_XOR', '*^']
    BIT_AND =       ['BIT_AND', '*&']
    BIT_SHR =       ['BIT_SHR', '>>']
    BIT_SHL =       ['BIT_SHL', '<<']

    RANGE =         ['RANGE', '..']

    SUM =           ['SUM', None]
    ADD =           ['ADD', '+']
    SUB =           ['SUB', '-']

    TERM =          ['TERM', None]
    MULT =          ['MULT', '*']
    DIV =           ['DIV', '/']
    MOD =           ['MOD', '%']
    
    FACTOR =        ['FACTOR', None]
    POSATE =        ['POSATE', '+']
    NEGATE =        ['NEGATE', '-']
    
    POWER =         ['POWER', '**']
    
    CREMENT =       ['CREMENT', None]
    INCREMENT =     ['INCREMENT', '++']
    DECREMENT =     ['DECREMENT', '--']

    PRIMARY =       ['PRIMARY', None]
    SELFMEMBER =    ['SELFMEMBER', None]
    MEMBER =        ['MEMBER', None]
    INDEX =         ['INDEX', None]
    CALL =          ['CALL', None]

    ARGS =          ['ARGS', None]
    ATOM =          ['ATOM', None]
    ID =            ['ID', None]

    LIT_INT =       ['LIT_INT', None]
    LIT_FLOAT =     ['LIT_FLOAT', None]
    LIT_STRING =    ['LIT_STRING', None]
    LIT_TRUE =      ['LIT_TRUE', 'true']
    LIT_FALSE =     ['LIT_FALSE', 'false']
    ESC_CHAR =      ['ESC_CHAR', None]
    STR_BASE =      ['STR_BASE', None]

    def get_dict() -> dict:
        return {t.value[1] : t for t in TokType}


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


class Lexer:

    tree:Tree
    s:TextStream

    def _trace(func:callable):
        def wrapper(*args, **kwargs):
            global indent
            shift = '  ' * indent
            indent += 1
            print(f'{shift}[[{func.__name__}]]')
            result = func(*args, **kwargs)
            indent -= 1
            return result
        return wrapper
    
    def __init__(self, filename) -> None:
        self.s = TextStream(filename)
        self.tree = Tree(Tok(TokType.PROGRAM, 0, 0))

        while not self.s.at_end():
            self.tree.add(self.begin())

    def begin(self):
        return self.comp()
    
    @_trace
    def block(self):
        val = []
        line, col = self.s.pos()
        
        self.s.match('{')
        while not self.s.is_match('}'):
            if self.s.is_match(WHITESPACE):
                self.s.consume()
            elif self.s.is_match('\n'):
                self.s.consume()
                val.append(Tok(TokType.LINEBREAK, '\n', *self.s.pos()))

            elif self.s.is_match('{'):
                val.append(self.block())
                
            else:
                val.append(self.sum())

        self.s.match('}')

        return Tok(TokType.BLOCK, val, line, col)

    @_trace
    def log_not(self):
        
        left = None
        while self.s.is_match('not'):
            self.s.match('not')
            pos = self.s.pos()
            left = Tree(Tok(TokType.LOG_NOT, *pos), [self.log_not()])
        
        if left is None:
            left = self.comp()

        return left

    @_trace
    def comp(self):
        
        left = self.b_not()

        while self.s.is_match(['==', '!=', '<', '>', '<=', '>=']):
            if self.s.is_match('=='):
                self.s.match('==')
                left = Tree(Tok(TokType.COMP_EQ, *self.s.pos()), [left, self.b_not()])

            elif self.s.is_match('!='):
                self.s.match('!=')
                left = Tree(Tok(TokType.COMP_NEQ, *self.s.pos()), [left, self.b_not()])

            elif self.s.is_match('<'):
                self.s.match('<')
                left = Tree(Tok(TokType.COMP_LT, *self.s.pos()), [left, self.b_not()])

            elif self.s.is_match('>'):
                self.s.match('>')
                left = Tree(Tok(TokType.COMP_GT, *self.s.pos()), [left, self.b_not()])

            elif self.s.is_match('<='):
                self.s.match('<=')
                left = Tree(Tok(TokType.COMP_LTE, *self.s.pos()), [left, self.b_not()])

            elif self.s.is_match('>='):
                self.s.match('>=')
                left = Tree(Tok(TokType.COMP_GTE, *self.s.pos()), [left, self.b_not()])
            
        return left

    @_trace
    def b_not(self):
        
        left = None
        while self.s.is_match('*~'):
            self.s.match('*~')
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_NOT, *pos), [self.b_not()])
        
        if left is None:
            left = self.b_or()

        return left

    @_trace
    def b_or(self):
        left = self.b_xor()

        while self.s.is_match('*|'):
            self.s.match('*|')
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_OR, *pos), [left, self.b_xor()])
        
        return left

    @_trace
    def b_xor(self):
        left = self.b_and()

        while self.s.is_match('*^'):
            self.s.match('*^')
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_XOR, *pos), [left, self.b_and()])
        
        return left

    @_trace
    def b_and(self):
        left = self.b_shift()

        while self.s.is_match('*&'):
            self.s.match('*&')
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_AND, *pos), [left, self.b_shift()])

        return left

    @_trace
    def b_shift(self):
        
        left = self.data_range()
        if self.s.is_match('<<'):
            self.s.match('<<')
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_SHL, *pos), [left, self.b_shift()])
    
        elif self.s.is_match('>>'):
            self.s.match('>>')
            pos = self.s.pos()
            left = Tree(Tok(TokType.BIT_SHR, *pos), [left, self.b_shift()])
        
        return left

    @_trace
    def data_range(self):
        left = self.sum()
        if self.s.is_match('..'):
            self.s.match('..')
            pos = self.s.pos()
            left = Tree(Tok(TokType.RANGE, *pos), [left, self.sum()])

        return left

    @_trace
    def sum(self):

        pos = self.s.pos()
        left = self.term()

        while self.s.is_match(['+', '-']):
            if self.s.is_match('+'):
                self.s.match('+')
                pos = self.s.pos()
                left = Tree(Tok(TokType.ADD, *pos), [left, self.term()])

            elif self.s.is_match('-'):
                self.s.match('-')
                pos = self.s.pos()
                left = Tree(Tok(TokType.SUB, *pos), [left, self.term()])

        return left

    @_trace
    def term(self):

        left = self.factor()

        while not self.s.is_match(['*&', '*^', '*|', '*~']) and self.s.is_match(['*', '/', '%']):
            if self.s.is_match('*'):
                self.s.match('*')
                pos = self.s.pos()
                left = Tree(Tok(TokType.MULT, *pos), [left, self.factor()])
            
            elif self.s.is_match('/'):
                self.s.match('/')
                pos = self.s.pos()
                left = Tree(Tok(TokType.DIV, *pos), [left, self.factor()])
            
            elif self.s.is_match('%'):
                self.s.match('%')
                pos = self.s.pos()
                left = Tree(Tok(TokType.MOD, *pos), [left, self.factor()])
                
        return left

    @_trace
    def factor(self):

        left = None

        if self.s.is_match('+'):
            self.s.match('+')
            pos = self.s.pos()
            left = Tree(Tok(TokType.POSATE, *pos), [self.power()])

        elif self.s.is_match('-'):
            self.s.match('-')
            pos = self.s.pos()
            left = Tree(Tok(TokType.NEGATE, *pos), [self.power()])
        
        else:
            left = self.power()
            
        return left

    @_trace
    def power(self):

        left = self.crement()
        if self.s.is_match('**'):
            self.s.match('**')
            pPos = self.s.pos()
            right = self.factor()
            left = Tree(Tok(TokType.POWER, *pPos), [left, right])

        return left

    @_trace
    def crement(self):

        pos = self.s.pos()
        left = self.primary()

        if self.s.is_match('++'):
            self.s.match('++')
            left = Tree(Tok(TokType.INCREMENT, *self.s.pos()), [left])
        elif self.s.is_match('--'):
            self.s.match('--')
            left = Tree(Tok(TokType.DECREMENT, *self.s.pos()), [left])
        
        return left

    @_trace
    def primary(self):

        left = None
        if self.s.is_match('@'):
            self.s.match('@')
            left = Tree(Tok(TokType.SELFMEMBER, *self.s.pos()), [self.primary()])
        else:
            left = self.atom()

        if self.s.is_match('('):
            cPos = self.s.pos()
            self.s.match('(')
            args = self.args()
            self.s.match(')')
            left = Tree(Tok(TokType.CALL, *cPos), [left, args])

        while not self.s.is_match('..') and self.s.is_match(['.', '[']):
            if self.s.is_match('.'):
                mPos = self.s.pos()
                self.s.match('.')
                member = self.primary()
                left = Tree(Tok(TokType.MEMBER, *mPos), [left, member])
            
            elif self.s.is_match('['):
                cPos = self.s.pos()
                self.s.match('[')
                args = self.args()
                self.s.match(']')
                left = Tree(Tok(TokType.INDEX, *cPos), [left, args])

        return left

    @_trace
    def args(self):
        # TODO
        return Tree(Tok(TokType.ARGS, *self.s.pos()), [[]])

    @_trace
    def atom(self):
        left = None
        if self.s.is_match(ALPHAS + ['_']):
            left = self.id()
        else:
            left = self.literal()
        return left

    @_trace
    def id(self):
        val = ''
        line, col = self.s.pos()

        val += self.s.match(ALPHAS + ['_'])
        while self.s.is_match(ALPHAS + DIGITS + ['_']):
            val += self.s.match(ALPHAS + DIGITS + ['_'])
        
        tokType = TokType.ID
        if val == 'true':
            tokType = TokType.LIT_TRUE
        elif val == 'false':
            tokType = TokType.LIT_FALSE

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
            if self.s.at_end():
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

        while not self.s.is_match(['\"', '{', '}', '\\']):
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
        if self.s.is_match('..'):
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

        val += self.s.match(DIGITS)
        while self.s.is_match(DIGITS):
            val += self.s.match(DIGITS)
        
        return Tree(Tok(TokType.LIT_INT, line, col), [val])


lexer = Lexer('test.pb')

print('-'*50)

lexer.tree.printer()