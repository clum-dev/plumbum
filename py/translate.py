from parser import *
import sys


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
            

        


def main():
    f = sys.argv[1]
    p = Parser(f)
    p.tree.printer()
    print('-'*50)


if __name__ == '__main__':
    main()