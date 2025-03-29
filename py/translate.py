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
    
    def make_var_data(self, var_tree:Tree|TParam):
        
        # TODO REDO PARAMS WITH DEFAULT -> USE ASSIGNMENT ???
        raise NotImplementedError('redo param defaults')

        if isinstance(var_tree, TParam):
            ptype = var_tree.ptype
            name = var_tree.name
            default = var_tree.default
        else:
            assert var_tree.tok.t == TokType.TYPED_ID
            ptype = var_tree.leaves[1]
            name = var_tree.leaves[0]
            default = None
        
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
                return self.make_var_data(t)
            
            case TokType.BLOCK:
                if DEBUG: print('TR block')
                for l in t.leaves:
                    # print(l.tok.t)
                    self.translate(l, parent)

            case TokType.VAR:
                if DEBUG: print('TR var')
                assert isinstance(parent, (DScope))
                
                if t.leaves[0].tok.t == TokType.TYPED_ID:
                    print('todo var decl')

                elif t.leaves[0].tok.t == TokType.ASSIGN:
                    self.generate(t.leaves[0], parent)
                
                # parent.d_locals[p.name] = self.translate(p, parent)

            case _:
                if DEBUG: print(f'unhandled:\t{t}')
                self.generate(t, parent)
                
    def generate(self, t:Tree, parent:Data) -> None:
        
        if t is None:
            return
        
        assert isinstance(parent, DScope)
        
        # print(t.tok.t)

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
            
        elif t.tok.t.has_attr(TokAttr.LITERAL):
            parent.insts.append(Inst(InstType.LOADV, t.get_leftmost()))

        elif t.tok.t.has_attr(TokAttr.ASSIGN):
            self.generate(t.leaves[1], parent)
            parent.insts.append(Inst(InstType.STORE, t.leaves[0].get_leftmost()))

        elif t.tok.t.has_attr(TokAttr.BINOP):
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.BINOP, t.tok.t))

        else:
            if DEBUG: print(f'unhandled instr:\t{t}')
        

def main():

    p = Parser('py/test4.pb', False)
    p.tree.printer()
    print('-'*50)

    g = Generator(p.tree)
    # g.printer()
    print('done')


if __name__ == '__main__':
    main()

