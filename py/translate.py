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