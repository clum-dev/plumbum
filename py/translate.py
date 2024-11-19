from parser import *
import sys
from typing_extensions import Self, Any

from enum import Enum, auto

class Inst:

    class InstType(Enum):
        RET   = auto()
        CALL  = auto()
        LOADV = auto()
        LOADN = auto()
        STORE = auto()
        BINOP = auto()
        UNOP  = auto()

        def __str__(self) -> str:
            return self.name

        def __repr__(self) -> str:
            return self.__str__()

    name:InstType
    arg:str

    def __init__(self, name:InstType, arg) -> None:
        assert isinstance(name, self.InstType)
        self.name = name
        self.arg = arg

    def __str__(self) -> str:
        out = str(self.name)
        if self.arg is not None:
            out += f' ({self.arg})'
        return out

    def __repr__(self) -> str:
        return self.__str__()

class Scope:

    tree:Tree
    name:str
    level:int
    parent:Self
    children:list[Self]

    _locals:dict
    insts:list
    stack:list

    input:Any               # Data passed into scope
    inputStoreMode:Any      # e.g. |> for funcs (if used) - default |:
    output:Any              # Data returned from scope

    def __init__(self, tree:Tree, level:int, parent:Self|None) -> None:

        self.tree = tree
        # self.name = None
        self.name = tree.tok.t
        self.level = level
        self.parent = parent
        self.children = []

        self._locals = {}
        self.insts = []
        self.stack = []

        self.input = None
        self.inputStoreMode = None
        self.output = None

        ind = self.level * ' '
        self.add_children_scope()
        print(f'{ind}{self.name} -> {self.parent.name if self.parent is not None else None}')
        print(f'{ind + " "}{self._locals}')

    def __str__(self) -> str:
        ind = '  ' * self.level
        return f'{ind}{self.name} -> {self.parent.name if self.parent is not None else None}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def add_children_scope(self):
        for l in self.tree.leaves:
            if isinstance(l, Tree):
                if l.tok.t in [TokType.FUNC, TokType.STRUCT, TokType.ENUM, TokType.BLOCK]:
                    self.children.append(Scope(l, self.level + 1, self))
                    
                    # TODO split this up and add func and struct data I/O
                    
                elif l.tok.t in [TokType.VAR, TokType.CONST]:
                    for d in l.leaves:
                        self.add_data(d)
                else:
                    self.add_data(l)

    def add_data(self, tree:Tree):

        if tree == None or tree.tok == None:
            return
        if tree.tok.t == TokType.PARAM:
            name = tree.leaves[0].leaves[0]
            dtype = tree.leaves[1]
            default = tree.leaves[2]

            self._locals[name] = None   # TODO change to data type

        elif tree.tok.t == TokType.PARAM_SEQ:
            for l in tree.leaves:
                self.add_data(l)

    def fetch_data(self, name:str):
        if name in self._locals.keys():
            return self._locals.get(name)

        if self.parent is None:
            raise RuntimeError(f'Object `{name}` not found')

        return self.parent.fetch_data(name)


def main():

    # if len(sys.argv) > 1:    
    # f = sys.argv[1]
    p = Parser('test3.pb')
    p.tree.printer()
    print('-'*50)

    c = Scope(p.tree, 0, None)
    

if __name__ == '__main__':
    main()