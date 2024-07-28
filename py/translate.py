from parser import *
import sys

class Scope:
    
    tree:Tree
    parent:any
    children:list
    level:int
    localdata:dict
    
    def __init__(self, t:Tree, parent, level:int) -> None:
        self.tree = t
        self.parent = parent
        self.level = level

        self.children = []
        self.localdata = {}

class Data:
    
    tree:Tree
    toktype:TokType
    values:any
    scope:any

    isConst:bool
    isCallable:bool
    isIterable:bool
    isIndexable:bool

    def __init__(self, t:Tree) -> None:
        self.tree = t
        self.toktype = self.tree.tok.t

        match self.toktype:
            case TokType.LIT_INT:
                self.values = int(self.tree.leaves[0])
            case TokType.LIT_FLOAT:
                self.values = float(self.tree.leaves[0])
            case TokType.LIT_TRUE:
                self.values = bool(self.tree.leaves[0])
            


class Translator:

    t:Tree

    def __init__(self, t:Tree) -> None:
        self.t = t


def main():
    f = sys.argv[1]
    p = Parser(f)

    p.tree.printer()

if __name__ == '__main__':
    main()