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

a()[].b()--**+2++


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
            else:
                return None
            
            c = self.consume()
        
        return c

    def expected(self, cmatch:List[str]|str, got:str|None=None) -> SyntaxError:
        if got is None:
            got = self.curr()

        if isinstance(cmatch, list) and len(cmatch) > 10:
            cmatch = f'[{cmatch[0]}, {cmatch[1]} ... {cmatch[-2]}, {cmatch[-1]}]'
        
        raise SyntaxError(f'{self.name} [{self.line}:{self.col}]\tExpected token: {cmatch}\t(got {repr(got)})')


class TokType(Enum):
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
    values:list

    line:int    
    col:int

    def __init__(self, t:TokType, value:list, line:int, col:int) -> None:
        self.t, self.values, self.line, self.col = t, value, line, col

    def tree(self, indent:int=0):
        shift = '  ' * indent
        print(f'{shift}{self.t:20}\t({self.line}:{self.col})\t')

        for t in self.values:
            if isinstance(t, Tok):
                t.tree(indent+1)
            else:
                shift = '  ' * (indent+1)
                print(f'{shift}{repr(t)}')

    def simple(self, indent:int=0):
        for t in self.values:
            if isinstance(t, Tok):
                t.simple(indent+1)
            else:
                shift = '  ' * (indent+1)
                print(f'{shift}{repr(t)}')

