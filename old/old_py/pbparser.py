from typing import List
from dataclasses import dataclass
from pprint import pprint
from enum import Enum

from pblexer import *

class Tree:
    tok: Token
    leaves: List

    def __init__(self, tok:Token, leaves:List=None) -> None:
        self.tok = tok
        if leaves == None:
            self.leaves = []
        else:
            self.leaves = leaves
    
    def add(self, leaves):
        self.leaves.append(leaves)

    def printer(self, indent=0):
        print('\t'*indent, self.tok, sep='')
        for l in self.leaves:
            if isinstance(l, Tree):
                l.printer(indent + 1)
            elif isinstance(l, Token):
                print('\t'*(indent+1), l, sep='')
        
    def __repr__(self) -> str:
        return '{' + f'{self.tok}: {str(self.leaves)}' + '}'


class Parse:
    tokStream: List[Token]
    index: int
    tree: Tree
    debug: bool

    def __init__(self, tokset: List[Token], debug=False) -> None:
        self.tokStream = tokset
        self.index = 0
        self.tree = Tree(Token('__PROGRAM', 'INTERNAL_PROGRAM'))
        self.debug = debug
    
    def printer(self):
        if isinstance(self.tree, Tree):
            self.tree.printer()
        else:
            print(self.tree)

    def match(self, ttype:str) -> Token:
        curr = self.get_curr()
        if curr.ttype == ttype:
            if self.debug:
                print(f'\t matched {ttype}')
            self.next()
            return curr
        else:
            raise SyntaxError(f"Parse: Could not match `{ttype}` (got `{curr.ttype}`)")
    
    def is_match(self, ttype:str) -> bool:
        # if ttype not in [t.ttype for t in TOKENS.values()]:
        #     raise NameError(f"Parse: is_match: Invalid name lookup: {ttype}")
        
        return self.get_curr().ttype == ttype
    
    def is_match_multi(self, ttypes:List[str]) -> bool:
        return self.get_curr().ttype in ttypes

    def get_curr(self) -> Token:
        return self.tokStream[self.index] if self.index < len(self.tokStream) else Token('__OOB', 'T_OOB')

    def next(self):
        self.index += 1

    def begin(self):

        result = []

        while not self.is_match_multi(["T_EOF", "T_OOB"]):
            temp = self.top_level()
            result.append(temp)

        if not (self.is_match("T_EOF") or self.is_match("T_OOB")):
            print("\n---DONE---")
            # raise SyntaxError(f"Parse: Unexpected token {self.get_curr().ttype}")

        self.tree = Tree(Token("__TOP_LEVEL", "T_TOP_LEVEL"), result)
    
    def top_level(self):
        if self.debug:
            print('[PARSE]\t top_level')

        while self.is_match("T_LINEBREAK"):
            self.match("T_LINEBREAK")
        
        result = None
        if self.is_match("T_FUNC"):
            result = self.func()
        elif self.is_match("T_STRUCT"):
            result = self.struct()
        elif self.is_match("T_ENUM"):
            result = self.enum()
        elif self.is_match("T_CONST"):
            result = self.const()
        elif self.is_match("T_USE"):
            result = self.use()
        else:
            raise SyntaxError(f"Parse: Top Level: Expected top level keyword (got {self.get_curr().ttype})")

        return result

    def func(self):
        if self.debug:
            print('[PARSE]\t func')

        self.match("T_FUNC")
        name = self.match("T_ID")

        # Method
        if self.is_match("T_COLON2"):
            op = self.match("T_COLON2")
            method = self.match("T_ID")
            name = Tree(op, [name, method])
        
        # Pipe
        op = None
        if self.is_match_multi(["T_PIPE", "T_PIPEFUNNEL", "T_PIPEPAIR", "T_PIPEDIST"]):
            if self.is_match("T_PIPE"):
                op = self.match("T_PIPE")
            elif self.is_match("T_PIPEFUNNEL"):
                op = self.match("T_PIPEFUNNEL")
            elif self.is_match("T_PIPEPAIR"):
                op = self.match("T_PIPEPAIR")
            elif self.is_match("T_PIPEDIST"):
                op = self.match("T_PIPEDIST")

        # Params
        params = None
        if not self.is_match("T_LBRACE"):
            params = self.param_list()
            params = Tree(op, [params])

        rettype = None
        if self.is_match("T_RARROW"):
            self.match("T_RARROW")
            rettype = self.type_name()
    
        result = self.block()
        
        return Tree(Token("__FUNC", "T_FUNC"), [name, params, rettype, result])

    def struct(self):
        if self.debug:
            print('[PARSE]\t struct')

        self.match("T_STRUCT")
        name = self.match("T_ID")

        self.match("T_LBRACE")
        while self.is_match("T_LINEBREAK"):
            self.match("T_LINEBREAK")
        
        result = []
        while not self.is_match("T_RBRACE"):

            result.append(self.param_list())

            while self.is_match("T_LINEBREAK"):
                self.match("T_LINEBREAK")

        self.match("T_RBRACE")
        
        return Tree(Token("__STRUCT", "T_STRUCT"), result)

    def enum(self):
        if self.debug:
            print('[PARSE]\t enum')

        self.match("T_ENUM")
        name = self.match("T_ID")

        self.match("T_LBRACE")
        while self.is_match("T_LINEBREAK"):
            self.match("T_LINEBREAK")
        
        result = []
        while not self.is_match("T_RBRACE"):
            left = self.match("T_ID")
            if self.is_match("T_COMMA"):
                self.match("T_COMMA")
            elif self.is_match("T_LINEBREAK"):
                self.match("T_LINEBREAK")
            elif self.is_match("T_RBRACE"):
                result.append(left)
                break
            else:
                raise SyntaxError(f"Parse: Enum: Expected comma or linebreak (got {self.get_curr().ttype})")

            result.append(left)

            while self.is_match("T_LINEBREAK"):
                self.match("T_LINEBREAK")

        self.match("T_RBRACE")

        return Tree(Token("__ENUM", "T_ENUM"), result)

    def const(self):
        if self.debug:
            print('[PARSE]\t const')

        self.match("T_CONST")
        # All output vars will be set as constant
        result = self.block()
        return Tree(Token("__CONST", "T_CONST"), [result])

    def use(self):
        if self.debug:
            print('[PARSE]\t use')
        
        self.match("T_USE")

        self.match("T_LBRACE")
        while self.is_match("T_LINEBREAK"):
            self.match("T_LINEBREAK")
        
        result = []
        while not self.is_match("T_RBRACE"):
            left = self.match("T_ID")
            if self.is_match("T_PIPE"):
                op = self.match("T_PIPE")
                right = self.match("T_ID")
                left = Tree(op, [left, right])
            
            result.append(left)

            while self.is_match("T_LINEBREAK"):
                self.match("T_LINEBREAK")

        self.match("T_RBRACE")
        
        return Tree(Token("__USE", "T_USE"), result)

    def block(self):
        if self.debug:
            print('[PARSE]\t block')

        self.match("T_LBRACE")
        while self.is_match("T_LINEBREAK"):
            self.match("T_LINEBREAK")
        
        result = []
        while not self.is_match("T_RBRACE"):
            if self.is_match("T_IF"):
                result.append(self.if_else_stmt())
            elif self.is_match("T_WHILE"):
                result.append(self.while_stmt())           
            else:
                result.append(self.pipe_list())

            while self.is_match("T_LINEBREAK"):
                self.match("T_LINEBREAK")

        self.match("T_RBRACE")
        
        return Tree(Token("__BLOCK", "T_BLOCK"), result)

    def if_else_stmt(self):
        if self.debug:
            print('[PARSE]\t if_else_stmt')
            
        result = []

        self.match("T_IF")
        cond = self.pipe()
        if isinstance(cond, Tree) and cond.tok in ["T_EOF", "T_OOB"] or isinstance(cond, Token) and cond.ttype in ["T_EOF", "T_OOB"]:
            raise SyntaxError("Parse: If: Expected condition")
        block = self.block()
        
        result.append(Tree(Token("__IF", "T_IF"), [cond, block]))
        print(result)

        while self.is_match("T_ELSE") or self.is_match("T_LINEBREAK"):
            while self.is_match("T_LINEBREAK"):
                self.match("T_LINEBREAK")
            
            self.match("T_ELSE")
            if self.is_match("T_IF"):
                self.match("T_IF")
                cond = self.pipe()
                block = self.block()
                result.append(Tree(Token("__ELSE_IF", "T_ELSE_IF"), [cond, block]))
            else:
                block = self.block()
                result.append(Tree(Token("__ELSE", "T_ELSE"), [block]))
                break
        
        return Tree(Token("__IF_ELSE_STMT", "T_IF_ELSE_STMT"), result)
    
    def while_stmt(self):
        if self.debug:
            print('[PARSE]\t while_stmt')
        
        self.match("T_WHILE")
        cond = self.pipe()
        if isinstance(cond, Tree) and cond.tok in ["T_EOF", "T_OOB"] or isinstance(cond, Token) and cond.ttype in ["T_EOF", "T_OOB"]:
            raise SyntaxError("Parse: While: Expected condition")
        block = self.block()

        return Tree(Token("__WHILE_STMT", "T_WHILE_STMT"), [cond, block])

    # TODO 14/02/2024 do for loop stmt

    def pipe_list(self):
        if self.debug:
            print('[PARSE]\t pipe_list')

        # Get LHS list        
        left = [self.pipe()]
        while self.is_match("T_COMMA"):
            self.match("T_COMMA")
            left.append(self.pipe())

        # Get RHS if present
        op = None
        right = None

        if self.is_match_multi(["T_PIPEFUNNEL", "T_PIPEPAIR", "T_PIPEDIST"]):
            if self.is_match("T_PIPEFUNNEL"):
                op = self.match("T_PIPEFUNNEL")
            elif self.is_match("T_PIPEPAIR"):
                op = self.match("T_PIPEPAIR")
            elif self.is_match("T_PIPEDIST"):
                op = self.match("T_PIPEDIST")

            right = self.pipe_list()
        
        # Form lists
        if len(left) > 1:
            left = Tree(T_TYPES_COMPLEX.get("List"), left)
        else:
            left = left[0]

        if op != None:
            left = Tree(op, [left, right])
            # TODO 11/02/2024 length check for pipe list operators???
            # e.g. len(lhs) == len(rhs) for pipe pair
            
        return left
                   
    def pipe(self):
        if self.debug:
            print('[PARSE]\t pipe')

        result = self.stream()
        op = None
        
        while self.is_match_multi(["T_PIPE", "T_PIPESUM"]) or self.is_match_multi([t.ttype for t in T_PIPES_STREAM.values()]):
            if self.is_match("T_PIPE"):
                op = self.match("T_PIPE")
            elif self.is_match("T_PIPESUM"):
                op = self.match("T_PIPESUM")
            else:
                raise SyntaxError(f"Parse: Pipe: Expected pipe symbol (got {self.get_curr().ttype})")

            right = self.stream()
            result = Tree(op, [result, right])
        
        return result
    
    def stream(self):
        if self.debug:
            print('[PARSE]\t stream')

        result = self.rel_cond()

        # Ternary
        if self.is_match("T_QUESTION"):
            if self.debug:
                print('[PARSE]\t ternary')
            op = self.match("T_QUESTION")
            true = self.pipe()
            self.match("T_COLONRARROW")
            false = self.pipe()
            result = Tree(Token("__TERNARY", "T_TERNARY"), [result, true, false])
        
        while self.is_match_multi([t.ttype for t in T_PIPES_STREAM.values()]):
            op = self.stream_pipe_op()
            lam = self.lambda_expr()
        
            result = (Tree(op, [result, lam]))
        
        return result

    def stream_pipe_op(self):
        if self.debug:
            print('[PARSE]\t stream_pipe_op')

        if self.is_match("T_PIPEMAP"):
            return self.match("T_PIPEMAP")
        elif self.is_match("T_PIPEFILTER"):
            return self.match("T_PIPEFILTER")
        elif self.is_match("T_PIPEREDUCE"):
            return self.match("T_PIPEREDUCE")
        elif self.is_match("T_PIPESCAN"):
            return self.match("T_PIPESCAN")
        else:
            raise SyntaxError(f"Parse: Stream_Pipe_Op: Expected stream pipe operator (got {self.get_curr().ttype})")

    def other_pipe_op(self):
        if self.debug:
            print('[PARSE]\t other_pipe_op')

        if self.is_match("T_PIPEREGEX"):
            return self.match("T_PIPEREGEX")
        else:
            raise SyntaxError(f"Parse: Other_Pipe_Op: Expected pipe operator (got {self.get_curr().ttype})")

    def lambda_expr(self):
        if self.debug:
            print('[PARSE]\t lambda_expr')
        
        left = self.param_list()
        lam = self.match("T_RARROW")
        right = self.block()

        if lam == None:
            raise SyntaxError("Parse: Lambda_Expr: Invalid lambda format (expected <capture> -> <expression>)")
        
        return Tree(lam, [left, Tree(Token('__LAMBDA_BODY', 'T_LAMBDA_BODY'), [right])])

    def rel_cond(self):
        if self.debug:
            print('[PARSE]\t rel_cond')
        
        result = self.log()
        if self.get_curr().raw in T_COMP_OPS.keys():
            op = self.rel_op()
            right = self.rel_cond()
            result = Tree(op, [result, right])

        return result

    def rel_op(self):
        if self.debug:
            print('[PARSE]\t rel_op')

        if self.is_match("T_EQUAL2"):
            return self.match("T_EQUAL2")
        elif self.is_match("T_BANGEQUAL"):
            return self.match("T_BANGEQUAL")
        elif self.is_match("T_LANGLEEQUAL"):
            return self.match("T_LANGLEEQUAL")
        elif self.is_match("T_RANGLEEQUAL"):
            return self.match("T_RANGLEEQUAL")
        elif self.is_match("T_LANGLE"):
            return self.match("T_LANGLE")
        elif self.is_match("T_RANGLE"):
            return self.match("T_RANGLE")
        else:
            raise SyntaxError(f"Parse: Rel_Op: Expected comparator symbol (got {self.get_curr().ttype})")      

    def log(self):
        if self.debug:
            print('[PARSE]\t log')

        negated = None
        if self.is_match("T_NOT"):
            negated = self.match("T_NOT")
        
        result = self.expr()
        if negated != None:
            result = Tree(negated, [result])

        while self.is_match_multi([t.ttype for t in T_LOG_OPS.values()]):
            op = self.log_op()
            right = self.log()
            result = Tree(op, [result, right])
        
        return result

    def log_op(self):
        if self.debug:
            print('[PARSE]\t log_op')

        if self.is_match("T_OR"):
            return self.match("T_OR")
        elif self.is_match("T_AND"):
            return self.match("T_AND")
        else:
            raise SyntaxError(f"Parse: Log_Op: Expected `and` or `or` (got {self.get_curr().ttype})")

    def expr(self):
        if self.debug:
            print('[PARSE]\t expr')

        result = self.term()
        
        while self.is_match("T_PLUS") or self.is_match("T_MINUS"):
            if self.is_match("T_PLUS"):
                op = self.get_curr()
                self.match("T_PLUS")
            elif self.is_match("T_MINUS"):
                op = self.get_curr()
                self.match("T_PLUS")
            else:
                raise SyntaxError(f"Parse: Expr: Expected `+` or `-` (got {self.get_curr().ttype})")

            right = self.term()
            result = Tree(op, [result, right])
    
        return result

    def term(self):
        if self.debug:
            print('[PARSE]\t term')

        result = self.prefix()
        op = None

        while self.is_match_multi([t.ttype for t in T_TERM_OPS.values()]):
            if self.is_match("T_ASTERISK2"):
                op = self.get_curr()
                self.match("T_ASTERISK2")
            elif self.is_match("T_PERCENT"):
                op = self.get_curr()
                self.match("T_PERCENT")
            elif self.is_match("T_ASTERISK"):
                op = self.get_curr()
                self.match("T_ASTERISK")
            elif self.is_match("T_SLASH"):
                op = self.get_curr()
                self.match("T_SLASH")
            else:
                raise SyntaxError(f"Parse: Term: Expected `*` or `/` (got {self.get_curr().ttype})")

            right = self.prefix()
            result = Tree(op, [result, right])

        return result
    
    def prefix(self):
        if self.debug:
            print('[PARSE]\t prefix')

        # Unary prefix
        prefix = None
        if self.is_match("T_PLUS"):
            prefix = self.get_curr()
            self.match("T_PLUS")
        elif self.is_match("T_MINUS"):
            prefix = self.get_curr()
            self.match("T_MINUS")
        elif self.is_match("T_AT"):
            prefix = self.match("T_AT")

        result = self.factor()
        
        # Unary negation
        if prefix != None and prefix.ttype != "T_PLUS":
            result = Tree(prefix, [result])

        return result

    def factor(self):
        if self.debug:
            print('[PARSE]\t factor')
        
        result = None

        # Match parentheses
        if self.is_match("T_LPAREN"):
            self.match("T_LPAREN")
            result = self.pipe_list()
            self.match("T_RPAREN")
        else:
            result = self.suffix()
        
        return result  

    def suffix(self):
        if self.debug:
            print('[PARSE]\t suffix')

        suffix = None
        result = self.cast()

        # Increment or decrement suffix
        if self.is_match("T_PLUS2"):
            suffix = self.match("T_PLUS2")
        elif self.is_match("T_MINUS2"):
            suffix = self.match("T_MINUS2")
        
        if suffix != None:
            result = Tree(suffix, [result])

        return result

    def cast(self):
        if self.debug:
            print('[PARSE]\t cast')
        
        result = self.data_complex()
        
        if self.is_match("T_PIPE_CAST"):
            op = self.match("T_PIPE_CAST")
            cast = self.type_name()
            result = Tree(Token("__CAST", "T_CAST"), [result, cast])
        
        return result
    
    def data_complex(self):
        if self.debug:
            print('[PARSE]\t data_complex')
        
        result = self.data_simple()
        op = None

        # Range
        if self.is_match("T_DOT2"):
            op = self.match("T_DOT2")
            right = self.data_complex()
            result = Tree(op, [result, right])

        # Method
        elif self.is_match("T_DOT"):
            op = self.match("T_DOT")
            right = self.match("T_ID")
            result = Tree(op, [result, right])

        # Index
        elif self.is_match("T_LBRACKET"):
            op = self.match("T_LBRACKET")
            right = self.pipe()
            self.match("T_RBRACKET")
            result = Tree(Token("__INDEX", "T_INDEX"), [result, right])
       
        return result

    def data_simple(self):
        if self.debug:
            print('[PARSE]\t data_simple')

        result = None

        if self.is_match_multi(['T_INT_LIT', 'T_FLOAT_LIT', 'T_STR_LIT']):
            result = self.literal()
        
        elif self.is_match("T_ID"):
            result = self.match("T_ID")

        elif self.is_match("T_RETURN"):
            result = self.match("T_RETURN")
        elif self.is_match("T_BREAK"):
            result = self.match("T_BREAK")
        elif self.is_match("T_CONTINUE"):
            result = self.match("T_CONTINUE")
        
        elif self.is_match("T_EOF"):
            result = self.match("T_EOF")
        elif self.is_match("T_OOB"):
            result = self.match("T_OOB")

        else:
            raise SyntaxError(f"Parse: Data_Value: Expected data value (got `{self.get_curr().ttype}`)")
        
        return result

    def literal(self):
        if self.debug:
            print('[PARSE]\t literal')
        
        if self.is_match("T_INT_LIT"):
            result = self.match("T_INT_LIT")
        elif self.is_match("T_FLOAT_LIT"):
            result = self.match("T_FLOAT_LIT")
        elif self.is_match("T_STR_LIT"):
            result = self.match("T_STR_LIT")

        return result

    def param_list(self):
        if self.debug:
            print('[PARSE]\t param_list')
        
        result = [self.param()]
        
        while self.is_match("T_COMMA"):
            self.match("T_COMMA")
            result.append(self.param())

        if len(result) == 1:
            return result[0]
        return Tree(Token('__PARAM_LIST', 'T_PARAM_LIST'), result)

    def param(self):
        if self.debug:
            print('[PARSE]\t param')

        result = None
        if self.is_match("T_ID"):
            result = [self.match("T_ID")]
        else:
            raise SyntaxError(f"Parse: Param: Expected identifier (got {self.get_curr().ttype})")

        td = self.type_def()

        if td != None:
            result.append(td)

        return Tree(Token("__PARAM", "T_PARAM"), result)

    def type_def(self):
        if self.debug:
            print('[PARSE]\t type_def')
        
        name = None

        # If colon found, then must match type name
        if self.is_match("T_COLON"):
            self.match("T_COLON")
            name = self.type_name()
            if name == None:
               raise SyntaxError(f"Parse: Type_Def: Invalid type definition name: {self.get_curr().raw}")

        return name
    
    def type_name(self):
        if self.debug:
            print('[PARSE]\t type_name')
        
        isPrimitive = True
        isCustom = False
        name = None
        inner = None

        # Primitive types
        if self.is_match("T_TYPE_ANY"):
            name = self.match("T_TYPE_ANY")
        elif self.is_match("T_TYPE_INT"):
            name = self.match("T_TYPE_INT")
        elif self.is_match("T_TYPE_FLOAT"):
            name = self.match("T_TYPE_FLOAT")
        elif self.is_match("T_TYPE_BOOL"):
            name = self.match("T_TYPE_BOOL")
        elif self.is_match("T_TYPE_NULL"):
            name = self.match("T_TYPE_NULL")

        # Complex types
        elif self.is_match("T_TYPE_STR"):
            name = self.match("T_TYPE_STR")
            isPrimitive = False
            
        elif self.is_match("T_TYPE_LIST"):
            name = self.match("T_TYPE_LIST")
            isPrimitive = False

            if self.is_match("T_LANGLE"):
                self.match("T_LANGLE")
                inner = self.type_name()
                self.match("T_RANGLE")

        elif self.is_match("T_TYPE_DICT"):
            name = self.match("T_TYPE_DICT")
            isPrimitive = False

            if self.is_match("T_LANGLE"):
                self.match("T_LANGLE")
                inner = self.type_name()
                self.match("T_RANGLE")
       
        # Custom type (identifier)
        elif self.is_match("T_ID"):
            name = self.match("T_ID")
            isPrimitive = False
            isCustom = True

        if name == None:
            raise SyntaxError(f"Parse: Type_Name: Invalid type name specifier")
        if inner == None:
            name = [name]
        else:
            name = [name, inner]
        
        if not isPrimitive:
            if not isCustom:
                name = Tree(Token('__TYPE_COMPLEX', 'T_TYPE_COMPLEX'), name)
            else:
                name = Tree(Token('__TYPE_USER', 'T_TYPE_USER'), name)
        else:
            name = Tree(Token('__TYPE_PRIM', 'T_TYPE_PRIM'), name)

        return name



