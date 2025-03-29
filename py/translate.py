import sys
from typing import Union
from typing_extensions import Self, Any
from parser import *
from data import *

TTREE = Union[Tree, TFunc, TParam, TParamSeq]
DEBUG = True

class Generator:
    
    tree:Tree
    root:DScope

    def __init__(self, t:Tree):
        self.tree = t
        self.root = self.translate(self.tree, None)

    def __str__(self):
        return f'GENERATOR :: {self.root.name}'

    def __repr__(self):
        return self.__str__()

    def printer(self):
        print(self.__str__())
        print(self.root)
        
    def translate(self, t:TTREE, parent:Data) -> None|Data:
        
        if t is None:
            return

        if not isinstance(t, TTREE):
            raise TypeError(f'Expected TTREE, got {type(t)}')
        
        match t.tok.t:
            case TokType.PROGRAM:
                if DEBUG: print('TR prog')
                out = DScope('PROG', None, None, 'PROG')
                for l in t.leaves:
                    self.translate(l, out)
                return out

            case TokType.FUNC:
                if DEBUG: print('TR func')
                assert isinstance(t, TFunc)
                assert isinstance(parent, DScope)
                func = DFunc(value=None,
                             dtype=t.ret,
                             parent=parent,
                             name=t.name)
                
                parent.d_locals[t.name] = func
                self.translate(t.params, func)
                self.translate(t.ret, func)
                self.translate(t.block, func)
                                                
            case TokType.PARAM_SEQ:
                if DEBUG: print('TR param seq')
                assert isinstance(t, TParamSeq)
                assert isinstance(parent, (DScope))
                param:TParam
                for param in t.params:
                    assert isinstance(param, TParam)
                    parent.d_locals[param.name] = self.translate(param, parent)
                    
            case TokType.PARAM:
                if DEBUG: print('TR param')
                assert isinstance(t, TParam)
                out_type = {
                    TokType.TYPE_INT:       DInt,
                    TokType.TYPE_FLOAT:     DFloat,
                    TokType.TYPE_STRING:    DString,
                    TokType.TYPE_BOOL:      DBool,
                    TokType.TYPE_NULL:      DNull,
                    TokType.TYPE_ANY:       DAny,
                    TokType.TYPE_DEF:       DAny,
                }[t.ptype]

                return out_type(value=t.default if t.default is not None and t.default.t.has_attr(TokAttr.LITERAL) else None,
                                dtype=t.ptype,
                                parent=parent,
                                name=t.name)
            
            case TokType.BLOCK:
                if DEBUG: print('TR block')
                for l in t.leaves:
                    # print(l.tok.t)
                    self.translate(l, parent)

            case TokType.VAR:
                if DEBUG: print('TR var')
                assert isinstance(parent, (DScope))
                p:TParam = t.leaves[0]
                parent.d_locals[p.name] = self.translate(p, parent)

            case _:
                if DEBUG: print(f'unhandled:\t{t}')
                self.generate(t, parent)
                
    def generate(self, t:Tree, parent:Data) -> None:
        
        if t is None:
            return
        
        assert isinstance(parent, DScope)
        
        print(t.tok.t)

        if t.tok.t == TokType.RETURN:
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.RET))
        elif t.tok.t == TokType.CALL:
            parent.insts.append(Inst(InstType.LOADN, t.get_leftmost()))
            for l in t.leaves[1:]:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.CALL))
        elif t.tok.t == TokType.ID:
            parent.insts.append(Inst(InstType.LOADN, t.get_leftmost()))
        elif t.tok.t in TokType.with_attr(TokAttr.LITERAL, value_only=False):
            parent.insts.append(Inst(InstType.LOADV, t.get_leftmost()))


def main():

    p = Parser('test4.pb', False)
    p.tree.printer()
    print('-'*50)

    g = Generator(p.tree)
    # g.printer()
    print('done')


if __name__ == '__main__':
    main()