class Lexer:

    toks:list[Tok]
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
        self.toks = []

        while not self.s.at_end():
            self.toks.append(self.begin())


    def begin(self):
        return self.sum()

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
                val.append(self.begin())

        self.s.match('}')

        return Tok(TokType.BLOCK, val, line, col)

    @_trace
    def b_and(self):
        pos = self.s.pos()
        left = self.b_shift()

        while self.s.is_match('*&'):
            self.s.match('*&')
            # TODO

    @_trace
    def b_shift(self):
        pos = self.s.pos()
        left = self.data_range()
        
        if self.s.is_match('<<'):
            self.s.match('<<')
            return Tok(TokType.BIT_SHL, left, *pos)
        elif self.s.is_match('>>'):
            self.s.match('>>')
            return Tok(TokType.BIT_SHR, left, *pos)
        
        return left

    @_trace
    def data_range(self):
        val = []
        pos = self.s.pos()
        val.append(self.sum())
        if self.s.is_match('..'):
            self.s.match('..')
            val.append(self.sum())

        return Tok(TokType.RANGE, val, *pos)

    @_trace
    def sum(self):
        val = []
        sPos = self.s.pos()

        val.append(self.term())

        if self.s.is_match('+'):
            self.s.match('+')
            pos = self.s.pos()
            val.append(Tok(TokType.ADD, [self.term()], *pos))

        elif self.s.is_match('-'):
            self.s.match('-')
            pos = self.s.pos()
            val.append(Tok(TokType.SUB, [self.term()], *pos))

        return Tok(TokType.SUM, val, *sPos)

    @_trace
    def term(self):
        val = []
        tPos = self.s.pos()

        val.append(self.factor())

        if self.s.is_match('*'):
            self.s.match('*')
            pos = self.s.pos()
            val.append(Tok(TokType.MULT, [self.factor()], *pos))
        
        elif self.s.is_match('/'):
            self.s.match('/')
            pos = self.s.pos()
            val.append(Tok(TokType.DIV, [self.factor()], *pos))
        
        elif self.s.is_match('%'):
            self.s.match('%')
            pos = self.s.pos()
            val.append(Tok(TokType.MOD, [self.factor()], *pos))
               
        return Tok(TokType.TERM, val, *tPos)

    @_trace
    def factor(self):
        val = []
        fPos = self.s.pos()

        if self.s.is_match('+'):
            self.s.match('+')
            pos = self.s.pos()
            val.append(Tok(TokType.POSATE, [self.power()], *pos))

        elif self.s.is_match('-'):
            self.s.match('-')
            pos = self.s.pos()
            val.append(Tok(TokType.NEGATE, [self.power()], *pos))
        
        else:
            val.append(self.power())
            
        return Tok(TokType.FACTOR, val, *fPos)

    @_trace
    def power(self):
        pos = self.s.pos()
        val = [self.crement()]

        if self.s.is_match('**'):
            self.s.match('**')
            val.append(self.factor())

        return Tok(TokType.POWER, val, *pos)

    @_trace
    def crement(self):
        val = []
        line, col = self.s.pos()

        val.append(self.primary())

        if self.s.is_match('++'):
            self.s.match('++')
            val.append(Tok(TokType.INCREMENT, ['++'], *self.s.pos()))
        elif self.s.is_match('--'):
            self.s.match('--')
            val.append(Tok(TokType.DECREMENT, ['--'], *self.s.pos()))
        
        return Tok(TokType.CREMENT, val, line, col)

    @_trace
    def primary(self):
        val = []
        pPos= self.s.pos()

        if self.s.is_match('@'):
            self.s.match('@')
            sPos = self.s.pos()
            selfMember = self.primary()
            val.append(Tok(TokType.SELFMEMBER, [selfMember], *sPos))

            return Tok(TokType.PRIMARY, val, *pPos)

        val.append(self.atom())

        if self.s.is_match('('):
            cPos = self.s.pos()
            self.s.match('(')
            args = self.args()
            self.s.match(')')
            val.append(Tok(TokType.CALL, [val.pop(), args], *cPos))

        while not self.s.is_match('..') and self.s.is_match(['.', '[']):
            if self.s.is_match('.'):
                mPos = self.s.pos()
                self.s.match('.')
                member = self.primary()
                val.append(Tok(TokType.MEMBER, [member], *mPos))
            
            elif self.s.is_match('['):
                cPos = self.s.pos()
                self.s.match('[')
                args = self.args()
                self.s.match(']')
                val.append(Tok(TokType.INDEX, [val.pop(), args], *cPos))

        return Tok(TokType.PRIMARY, val, *pPos)

    @_trace
    def args(self):
        # TODO
        pos = self.s.pos()
        return Tok(TokType.ARGS, [[]], *pos)

    @_trace
    def atom(self):
        val = []
        line, col = self.s.pos()

        if self.s.is_match(ALPHAS + ['_']):
            val.append(self.id())
        else:
            val.append(self.literal())
        
        return Tok(TokType.ATOM, val, line, col)

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

        return Tok(tokType, [val], line, col)


    @_trace
    def literal(self):
        val = None
        line, col = self.s.pos()
        
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
        
        return Tok(TokType.LIT_STRING, val, line, col)

    @_trace
    def str_base(self):
        val = ''
        line, col = self.s.pos()

        while not self.s.is_match(['\"', '{', '}']):
            temp = self.s.consume()
            if temp is None:
                break
            else:
                val += temp

        return Tok(TokType.STR_BASE, [val], line, col)

    @_trace
    def esc_char(self):
        val = ''
        line, col = self.s.pos()
        
        val += self.s.match('\\')
        val += self.s.match(['\\', 'b', 't', 'f', 'b', 'n', '\"'])
        
        return Tok(TokType.ESC_CHAR, [val], line, col)

    @_trace
    def lit_float(self):
        val = ''
        line, col = self.s.pos()
        left = self.lit_int()

        if self.s.is_match('..'):
            return left

        # Float
        if self.s.is_match('.'):
            dot = self.s.match('.')
            right = self.lit_int()
            val = left.values + dot + right.values
            return Tok(TokType.LIT_FLOAT, [val], line, col)
        
        # Otherwise just the int
        return left

    @_trace
    def lit_int(self) -> Tok:
        val = ''
        line, col = self.s.pos()

        val += self.s.match(DIGITS)
        while self.s.is_match(DIGITS):
            val += self.s.match(DIGITS)
        
        return Tok(TokType.LIT_INT, [val], line, col)

lexer = Lexer('test.pb')


print('-'*50)

# pprint(lexer.toks)

for tok in lexer.toks:
    tok.tree()
    # tok.simple()