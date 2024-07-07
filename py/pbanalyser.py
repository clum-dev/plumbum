from typing import List

from pblexer import gen_refined, Token
from pbparser import Parse, Tree
from dataclasses import dataclass
from enum import Enum


class Var:
    class VarType(Enum):
        ANY=0

        INT=1
        FLOAT=2
        BOOL=3
        NULL=4

        STRING=5
        LIST=6
        DICT=7

        CUSTOM=8
    
    class _String:
        pass

    class _List:
        pass

    class _Dict:
        pass
    
    tok: Token
    ttype: VarType
    raw: str
    val: any
    
    def __init__(self, var) -> None:
        if isinstance(var, Tree):
            
            print(f'var init:\t{var}')
            
            tok = var.leaves[0]
            self.ttype = self.VarType.ANY
            if len(var.leaves) > 1:
                self.ttype = self.get_type(var.leaves[1])
            
    def get_type(self, typedef) -> VarType:
        if isinstance(typedef, Tree) and len(typedef.leaves) > 0:
            if len(typedef.leaves) > 0:
                
                # TODO 21/02/2024 handle subtypes e.g. List<String> etc
                
                match typedef.leaves[0].ttype:
                    case 'T_TYPE_ANY':
                        return self.VarType.ANY
                    case 'T_TYPE_INT':
                        return self.VarType.INT
                    case 'T_TYPE_FLOAT':
                        return self.VarType.FLOAT
                    case 'T_TYPE_BOOL':
                        return self.VarType.BOOL
                    case 'T_TYPE_NULL':
                        return self.VarType.NULL
                    
                    case 'T_TYPE_STR':
                        return self.VarType.STRING
                    
class TopLevel:

    class TopLevelType(Enum):
        FUNC=0
        STRUCT=1
        ENUM=2
        CONST=3
        USE=4

    ttype: TopLevelType
    data: any

    def __init__(self, ttype:TopLevelType, tree:Tree) -> None:
        self.ttype = ttype

        match ttype:
            case TopLevel.TopLevelType.FUNC:
                name, method = None, None
                if isinstance(tree.leaves[0], Tree):
                    name = tree.leaves[0].leaves[0]
                    method = tree.leaves[0].leaves[1]
                else:
                    name = tree.leaves[0]

                paramPipe = tree.leaves[1].tok
                params = tree.leaves[1].leaves[0].leaves

                returnType = tree.leaves[2]

                print(f'func: {name}\t({method})')
                print(f'paramPipe: {paramPipe}')
                print(f'params: {params}')
                print(f'returnType: {returnType}')

                paramVars = []
                for p in params:
                    v = Var(p)


    @dataclass
    class Func:
        tok: Token

        name: Token
        method: Token
        _params: List[Var]
        _paramPipe: Token

        _locals: List[Var]
    
    @dataclass
    class Struct:
        tok: Token

        name: str
        _members: List[Var]

    @dataclass
    class Enum:
        tok: Token

        name: str
        _members: List[Var]

    @dataclass
    class Const:
        _members: List[Var]

    @dataclass
    class Use:
        _members: List[Var]

        
class ProgramData:
    topLvl: List[TopLevel]

    def __init__(self, tree:Tree) -> None:
        for i, leaf in enumerate(tree.leaves):
            match leaf.tok.ttype:
                case "T_FUNC":
                    tlvl = TopLevel(TopLevel.TopLevelType.FUNC, leaf)
                
                case _:
                    raise ValueError("Analyser: Top level: Unreachable invalid top level name")
            



def main():
    ref = gen_refined(False)
    p = Parse(ref, debug=False)
    
    p.begin()
    # print('='*60)
    p.printer()

    print('='*60)
    # data = ProgramData(p.tree)

    
if __name__ == '__main__':
    main()