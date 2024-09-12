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
        if self.parent is not None:
            self.parent.data.append(self)
        self.data = []
        self.config = Config()

    def __str__(self) -> str:
        return f'{self.idStr}({self.level})'

    def printer(self) -> None:
        print('\t'*self.level, self, sep='')
        for item in self.data:
            print('\t'*self.level, item, sep='')
            
    def add_data(self, data:object) -> None:
        self.data.append(data)


class Data:
    
    tree:Tree
    name:str            # for lookup
    value:object        # for output
    scope:Scope

    isConst:bool
    isCallable:bool
    isIterable:bool
    isIndexable:bool

    def __init__(self, t:Tree, scope:Scope) -> None:
        self.tree = t
        self.scope = scope
        self.toktype = self.tree.tok.t

        self.isConst = False
        self.isCallable = False
        self.isIterable = False
        self.isIndexable = False


class DataType:

    tree:Tree
    name:str

    isCustom:bool
    default:object
    
    def __init__(self, t:Tree) -> None:
        self.tree = t
        self.isCustom = True if t.tok.t == TokType.TYPE_DEF else False
        self.name = t.tok.t.lookup()
        self.default = None

        match t.tok.t:
            case TokType.TYPE_INT:
                self.default = 0
            case TokType.TYPE_FLOAT:
                self.default = 0.0
            case TokType.TYPE_STRING:
                self.default = ''
            case TokType.TYPE_BOOL:
                self.default = False
            case TokType.TYPE_NULL, TokType.TYPE_DEF, TokType.TYPE_ANY:
                self.default = None
            case TokType.TYPE_LIST:
                self.default = list()
            case TokType.TYPE_DICT:
                self.default = dict()
        

class Param(Data):
    
    dType:DataType
    default:Data

    def __init__(self, t:Tree, parentScope:Scope) -> None:
        super().__init__(t, parentScope)
        # TODO
        

    def __str__(self) -> str:
        return f'{self.name}:{self.dType}({self.default})'

    def __repr__(self) -> str:
        return self.__str__()


class Var(Data):

    def __init__(self, t:Tree, scope:Scope) -> None:
        super().__init__(t, scope)
        # TODO



class Func(Data):
    
    localScope:Scope
    params:list

    def __init__(self, t:Tree, scope:Scope) -> None:
        super().__init__(t, scope)
        self.isCallable = True

        # Set name and local scope
        self.name = t.leaves[0].leaves[0]
        self.localScope = Scope(self.name, scope.level+1, scope, t)

        # Set params
        params = t.leaves[1]
        self.params = []
        if params is not None:
            assert params.tok.t == TokType.PARAM_SEQ
            for p in self.params:
                param = Param(p, self.localScope)
                self.params.append(param)           # param for calling

                # TODO add param as var to local scope

                self.localScope.add_data(param)     # local for reference
        
    def __str__(self) -> str:
        return f'{self.scope}::{self.name}'

def get_data_from_tok(t:Tree, scope:Scope) -> Data:
    match t.tok.t:
        case TokType.FUNC:
            scope.add_data(Func(t, scope))

        case _:
            pass


def translate(tree:Tree, baseScope:Scope):
    for leaf in tree.leaves:
        get_data_from_tok(leaf, baseScope)
        

def main():
    
    f = sys.argv[1]
    p = Parser(f)
    p.tree.printer()
    print('-'*50)

    progScope = Scope('program', 0, None, p.tree)
    translate(p.tree, progScope)


if __name__ == '__main__':
    main()