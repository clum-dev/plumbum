from dataclasses import dataclass
from enum import Enum
from typing import List
from pprint import pprint

class OpType(Enum):
    NONE=0
    UNARY_L=1
    UNARY_R=2
    BINARY=3

# @dataclass
class Token:
    raw: str
    ttype: str
    opType:OpType=OpType.NONE

    def __init__(self, raw:str, ttype:str, opType:OpType=OpType.NONE) -> None:
        self.raw, self.ttype, self.opType = raw, ttype, opType

    def __repr__(self) -> str:
        return f'{self.ttype}({self.raw})'


T_PARSING = {
    ' ': Token(' ', 'T_SPACE'),
}

T_TOP_LEVEL = {
    'func': Token('func', 'T_FUNC'),
    'struct': Token('struct', 'T_STRUCT'),
    'enum': Token('enum', 'T_ENUM'),
    'const': Token('const', 'T_CONST'),
    'use': Token('use', 'T_USE'),
}

T_BOOL_LIT = {
    'true': Token('true', 'T_TRUE'),
    'false': Token('false', 'T_FALSE'),
}

T_CONTROL_FLOW = {
    'if': Token('if', 'T_IF'),
    'else': Token('else', 'T_ELSE'),
    'for': Token('for', 'T_FOR'),
    'while': Token('while', 'T_WHILE'),
    'break': Token('break', 'T_BREAK'),
    'continue': Token('continue', 'T_CONTINUE'),
    'return': Token('return', 'T_RETURN'),
}

T_MISC_SYM = {
    '=': Token('=', 'T_EQUAL'),
    '#': Token('#', 'T_HASH'),
    '"': Token('"', 'T_QUOTE'),
    ':': Token(':', 'T_COLON', OpType.BINARY),
    '::': Token('::', 'T_COLON2', OpType.BINARY),
    ':>': Token(':>', 'T_COLONRARROW', OpType.BINARY),  # Ternary
    ';': Token(';', 'T_SEMICOLON'),
    ',': Token(',', 'T_COMMA'),
    '$': Token('$', 'T_DOLLAR', OpType.UNARY_L),
    '&': Token('&', 'T_AMPERSAND'),
    '@': Token('@', 'T_AT', OpType.UNARY_L),
    '?': Token('?', 'T_QUESTION', OpType.BINARY),
    '_': Token('_', 'T_UNDERSCORE'),
    '.': Token('.', 'T_DOT', OpType.BINARY),
    '..': Token('..', 'T_DOT2', OpType.BINARY),
    '->': Token('->', 'T_RARROW', OpType.BINARY),
    '=>': Token('=>', 'T_RARROW2', OpType.BINARY)
}

T_BRACKETS = {
    '(': Token('(', 'T_LPAREN'),
    ')': Token(')', 'T_RPAREN'),
    '[': Token('[', 'T_LBRACKET'),
    ']': Token(']', 'T_RBRACKET'),
    '{': Token('{', 'T_LBRACE'),
    '}': Token('}', 'T_RBRACE'),
    '<': Token('<', 'T_LANGLE', OpType.BINARY),
    '>': Token('>', 'T_RANGLE', OpType.BINARY),
}

T_MATH_OPS = {
    '+': Token('+', 'T_PLUS', OpType.BINARY),
    '-': Token('-', 'T_MINUS', OpType.BINARY),
    '*': Token('*', 'T_ASTERISK', OpType.BINARY),
    '/': Token('/', 'T_SLASH', OpType.BINARY),
    '%': Token('%', 'T_PERCENT', OpType.BINARY),
    '**': Token('**', 'T_ASTERISK2', OpType.BINARY),
    '++': Token('++', 'T_PLUS2', OpType.UNARY_R),
    '--': Token('--', 'T_MINUS2', OpType.UNARY_R),
}

T_LOG_OPS = {
    'and': Token('and', 'T_AND', OpType.BINARY),
    'or': Token('or', 'T_OR', OpType.BINARY),
    'not': Token('not', 'T_NOT', OpType.UNARY_L),
}

