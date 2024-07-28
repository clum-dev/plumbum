from parser import *

class Stack:
    items:list
    
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

    def empty(self) -> bool:
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.empty():
            return None
        return self.items.pop()
    
    def peek(self):
        if self.empty():
            return None
        return self.items[-1]


    

class Instr:

    l:any
    r:any
    op:any

    def __init__(self, l, r) -> None:
        self.l, self.r = l, r

    def add(self):
        return self.l + self.r

    def sub(self):
        return self.l - self.r
    
    def mult(self):
        return self.l * self.r
    
    def div(self):
        return self.l / self.r

class Engine:

    infeed:list
    stack:Stack
    count:int

    def __init__(self, infeed) -> None:
        self.infeed = infeed
        self.stack = Stack()
        self.count = 0

    def run(self):
        print(f'IN   {self.infeed}')
        while len(self.infeed) > 0 and self.count < 10:
            print(f'EXEC [{self.count}]\n{str(self.stack)}\n{"-"*50}')
            self.stack.push(self.infeed.pop(0))
            self.execute()
            self.count += 1
            print(f'IN   {self.infeed}')

    def execute(self):

        op = self.stack.peek()
        
        if op in ['+', '-', '*', '/']:
            op = self.stack.pop()
            left = self.stack.pop()
            right = self.stack.pop()

            # print(f'{left} {op} {right}')
            instr = Instr(left, right)

            match op:
                case '+':
                    self.stack.push(instr.add())
                case '-':
                    self.stack.push(instr.sub())
                case '*':
                    self.stack.push(instr.mult())
                case '/':
                    self.stack.push(instr.div())

e = Engine([1,2,'+',3,'*', 'EOF'])
e.run()