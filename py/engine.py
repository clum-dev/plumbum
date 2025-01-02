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

    scope:Scope
    data_stack:Stack

    def __init__(self, scope:Scope) -> None:       
        self.scope = scope
        self.data_stack = Stack()

    def run_entrypoint(self):
        entry = self.scope.lookup_local('main')
        self.exec_scope(entry.scope)
        print('done')

    def exec_scope(self, scope:Scope):
        self.scope = scope

        print(f'SCOPE :: {scope.name}\n')
        for i in scope.insts:
            print(i)
        print('='*80)

        for i in scope.insts:
            self.eval_inst(i)
            print(self.data_stack)
            print('-'*80)

    def eval_inst(self, inst:Inst) -> Data|None:
        
        print(f'>>> {inst}')
        
        match inst.name:
            case Inst.InstType.RET:
                self.scope._ret = self.data_stack.pop()
                self.data_stack.clear()

            case Inst.InstType.CALL:
                target = self.scope.lookup_local(inst.arg)
                assert target.isCallable
                s:Scope = target.scope

                for i in range(s._call_non_defaults):
                    a = s.lookup_local(s._call_args[i])
                    # print(a)
                    a._assign(self.data_stack.pop())

                inner = Engine(target.scope)
                inner.exec_scope(target.scope)
                self.data_stack.push(target.scope._ret)
            
            case Inst.InstType.LOADV:
                self.data_stack.push(inst.arg)

            case Inst.InstType.LOADN:
                target = self.scope.lookup_local(inst.arg)
                self.data_stack.push(target)
            
            case Inst.InstType.STORE:
                target = self.scope.lookup_local(inst.arg)
                target._assign(self.data_stack.pop())

            case Inst.InstType.BINOP:
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
            
            case Inst.InstType.UNOP:
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
    e = Engine(Scope(Parser('test2.pb').tree, debug=True))
    print('='*80)
    # e.scope.tree.printer()
    e.run_entrypoint()

if __name__ == '__main__':
    main()