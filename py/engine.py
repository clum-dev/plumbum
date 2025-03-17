from typing import Any
from parser import *
from translate import *


class Stack:

    items:list[Data]
    
    def __init__(self, items=None) -> None:
        self.items = []
        if items is not None:
            if isinstance(items, list):
                self.items += items
            else:
                self.items.append(items)

    def __str__(self) -> str:
        if len(self.items) == 0:
            return '<empty stack>'
        return '\n'.join(list(map(lambda x: f'{x[0]}: {x[1]}', 
                                  list(enumerate(self.items)))))

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def push_multi(self, items:list):
        for i in items:
            self.items.append(i)
    
    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def clear(self):
        self.items.clear()


class Engine:

    scope:DScope
    data_stack:Stack

    def __init__(self, scope:DScope) -> None:       
        assert isinstance(scope, DScope)
        self.scope = scope
        self.data_stack = Stack()

    def run_entrypoint(self):

        # TODO fix this #FIXME        
        
        entry:DScope = self.scope.lookup_local('main')
        entry = entry.lookup_local('BLOCK')
        assert isinstance(entry, DScope)
        self.exec_scope(entry)
        print('done')

    def exec_scope(self, scope:DScope):

        self.scope = scope.lookup_local('BLOCK')
        print(f'SCOPE :: {self.scope.name}\n')

        for i in self.scope.insts:
            print(i)
        print('='*80)

        # exec
        for i in scope.insts:
            self.eval_inst(i)
            print(self.data_stack)
            print('-'*80)

    def eval_inst(self, inst:Inst) -> DScope|None:
        
        print(f'>>> {inst}')
        
        match inst.name:
            case InstType.RET:
                raise NotImplementedError('eval inst ret')
                
                # self.scope._ret = self.data_stack.pop()
                # self.data_stack.clear()

            case InstType.CALL:
                target = self.scope.lookup_local(inst.arg)
                assert target.isCallable
                
                raise NotImplementedError('eval inst call')

                # for i in range(s._call_non_defaults):
                #     a = s.lookup_local(s._call_args[i])
                #     # print(a)
                #     a._assign(self.data_stack.pop())

                # inner = Engine(target.scope)
                # inner.exec_scope(target.scope)
                # self.data_stack.push(target.scope._ret)
            
            case InstType.LOADV:
                self.data_stack.push(inst.arg)

            case InstType.LOADN:
                target = self.scope.lookup_local(inst.arg)
                self.data_stack.push(target)
            
            case InstType.STORE:
                target = self.scope.lookup_local(inst.arg)
                if target is None:
                    self.scope.add_new_local(inst.arg)
                    target = self.scope.lookup_local(inst.arg)

                target._assign(self.data_stack.pop())

            case InstType.BINOP:
                assert isinstance(inst.arg, TokType)
                
                right = self.data_stack.pop()
                left = self.data_stack.pop()

                match inst.arg:
                    case TokType.ADD:
                        self.data_stack.push(left._add(right))
                    case TokType.SUB:
                        self.data_stack.push(left._sub(right))
                    case TokType.MULT:
                        self.data_stack.push(left._mult(right))
                    case TokType.DIV:
                        self.data_stack.push(left._div(right))
                    case TokType.MOD:
                        self.data_stack.push(left._mod(right))
                    case TokType.POWER:
                        self.data_stack.push(left._pow(right))
            
            case InstType.UNOP:
                assert isinstance(inst.arg, TokType)

                left = self.data_stack.pop()

                match inst.arg:
                    case TokType.POSATE:
                        self.data_stack.push(left._posate())
                    case TokType.NEGATE:
                        self.data_stack.push(left._negate())
                    case TokType.INCREMENT:
                        self.data_stack.push(left._increment())
                    case TokType.DECREMENT:
                        self.data_stack.push(left._decrement())
                            
        return None

def main():
    fname = sys.argv[1] if len(sys.argv) > 1 else 'test4.pb'
    p = Parser(fname)
    p.tree.printer()
    g = Generator(p.tree)
    e = Engine(g.root)
    print('='*80)
    e.run_entrypoint()
    print('='*80)

if __name__ == '__main__':
    main()