T_COMP_OPS = {
    '==': Token('==', 'T_EQUAL2', OpType.BINARY),
    '!=': Token('!=', 'T_BANGEQUAL', OpType.BINARY),
    '<=': Token('<=', 'T_LANGLEEQUAL', OpType.BINARY),
    '>=': Token('>=', 'T_RANGLEEQUAL', OpType.BINARY),
    '<': Token('<', 'T_LANGLE', OpType.BINARY),
    '>': Token('>', 'T_RANGLE', OpType.BINARY),
}

T_PIPES_BASIC = {
    '|': Token('|', 'T_PIPE', OpType.BINARY),
    '|>': Token('|>', 'T_PIPEFUNNEL', OpType.BINARY),
    '|<': Token('|<', 'T_PIPEDIST', OpType.BINARY),
    '|:': Token('|:', 'T_PIPEPAIR', OpType.BINARY),
    '|=': Token('|=', 'T_PIPE_CAST', OpType.BINARY),
    '|+': Token('|+', 'T_PIPESUM', OpType.BINARY),
}

T_PIPES_STREAM = {
    '|@': Token('|@', 'T_PIPEMAP', OpType.BINARY),
    '|?': Token('|?', 'T_PIPEFILTER', OpType.BINARY),
    '|_': Token('|_', 'T_PIPEREDUCE', OpType.BINARY),
    '|%': Token('|%', 'T_PIPESCAN', OpType.BINARY),
}

T_PIPES_OTHER = {
    '|~': Token('|~', 'T_PIPEREGEX', OpType.BINARY),
}

T_TYPES_PRIMITIVE = {
    'any': Token('any', 'T_TYPE_ANY'),
    'int': Token('int', 'T_TYPE_INT'),
    'float': Token('float', 'T_TYPE_FLOAT'),
    'bool': Token('bool', 'T_TYPE_BOOL'),
    'null': Token('null', 'T_TYPE_NULL'),
}

T_TYPES_COMPLEX = {
    'String': Token('String', 'T_TYPE_STR'),
    'List': Token('List', 'T_TYPE_LIST'),
    'Dict': Token('Dict', 'T_TYPE_DICT'),
}

TOKENS =    T_PARSING |\
            T_TOP_LEVEL |\
            T_BOOL_LIT |\
            T_CONTROL_FLOW |\
            T_MISC_SYM |\
            T_BRACKETS |\
            T_MATH_OPS |\
            T_LOG_OPS |\
            T_COMP_OPS |\
            T_PIPES_BASIC |\
            T_PIPES_STREAM |\
            T_PIPES_OTHER |\
            T_TYPES_PRIMITIVE |\
            T_TYPES_COMPLEX


# Extracted
T_TERM_OPS = {
    '*': Token('*', 'T_ASTERISK', OpType.BINARY),
    '/': Token('/', 'T_SLASH', OpType.BINARY),
    '%': Token('%', 'T_PERCENT', OpType.BINARY),
    '**': Token('**', 'T_ASTERISK2', OpType.BINARY),
}


class NumType(Enum):
    INVALID=0
    FLOAT=1
    INT=2

def is_number(num:str) -> NumType:
    floatCast = False
    try:
        float(num)
        floatCast = True
    except ValueError:
        return NumType.INVALID
    
    # Check is float and not int
    if floatCast and num.count('.') > 0:
        return NumType.FLOAT
    return NumType.INT

def add_buff(buff:str, tokset:List[Token], type:str='T_UNKNOWN'):
    if len(buff) > 0:
        # print(f'add buff: `{buff}`', end='\t\t')
        
        if TOKENS.get(buff):
            tokset.append(TOKENS.get(buff))
        else:
            tokset.append(Token(buff, type))

