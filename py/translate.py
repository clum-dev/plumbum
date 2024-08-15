from parser import *
import sys


class Config:
    strict:bool
    
    def __init__(self) -> None:
        self.strict = False


class Scope:

    idStr:str
    level:int
    tree:Tree

    parent:object
    data:list
    config:Config

    def __init__(self, idStr:str, level:int, parent:object, tree:Tree) -> None:
        self.idStr, self.level, self.tree = idStr, level, tree
        self.parent = parent
        self.data = []
        self.config = Config()

    def __str__(self) -> str:
        return f'{self.idStr}({self.level})'
    
    def printer(self, indent:int=1) -> None:
        print('\t'*(indent-1), self, sep='')
        for d in self.data:
            print('\t'*indent, d, sep='')
            if isinstance(d, Func):
                d.funcScope.printer(indent+1)

    def add_data(self, data:object) -> None:
        self.data.append(data)

    
class Data:
    
    tree:Tree
    toktype:TokType

    name:str
    value:any
    parentScope:Scope

    isConst:bool
    isCallable:bool
    isIterable:bool
    isIndexable:bool

    def __init__(self, t:Tree, parentScope:Scope) -> None:
        self.tree = t
        self.parentScope = parentScope
        self.toktype = self.tree.tok.t

        self.parentScope.add_data(self)     # Add any new data instance to parent scope


class DataType(Data):

    innerType:object
    isUserDefined:bool

    def __init__(self, t:Tree, parentScope:Scope) -> None:
        super().__init__(t, parentScope)
        self.outerType = None
        self.innerType = None
        self.isUserDefined = False

        # User defined type
        if t.tok.t == TokType.TYPE_DEF:
            self.isUserDefined = True
            self.outerType = t.leaves[0].leaves[0]
        
        # Standard type
        else:
            if len(t.leaves) >= 1 and t.leaves[0].tok.t.has_attr(TokAttr.TYPE):
                self.innerType = DataType(t.leaves[0], parentScope)
            self.name = t.tok.t

    def __str__(self) -> str:
        if self.innerType is not None:
            return f'{self.name.lookup()}<{self.innerType}>'
        else:
            return f'{self.name.lookup()}'


class Param(Data):
    
    dType:DataType
    default:Data

    def __init__(self, t:Tree, parentScope:Scope) -> None:
        super().__init__(t, parentScope)
        self.default = None
        self.dType = DataType(Tree(Tok(TokType.TYPE_ANY, t.tok.line, t.tok.col)), parentScope)
        self.name = None

        # Convert any untyped param to any type
        if t.tok.t == TokType.ID:
            self.name = t.leaves[0]
        else:
            self.name = t.leaves[0].leaves[0]
            if t.leaves[1] is not None:
                self.dType = DataType(t.leaves[1], parentScope)

        # Store default value
        if len(t.leaves) > 2 and t.leaves[2] is not None:
            if t.leaves[2].tok.t.has_attr(TokAttr.LITERAL):
                lit = Literal(t.leaves[2], parentScope)
                self.default = lit.value
            else:
                raise NotImplementedError('Non literal default')
            
            # Check datatype 
            if parentScope.config.strict and self.dType.name != lit.name:
                raise Exception('Invalid type for inference')
                # raise NotImplementedError('Param strict type check')
            
            self.dType.name = lit.name

    def __str__(self) -> str:
        return f'{self.name}:{self.dType}({self.default})'

    def __repr__(self) -> str:
        return self.__str__()


class Literal(Data):
    
    def __init__(self, t:Tree, parentScope:Scope) -> None:
        super().__init__(t, parentScope)
        self.name = TokType.TYPE_ANY

        match t.tok.t:
            case TokType.LIT_INT:
                self.value = int(t.leaves[0])
                self.name = TokType.TYPE_INT
            case TokType.LIT_FLOAT:
                self.value = float(t.leaves[0])
                self.name = TokType.TYPE_FLOAT
            case TokType.LIT_STRING:
                raise NotImplementedError('String literal -> TODO evaluate strings')
            case TokType.LIT_TRUE:
                self.value = bool(t.leaves[0])
                self.name = TokType.TYPE_BOOL
            case TokType.LIT_FALSE:
                self.value = bool(t.leaves[0])
                self.name = TokType.TYPE_BOOL

            case _:
                self.value = t.leaves[0]
                self.name = TokType.TYPE_ANY
    
    def __str__(self) -> str:
        return f'{str(self.value)}({self.name.lookup()})'


class Func(Data):
    class ParamType(Enum):
        NONE=0
        PAIR=1
        FUNNEL=2
        DIST=3

        def __str__(self) -> str:
            return self.name

    funcScope:Scope
    pType:ParamType
    rType:DataType
    params:list

    def __init__(self, t:Tree, parentScope:Scope) -> None:
        super().__init__(t, parentScope)
        
        # Set name and local func scope
        self.name = t.leaves[0].leaves[0]
        self.funcScope = Scope(self.name, parentScope.level + 1, parentScope, t)

        # Set passed params (seq or single)
        passed = t.leaves[1]
        self.params = []
        if passed is not None:
            if passed.tok.t == TokType.PARAM_SEQ:
                for p in passed.leaves:
                    self.params.append(Param(p, self.funcScope))
            elif passed.tok.t in [TokType.PARAM, TokType.ID]:
                self.params.append(Param(passed, self.funcScope))
        
        # Set param store type
        if t.leaves[2] is not None:
            self.pType = {TokType.PIPE_PAIR:    Func.ParamType.PAIR,
                          TokType.PIPE_FUNNEL:  Func.ParamType.FUNNEL,
                          TokType.PIPE_DIST:    Func.ParamType.DIST}[t.leaves[2].t]
        else:
            self.pType = Func.ParamType.NONE
        
        # Set return datatype
        if t.leaves[3] is None:
            self.rType = DataType(Tree(Tok(TokType.TYPE_NULL, t.tok.line, t.tok.col)), self.funcScope)
        else:
            self.rType = DataType(t.leaves[3], self.funcScope)
               
    def __str__(self) -> str:
        return f'{self.parentScope}::func::{self.name}\t{self.pType}{self.params}->{self.rType}'

    def __repr__(self) -> str:
        return self.__str__()


class Struct(Data):

    structScope:Scope

    def __init__(self, t:Tree, parentScope:Scope) -> None:
        super().__init__(t, parentScope)
        
        # Set name and local struct scope
        self.name = t.leaves[0].leaves[0]
        self.structScope = Scope(self.name, parentScope.level + 1, parentScope, t)
        
            

def translate(tree:Tree, baseScope:Scope):
    toplevel = []
    
    for leaf in tree.leaves:
        if leaf.tok.t == TokType.FUNC:
            toplevel.append(Func(leaf, baseScope))

def main():
    
    f = sys.argv[1]
    p = Parser(f)
    p.tree.printer()
    print('-'*50)
    progScope = Scope('program', 0, None, p.tree)
    translate(p.tree, progScope)
    progScope.printer()


if __name__ == '__main__':
    main()