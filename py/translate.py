import sys
from typing_extensions import Self, Any
from enum import Enum, auto
from parser import *
from data import *


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
    arg:TokType|Data

    def __init__(self, name:InstType, arg:TokType|Data) -> None:
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

    tree:Tree                           # Parse tree
    level:int                           # Scope depth level
    parent:Self                         # Parent scope
    name:str                            # Lookup name

    _locals:dict[str, Data]             # Local data lookup 
    insts:list                          # Instruction list

    _call_args:list[str]                # Lookup names for args
    _call_non_defaults:int              # Number of non-default values
    _call_store_mode:Any                # e.g. |> for funcs (if used) - default |:

    _ret:Data                           # Data returned from scope

    debug:bool

    def __init__(self, tree:Tree, level:int=0, parent:Self|None=None, debug:bool=False) -> None:
        self.tree, self.level, self.parent = tree, level, parent
        self.debug = debug

        self._locals = {}
        self.insts = []

        self._call_args = []
        self._call_non_defaults = 0
        self._call_store_mode = TokType.PIPE_PAIR

        self._ret = DNull(None, None, self)
        
        if isinstance(tree, Tree):
            self.name = tree.tok.t.name

            for l in tree.leaves:
                if isinstance(l, Tree):
                    if not self.gen_local(l):
                        self.gen_inst(l)

    def __str__(self) -> str:
        return f'SCOPE :: {self.name}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def lookup_local(self, name:str) -> Data:
        res = self._locals.get(name)
        if res is not None:
            return res
        elif self.parent is not None:
            return self.parent.lookup_local(name)
        
        raise AttributeError(f'Scope {self.name} has no local attribute {name}')

    def gen_local(self, tree:Tree) -> bool:

        match tree.tok.t:
            case TokType.FUNC:
                func = self.gen_func(tree)
                self._locals[func.name] = func
            case TokType.PARAM_SEQ:
                params = self.gen_param_seq(tree)
                for p in params:
                    self._locals[p.name] = p
            case TokType.PARAM:
                param = self.gen_param(tree)
                self._locals[param.name] = param
            case TokType.VAR:
                for v in tree.leaves:
                    var = self.gen_param(v)
                    self._locals[var.name] = var
            
            case _:
                if self.debug:
                    print(f'Scope: {self.name}\t skipping local {tree.tok.t}')
                # raise NotImplementedError(f'gen local {tree.tok.t}')
                return False
        
        if self.debug:
            print(f'Scope: {self.name}\t adding local {tree.tok.t}')
        return True

    def gen_func(self, tree:Tree) -> Data:

        fscope = Scope(tree.leaves[4], self.level+1, self, debug=self.debug)
        store = tree.leaves[2]
        fscope._call_store_mode = store
        
        name = tree.leaves[0].get_last()
        params = fscope.gen_param_seq(tree.leaves[1], func_args=True) if tree.leaves[1] is not None else None
        ret = fscope.gen_param(tree.leaves[3]) if tree.leaves[3] is not None else DNull(value=None, dtype=None, scope=fscope, name='_ret')
    
        fscope._locals[ret.name] = ret
        if params is not None:
            for p in params:
                fscope._locals[p.name] = p
        
        return DFunc(None, ret.dtype, fscope, name=name)

    def gen_param_seq(self, tree:Tree, func_args:bool=False) -> list[Data]:

        if tree.tok.t == TokType.PARAM:
            return [self.gen_param(tree, func_arg=func_args)]
                
        assert tree.tok.t == TokType.PARAM_SEQ
        out = []
        for p in tree.leaves:
            out.append(self.gen_param(p, func_arg=func_args))

        return out

    def gen_param(self, tree:Tree, eval_default:bool=False, func_arg:bool=False) -> Data:
        assert tree.tok.t == TokType.PARAM
        name:str = tree.leaves[0].get_last()
        dtype = tree.leaves[1].tok.t
        val = tree.leaves[2].get_last() if tree.leaves[2] is not None else None
        
        if func_arg:
            self._call_args.append(name)
            if val == None:
                self._call_non_defaults += 1

        if not eval_default and tree.leaves[2] is not None and not tree.leaves[2].tok.t.has_attr(TokAttr.LITERAL):
            raise RuntimeError('gen param default is not literal')
        
        elif eval_default:
            self.insts.append(Inst(Inst.InstType.STORE, name))

        match dtype:
            case TokType.TYPE_INT:
                return DInt(value=val if val is not None else 0, dtype=int, scope=self, name=name)
            case TokType.TYPE_FLOAT:
                return DFloat(value=val if val is not None else 0.0, dtype=float, scope=self, name=name)
            case TokType.TYPE_STRING:
                raise NotImplementedError('gen param string')
                return DString(value=None, dtype=str, scope=self, name=name)
            case TokType.TYPE_BOOL:
                return DBool(value=val if val is not None else False, dtype=bool, scope=self, name=name)
            case TokType.TYPE_NULL:
                return DNull(value=val, dtype=None, scope=self, name=name)
            case TokType.TYPE_DEF:
                raise NotImplementedError('gen param typedef')
            case _:
                return DAny(value=val, dtype=Any, scope=self, name=name)
        
        return None

    def gen_literal(self, tree:Tree) -> Data:
        assert isinstance(tree, Tree)
        assert tree.tok.t.has_attr(TokAttr.LITERAL)

        match tree.tok.t:
            case TokType.LIT_INT:
                return DInt(int(tree.leaves[0]), int, self)
            case TokType.LIT_FLOAT:
                return DFloat(float(tree.leaves[0]), float, self)
            case TokType.LIT_STRING:
                raise NotImplementedError('gen literal string')
                return DString(tree.leaves[0], str, self)
            case TokType.LIT_TRUE | TokType.LIT_FALSE:
                return DFloat(bool(tree.leaves[0]), bool, self)
            case TokType.TYPE_NULL:
                return DNull(tree.leaves[0], None, self)
            case _:
                raise NotImplementedError('gen literal unhandled')
        
        return None
    
    def gen_inst(self, tree:Tree) -> bool:

        if tree.tok.t.has_attr(TokAttr.BINOP):
            self.gen_inst(tree.leaves[0])
            self.gen_inst(tree.leaves[1])
            self.insts.append(Inst(Inst.InstType.BINOP, tree.tok.t))
            
        elif tree.tok.t.has_attr(TokAttr.UNOP):
            self.gen_inst(tree.leaves[0])
            self.insts.append(Inst(Inst.InstType.UNOP, tree.tok.t))

        elif tree.tok.t.has_attr(TokAttr.LITERAL):
            self.insts.append(Inst(Inst.InstType.LOADV, self.gen_literal(tree)))
        
        elif tree.tok.t == TokType.ID:
            self.insts.append(Inst(Inst.InstType.LOADN, tree.leaves[0]))

        elif tree.tok.t == TokType.ASSIGN:
            self.gen_inst(tree.leaves[1])
            self.insts.append(Inst(Inst.InstType.STORE, tree.leaves[0].get_last()))

        elif tree.tok.t == TokType.CALL:
            
            if tree.leaves[1] is not None:
                if tree.leaves[1].tok.t == TokType.EXPR_SEQ:
                    for l in tree.leaves[1].leaves:
                        self.gen_inst(l)
                else:
                    self.gen_inst(tree.leaves[1])
            
            self.insts.append(Inst(Inst.InstType.CALL, tree.leaves[0].get_last()))

        elif tree.tok.t == TokType.RETURN:
            self.gen_inst(tree.leaves[0])
            self.insts.append(Inst(Inst.InstType.RET, None))

        else:
            if self.debug:
                print(f'Scope: {self.name}\t skipping inst {tree.tok.t}')
            # raise NotImplementedError(f'gen inst {tree.tok.t}')
            return False

        if self.debug:
            print(f'Scope: {self.name}\t adding inst {tree.tok.t.name}')
        return True


def main():
    pass

    print()

    # f = 'test2.pb'
    # if len(sys.argv) > 1:    
    #     f = sys.argv[1]

    p = Parser('test2.pb', False)
    p.tree.printer()
    print('-'*50)

    s = Scope(p.tree, 0)
    print(s)


if __name__ == '__main__':
    main()