def gen_tokset(lines:List[str], debug:bool=False) -> List[Token]:
    tokset = []

    for lineNum, line in enumerate(lines):
        buff = ''

        # Process each line
        i = 0
        while i <= len(line):
            c1 = line[i:i+1]
            c2 = line[i:i+2]

            # Avoid case for final char in line
            if c1 == c2:
                c2 = ''

            if debug:
                print(f'c1: `{c1}`\tc2: `{c2}`\tbuff: `{buff}`', end='\t')

            # Match 2-char token
            if TOKENS.get(c2) and not c2.isalpha():
                add_buff(buff, tokset)
                tokset.append(TOKENS.get(c2))
                i += 1  # skip second char
                buff = ''

                if debug:
                    print(f'add c2: `{c2}`')

            # Match 1-char token
            elif TOKENS.get(c1):
                add_buff(buff, tokset)
                tokset.append(TOKENS.get(c1))
                buff = ''
                
                if debug:
                    print(f'add c1: `{c1}`')

            # Match buffer
            elif TOKENS.get(buff) and c1 == ' ':
                tokset.append(TOKENS.get(buff))
                buff = ''

                if debug:
                    print(f'add buff: `{buff}`')

            # Otherwise increase buffer
            else:
                if debug:
                    print()
                buff += c1

            # Progress scan
            i += 1

        # Append final buffer each line
        add_buff(buff, tokset)

        # Add linebreaks to non-empty lines (don't add to last line)
        if len(line) > 0 and lineNum != len(lines) - 1:
            tokset.append(Token('\n', 'T_LINEBREAK'))
    
    # Append EOF at end
    tokset.append(Token('{END}', 'T_EOF'))

    return tokset

def refine_tokset(tokset:List[Token], debug:bool) -> List[Token]:
    refined:List[Token] = []
    
    i = 0
    while i < len(tokset):
        
        # Skip comments
        if tokset[i].ttype == 'T_HASH':
            if debug:
                print('Refine comment')
                
            while True:
                if tokset[i].ttype in ['T_LINEBREAK', 'T_EOF']:
                    break
                i += 1
        
        # Handle string literals
        if tokset[i].ttype == 'T_QUOTE':
            if debug:
                print('Refine str lit')
            
            strlit = ''
            i += 1  # skip first quote
            while tokset[i].ttype != 'T_QUOTE':
                strlit += tokset[i].raw
                i += 1
            refined.append(Token(strlit, 'T_STR_LIT'))
        
        # Handle numerical literals
        elif len(tokset[i].raw) > 0 and tokset[i].raw[0].isdecimal():
            if debug:
                print('Refine num lit')
            
            numlit = ''
            while True:
                if tokset[i].raw.isdigit():
                    numlit += tokset[i].raw
                elif tokset[i].ttype == 'T_DOT':
                    numlit += tokset[i].raw
                else:
                    i -= 2
                    break
                i += 1

            match is_number(numlit):
                case NumType.INT:
                    refined.append(Token(numlit, 'T_INT_LIT'))
                case NumType.FLOAT:
                    refined.append(Token(numlit, 'T_FLOAT_LIT'))
                case _:
                    refined.append(Token(numlit, 'E_INVALID_NUM'))

            # Don't erase EOF or newlines
            if i != len(tokset) - 2:
                i += 1

        # Skip spaces
        elif tokset[i].ttype != 'T_SPACE':
            if tokset[i].ttype == 'T_UNKNOWN':
                refined.append(Token(tokset[i].raw, 'T_ID'))
            else:
                refined.append(tokset[i])

        # Increment token
        i += 1
    
    return refined

def print_refined(refined:List[Token], raw:bool=True, showLineBreak:bool=False):
    for t in refined:
        if raw:
            if t.ttype == 'T_LINEBREAK':
                print()
            else:
                print(t.raw, end=' ')
        else:
            if t.ttype == 'T_LINEBREAK':
                if showLineBreak:
                    print(t.ttype, end='\n')
                else:
                    print()
            else:
                print(t.ttype, end=' ')

def gen_refined(debug:bool=False) -> List[Token]:
    
    path = r'../test/files/test3.pb'
    with open(path) as f:
        lines = f.read().splitlines()
        tokset: List[Token] = gen_tokset(lines, debug)

        if debug:
            print('\nTokens:')
            pprint(tokset)  
            print()
            print('='*60)

        # Refine tokens
        refined = refine_tokset(tokset, debug)

        if debug:
            print('Refined')
            pprint(refined)
            print('='*60)
            print()

        return refined
