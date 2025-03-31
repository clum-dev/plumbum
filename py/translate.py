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
    anon_count:int

    def __init__(self, t:Tree):
        self.tree = t
        self.anon_count = 0
        self.root = self.translate(self.tree, None)

    def __str__(self):
        return f'GENERATOR :: {self.root.name}'

    def __repr__(self):
        return self.__str__()

    def printer(self):
        print(self.__str__())
        print(self.root)
    
    def make_var_data(self, t:Tree, parent:Data) -> Data:
        
        ptype = None
        if isinstance(t, TParam):
            name = t.name
            ptype = t.ptype
        elif t.tok.t == TokType.TYPED_ID:
            # TODO make a tree subclass for typed id???
            name = t.leaves[0]
            ptype = t.leaves[1]
            if isinstance(ptype, Tree):
                ptype = ptype.tok.t

        elif t.tok.t == TokType.ID:
            name = t.leaves[0]
            ptype = TokType.TYPE_ANY

        else:
            raise RuntimeError(f'Unhandled passed arg: {type(t)}: {t.tok.t}')
        
        out_type = {
            TokType.TYPE_INT:       DInt,
            TokType.TYPE_FLOAT:     DFloat,
            TokType.TYPE_STRING:    DString,
            TokType.TYPE_BOOL:      DBool,
            TokType.TYPE_NULL:      DNull,
            TokType.TYPE_ANY:       DAny,
            TokType.TYPE_DEF:       DAny,
        }[ptype]

        return out_type(value= None, dtype=ptype, parent=parent, name=name)

    def translate(self, t:TTREE, parent:Data) -> None|Data:
        
        if t is None:
            return

        if not isinstance(t, TTREE):
            raise TypeError(f'Expected TTREE, got {type(t)}')
        
        assert isinstance(parent, (DScope, type(None)))
        
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

                func = DFunc(value=None,
                             dtype=t.ret.leaves[-1],
                             parent=parent,
                             name=t.name)
                
                parent.d_locals[t.name] = func
                self.translate(t.params, func)
                self.translate(t.ret, func)
                self.translate(t.block, func)
                                                
            case TokType.PARAM_SEQ:
                if DEBUG: print('TR param seq')
                assert isinstance(t, TParamSeq)

                param:TParam
                default_count = 0
                for param in t.params:
                    assert isinstance(param, TParam)
                    parent.d_locals[param.name] = self.translate(param, parent)
                    if param.has_default:
                        default_count += 1

                parent.insts.append(Inst(InstType.BUILD_DEFAULTS, default_count))
                    
            case TokType.PARAM:
                if DEBUG: print('TR param')
                assert isinstance(t, TParam)
                if t.has_default:
                    # print(f'has default -> generate: {t.leaves[0].tok}')
                    self.generate(t.leaves[0], parent)
                return self.make_var_data(t, parent)
            
            case TokType.BLOCK:
                if DEBUG: print('TR block')
                for l in t.leaves:
                    # print(l.tok.t)
                    self.translate(l, parent)

            case TokType.VAR | TokType.CONST:
                
                if DEBUG: print('TR var const')
                for l in t.leaves:

                    if l.tok.t in [TokType.TYPED_ID, TokType.ASSIGN]:
                        self.translate(l, parent)

                    # if l.tok.t == TokType.TYPED_ID:
                    #     var:Data = self.make_var_data(l, parent)
                    #     parent.d_locals[var.name] = var

                    # elif l.tok.t == TokType.ASSIGN:
                    #     var:Data = self.make_var_data(l.leaves[0], parent)
                    #     parent.d_locals[var.name] = var
                    #     self.generate(l, parent)
                
            case TokType.TYPED_ID | TokType.ID:
                assert isinstance(parent, (DScope))
                var:Data = self.make_var_data(t, parent)
                parent.d_locals[var.name] = var

            case TokType.ASSIGN:
                var:Data = self.make_var_data(t.leaves[0], parent)
                parent.d_locals[var.name] = var
                self.generate(t, parent)
            
            case _:
                if DEBUG: print(f'unhandled, try gen:\t{t}')
                self.generate(t, parent)
                
    def generate(self, t:Tree, parent:Data) -> None:
        
        if t is None:
            return
        
        assert isinstance(parent, DScope)

        if t.tok.t == TokType.BLOCK:
            b = DScope(None, None, parent, f'_block{self.anon_count}')
            self.anon_count += 1
            self.translate(t, b)
            parent.d_locals[b.name] = b
            return b
            
        elif t.tok.t == TokType.RETURN:
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.RET))

        elif t.tok.t == TokType.CALL:
            parent.insts.append(Inst(InstType.LOADN, t.get_leftmost()))
            for l in t.leaves[1:]:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.CALL, len(t.leaves)))
            
        elif t.tok.t == TokType.ID:
            parent.insts.append(Inst(InstType.LOADN, t.get_leftmost()))
            
        elif t.tok.t == TokType.LIT_STRING:
            for l in t.leaves:
                s:Data = self.generate(l, parent)
                if l.tok.t == TokType.BLOCK:
                    assert isinstance(s, DScope)
                    parent.insts.append(Inst(InstType.LOADN, s.name))
                    parent.insts.append(Inst(InstType.CALL, 1))
            parent.insts.append(Inst(InstType.BUILD_STR, len(t.leaves)))
        
        elif t.tok.t == TokType.RANGE:
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.BUILD_RANGE))

        elif t.tok.t in [TokType.STR_BASE, TokType.ESC_CHAR]:
            parent.insts.append(Inst(InstType.LOADV, DString(t.get_leftmost(), str, parent)))

        elif t.tok.t.has_attr(TokAttr.LITERAL):
            if not t.tok.t == TokType.LIT_STRING:
                parent.insts.append(Inst(InstType.LOADV, t.get_leftmost()))
            else:
                self.generate(t, parent)

        elif t.tok.t.has_attr(TokAttr.ASSIGN):
            self.generate(t.leaves[1], parent)
            parent.insts.append(Inst(InstType.STORE, t.leaves[0].get_leftmost()))

        elif t.tok.t.has_attr(TokAttr.BINOP):
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.BINOP, t.tok.t))

        elif t.tok.t.has_attr(TokAttr.UNOP):
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.UNOP, t.tok.t))

        elif t.tok.t.has_attr(TokAttr.PIPE) or t.tok.t == TokType.PIPE:
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.PIPE, t.tok.t))

        elif t.tok.t.has_attr(TokAttr.PRIMARY):
            ...
            # TODO do this

        elif t.tok.t == TokType.EXPR_SEQ:
            for l in t.leaves:
                self.generate(l, parent)
            parent.insts.append(Inst(InstType.BUILD_SEQ, len(t.leaves)))

        elif t.tok.t == TokType.LIST_RAW:
            self.generate(t.leaves[0], parent)
            
        else:
            if DEBUG: print(f'unhandled instr:\t{t}')

        if DEBUG: print(f'GEN {t.tok.t}')
        

def main():

    p = Parser('test4.pb', False)
    p.tree.printer()
    print('-'*80)

    g = Generator(p.tree)
    print('-'*80)
    g.printer()
    # print('done')


if __name__ == '__main__':
    main()

