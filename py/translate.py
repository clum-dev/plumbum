import sys
from typing import Union
from typing_extensions import Self, Any
from parser import *
from data import *

TTREE = Union[Tree, TFunc, TParam, TParamSeq]

class Generator:
    
    tree:Tree
    root:DScope

    def __init__(self, p:Parser):
        self.tree = p.tree
        prog = self.translate(self.tree, None)
        self.translate(self.tree.get_leftmost(), prog)

    def __str__(self):
        return f'GENERATOR :: '#{self.root.name}'

    def __repr__(self):
        return self.__str__()

    def translate(self, t:TTREE, parent:Data) -> Data:
        match t.tok.t:
            case TokType.PROGRAM:
                print('TR prog')
                return DScope('PROG', None, None, 'PROG')

            case TokType.FUNC:
                print('TR func')
                assert isinstance(t, TFunc)
                assert isinstance(parent, DScope)
                func = DFunc(value=None,
                             dtype=t.ret,
                             parent=parent,
                             name=t.name)
                
                parent.d_locals[t.name] = func
                                                
            case TokType.PARAM_SEQ:
                print('TR param seq')
                assert isinstance(t, TParamSeq)
                assert isinstance(parent, (DScope))
                param:TParam
                for param in t.params:
                    parent.d_locals[param.name] = self.translate(param, parent)
                    
            case TokType.PARAM:
                print('TR param')
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

                return out_type(value=t.default, dtype=t.ptype, parent=parent, name=t.name)


def main():

    p = Parser('test4.pb', False)
    p.tree.printer()
    print('-'*50)

    g = Generator(p)


if __name__ == '__main__':
    main()

