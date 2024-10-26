from parser import *
import sys

from enum import Enum

class TInst(Enum):
    LOAD = 0
    STORE = 1
    BINOP = 2
    UNOP = 3

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

class Inst:

    name:TInst
    arg:str

    def __init__(self, name:TInst, arg) -> None:
        assert isinstance(name, TInst)
        self.name = name
        self.arg = arg

    def __str__(self) -> str:
        out = str(self.name)
        if self.arg is not None:
            out += f' ({self.arg})'
        return out

    def __repr__(self) -> str:
        return self.__str__()



class Interp:

    stack:list
    instrs:list[Inst]
    pc:int

    def __init__(self, instrs:list[Inst]) -> None:
        self.stack = []
        self.instrs = instrs
        self.pc = 0

    def fetch(self) -> Inst|None:
        return self.instrs[self.pc] if self.pc < len(self.instrs) else None
    
    def exec(self):
        f = self.fetch()
        match f.name:
            case TInst.LOAD:
                self.stack.append(f.arg)

            case TInst.BINOP:
                match f.arg:
                    case 'add':
                        self.stack.append(self.stack.pop() + self.stack.pop())
                    case _:
                        pass
                    
            case TInst.UNOP:
                match f.arg:
                    case 'negate':
                        self.stack.append(-self.stack.pop())
                    case _:
                        pass
            case _:
                pass
    
    def run(self):
        while self.pc < len(self.instrs):
            print(f'{self.pc}\t{self.fetch()}')
            self.exec()
            print(self.stack)
            self.pc += 1

            print('-'*50)

def main():

    i = []
    i.append(Inst(TInst.LOAD, 1))
    i.append(Inst(TInst.LOAD, 2))
    i.append(Inst(TInst.LOAD, 30))
    i.append(Inst(TInst.BINOP, 'add'))
    i.append(Inst(TInst.BINOP, 'add'))
    i.append(Inst(TInst.UNOP, 'negate'))

    interp = Interp(i)
    interp.run()
    
    
    f = sys.argv[1]
    p = Parser(f)
    p.tree.printer()
    print('-'*50)

if __name__ == '__main__':
    main()