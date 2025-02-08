import sys
from typing_extensions import Self, Any
from parser import *
from data import *

class Generator:
    
    root:DScope

    def __init__(self, tree:Tree):
        self.root = self.gen_data(None, tree)

    def __str__(self):
        return f'GENERATOR :: {self.root.name}'

    def __repr__(self):
        return self.__str__()

    def gen_data(self, parent:DScope|None, tree:Tree) -> Data|Tree|None:

        if tree.tok.t == TokType.COMMENT:
            return None

        d = None
        match tree.tok.t:
            case TokType.PROGRAM:
                d = DScope(None, Any, None)
                d.name = tree.tok.t.name
                for l in tree.leaves:
                    child = self.gen_data(d, l)
                    if child is not None:
                        d.d_locals[child.name] = child
                
            case TokType.FUNC:
                d = DFunc(None, Any, parent)
                d.name = tree.leaves[0].get_last()          # func name
                d.call_store_mode = tree.leaves[2]          # store mode
                self.add_param_seq(d, tree.leaves[1])       # func params
                self.add_param_unset(d, tree.leaves[3])     # return type
                block = self.gen_data(d, tree.leaves[4])    # block
                d.d_locals[block.name] = block

            case TokType.STRUCT:
                raise NotImplementedError('gen scope struct')
            
            case TokType.BLOCK:
                d = DScope(None, Any, parent)
                d.name = tree.tok.t.name
                for l in tree.leaves:
                    if l.tok.t in [TokType.FUNC, TokType.STRUCT, TokType.BLOCK, TokType.VAR]:
                        child = self.gen_data(d, l)
                        if child is not None:
                            d.d_locals[child.name] = child
                    else:
                        d.insts = self.gen_instructions(d, l)

            case TokType.VAR:
                for l in tree.leaves:
                    self.add_param_default(parent, l)

            case _:
                raise NotImplementedError(f'gen data unhandled tok {tree.tok.t}')
                return None

        return d
        
    def add_param_seq(self, scope:DScope, tree:Tree):
        
        if tree is None:
            return

        assert tree.tok.t == TokType.PARAM_SEQ

        for l in tree.leaves:
            self.add_param_default(scope, l)
    
    def add_param_default(self, scope:DScope, tree:Tree):

        assert tree.tok.t == TokType.PARAM

        name:str = tree.leaves[0].get_last()
        dtype:TokType = tree.leaves[1]
        default:Tree = tree.leaves[2]

        if default is None:
            self.add_param_unset(scope, tree)
        else:
            d = self.param_data(scope, name, dtype)
            scope.d_locals[d.name] = d

            scope.insts += self.gen_instructions(scope, default)
            scope.insts.append(Inst(InstType.STORE, d.name))

    def add_param_unset(self, scope:DScope, tree:Tree):

        assert tree.tok.t == TokType.PARAM        

        name:str = tree.leaves[0].get_last()
        dtype:TokType = tree.leaves[1]

        d = self.param_data(scope, name, dtype)
        
        if d is not None:
            scope.d_locals[name] = d

    def param_data(self, scope:DScope, name:str, dtype:Tree) -> Data:
        
        p = None
        match dtype.tok.t:
            case TokType.TYPE_INT:
                p = DInt(value=0, dtype=int, parent=scope, name=name)
            case TokType.TYPE_FLOAT:
                p = DFloat(value=0.0, dtype=float, parent=scope, name=name)
            case TokType.TYPE_STRING:
                p = DString(value='', dtype=str, parent=scope, name=name)
            case TokType.TYPE_BOOL:
                p = DBool(value=False, dtype=bool, parent=scope, name=name)
            case TokType.TYPE_NULL:
                p = DNull(value=None, dtype=None, parent=scope, name=name)
            case TokType.TYPE_DEF:
                raise NotImplementedError('param_unset')
            case _:
                p = DAny(value=None, dtype=Any, parent=scope, name=name)

        if p is None:
            raise RuntimeError('param data param is none')
        return p

    def gen_instructions(self, scope:DScope, tree:Tree) -> list[Inst]:
        
        out = []
        if tree.tok.t.has_attr(TokAttr.BINOP):
            out += self.gen_instructions(scope, tree.leaves[1])
            out += self.gen_instructions(scope, tree.leaves[0])
            out += [Inst(InstType.BINOP, tree.tok.t)]
        
        elif tree.tok.t.has_attr(TokAttr.UNOP):
            out += self.gen_instructions(scope, tree.leaves[0])
            out += [Inst(InstType.UNOP, tree.tok.t)]
        
        elif tree.tok.t.has_attr(TokAttr.LITERAL):
            out += self.gen_load_lit(scope, tree)
        
        elif tree.tok.t == TokType.ID:
            out.append(Inst(InstType.LOADN, tree.leaves[0]))
        
        elif tree.tok.t == TokType.CALL:
            
            print('found call')
            tree.printer()
            print('-'*80)

            if tree.leaves[1] is not None:
                if tree.leaves[1].tok.t == TokType.EXPR_SEQ:
                    for l in tree.leaves[1].leaves:
                        out += self.gen_instructions(l)
                else:
                    out += self.gen_instructions(scope, tree.leaves[1])
            
                out.append(Inst(InstType.CALL, tree.leaves[0].get_last()))

        elif tree.tok.t == TokType.RETURN:
            out += self.gen_instructions(scope, tree.leaves[0])
            out.append(Inst(InstType.RET, None))
        
        else:
            raise NotImplementedError(f'gen instructions unhandled instruction {tree.tok.t}')

        return out

    def gen_load_lit(self, scope:DScope, tree:Tree) -> list[Inst]:

        assert isinstance(tree, Tree)
        assert tree.tok.t.has_attr(TokAttr.LITERAL)

        out = []
        match tree.tok.t:
            case TokType.LIT_INT:
                out.append(Inst(InstType.LOADV, DInt(int(tree.leaves[0]), int, scope)))
            case TokType.LIT_FLOAT:
                out.append(Inst(InstType.LOADV, DFloat(float(tree.leaves[0]), float, scope)))
            case TokType.LIT_STRING:
                out += self.gen_build_string(tree)
            case TokType.LIT_TRUE | TokType.LIT_FALSE:
                out.append(Inst(InstType.LOADV, DBool(bool(tree.leaves[0]), bool, scope)))
            case TokType.TYPE_NULL:
                return DNull(tree.leaves[0], None, scope)
            case _:
                raise NotImplementedError('gen literal unhandled')
            
        return out

    def gen_build_string(self, tree:Tree) -> list[Inst]:
        
        assert tree.tok.t == TokType.LIT_STRING
        out = []
        for l in tree.leaves:
            if l.tok.t in [TokType.STR_BASE, TokType.ESC_CHAR]:
                out.append(Inst(InstType.LOADV, l.leaves[0]))
            else:
                print(f'not base or esc: {l}')
                out += self.gen_instructions(l)

        out.append(Inst(InstType.BUILD_STR, None))
        return out


def main():

    p = Parser('test4.pb', False)
    p.tree.printer()
    print('-'*50)

    g = Generator(p.tree)
    print(g)


if __name__ == '__main__':
    main()