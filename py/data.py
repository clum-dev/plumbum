from typing import Any
from typing_extensions import Self, Type
    
class Data:

    isConst:bool
    isCallable:bool
    isIterable:bool
    isIndexable:bool

    name:str
    value:Self|list[Self]
    dtype:Type
    scope:Any

    subclass:Type

    def __init__(self, value, dtype, scope, name:str|None=None) -> None:
        self.value, self.dtype = value, dtype
        self.scope = scope
        self.name = name

        self.isConst = False
        self.isCallable = False
        self.isIterable = False
        self.isIndexable = False

        self.subclass = None

    def __str__(self) -> str:
        return f'{self.name}: {self.value} ({self.dtype})'

    def __repr__(self) -> str:
        return self.__str__()

    # Magic methods
    def _len(self) -> Self:
        raise NotImplementedError(self._len.__name__)

    # Assignment
    def _assign(self, value:Self):
        raise NotImplementedError(self._assign.__name__)

    def _assign_add(self, value:Self):
        raise NotImplementedError(self._assign_add.__name__)

    def _assign_sub(self, value:Self):
        raise NotImplementedError(self._assign_sub.__name__)

    def _assign_mult(self, value:Self):
        raise NotImplementedError(self._assign_mult.__name__)

    def _assign_div(self, value:Self):
        raise NotImplementedError(self._assign_div.__name__)

    def _assign_mod(self, value:Self):
        raise NotImplementedError(self._assign_mod.__name__)

    # Pipes
    def _pipe_dist(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_dist.__name__)
    
    def _pipe_funnel(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_funnel.__name__)
    
    def _pipe_pair(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_pair.__name__)

    def _pipe_map(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_map.__name__)
    
    def _pipe_filter(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_filter.__name__)

    def _pipe_reduce(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_reduce.__name__)
    
    def _pipe_member(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_reduce.__name__)

    def _pipe_zip(self) -> Self:
        raise NotImplementedError(self._pipe_zip.__name__)
    
    def _pipe_flatten(self) -> Self:
        raise NotImplementedError(self._pipe_flatten.__name__)
    
    def _pipe_any(self) -> Self:
        raise NotImplementedError(self._pipe_any.__name__)
    
    def _pipe_each(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe_each.__name__)
    
    def _pipe_sum(self) -> Self:
        raise NotImplementedError(self._pipe_sum.__name__)

    def _pipe(self, value:Self) -> Self:
        raise NotImplementedError(self._pipe.__name__)
    
    # Boolean Logic
    def _or(self, value:Self) -> Self:
        raise NotImplementedError(self._or.__name__)

    def _and(self, value:Self) -> Self:
        raise NotImplementedError(self._and.__name__)
    
    def _not(self) -> Self:
        raise NotImplementedError(self._not.__name__)
    
    # Comparisons
    def _eq(self, value:Self) -> Self:
        raise NotImplementedError(self._eq.__name__)

    def _neq(self, value:Self) -> Self:
        raise NotImplementedError(self._neq.__name__)

    def _lt(self, value:Self) -> Self:
        raise NotImplementedError(self._lt.__name__)

    def _gt(self, value:Self) -> Self:
        raise NotImplementedError(self._gt.__name__)
    
    def _lte(self, value:Self) -> Self:
        raise NotImplementedError(self._lte.__name__)
    
    def _gte(self, value:Self) -> Self:
        raise NotImplementedError(self._gte.__name__)
        
    # Bitwise
    def _bit_not(self) -> Self:
        raise NotImplementedError(self._bit_not.__name__)

    def _bit_or(self, value:Self) -> Self:
        raise NotImplementedError(self._bit_or.__name__)

    def _bit_xor(self, value:Self) -> Self:
        raise NotImplementedError(self._bit_xor.__name__)

    def _bit_and(self, value:Self) -> Self:
        raise NotImplementedError(self._bit_and.__name__)
    
    def _bit_shr(self, value:Self) -> Self:
        raise NotImplementedError(self._bit_shr.__name__)
    
    def _bit_shl(self, value:Self) -> Self:
        raise NotImplementedError(self._bit_shl.__name__)
        
    # Math
    def _add(self, value:Self) -> Self:
        raise NotImplementedError(self._add.__name__)
    
    def _sub(self, value:Self) -> Self:
        raise NotImplementedError(self._sub.__name__)
    
    def _mult(self, value:Self) -> Self:
        raise NotImplementedError(self._mult.__name__)
    
    def _div(self, value:Self) -> Self:
        raise NotImplementedError(self._div.__name__)

    def _mod(self, value:Self) -> Self:
        raise NotImplementedError(self._mod.__name__)

    def _pow(self, value:Self) -> Self:
        raise NotImplementedError(self._pow.__name__)

    def _posate(self) -> Self:
        raise NotImplementedError(self._posate.__name__)

    def _negate(self) -> Self:
        raise NotImplementedError(self._negate.__name__)

    # Crement
    def _increment(self) -> Self:
        raise NotImplementedError(self._increment.__name__)
    
    def _decrement(self) -> Self:
        raise NotImplementedError(self._decrement.__name__)

    # Primary access
    def _member(self, name:Self) -> Self:
        raise NotImplementedError(self._member.__name__)
    
    def _index(self, index:Self) -> Self:
        raise NotImplementedError(self._index.__name__)
    
    def _call(self, args:Self) -> Self:
        raise NotImplementedError(self._call.__name__)

    # Type casting
    def _int(self) -> Self:
        raise NotImplementedError(self._int.__name__)
    
    def _float(self) -> Self:
        raise NotImplementedError(self._float.__name__)
        
    def _str(self) -> Self:
        raise NotImplementedError(self._str.__name__)
    
    def _bool(self) -> Self:
        raise NotImplementedError(self._bool.__name__)
        
    def _null(self) -> Self:
        raise NotImplementedError(self._null.__name__)

    def _any(self) -> Self:
        raise NotImplementedError(self._any.__name__)


class DPrim(Data):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)

    # Assignment
    def _assign(self, value:Data):
        assert not self.isConst
        self.value = self.dtype(value.value)

    def _assign_add(self, value:Data):
        assert not self.isConst
        self.value += self.dtype(value.value)

    def _assign_sub(self, value:Data):
        assert not self.isConst
        self.value -= self.dtype(value.value)

    def _assign_mult(self, value:Data):
        assert not self.isConst
        self.value *= self.dtype(value.value)

    def _assign_div(self, value:Data):
        assert not self.isConst
        self.value /= self.dtype(value.value)

    def _assign_mod(self, value:Data):
        assert not self.isConst
        self.value %= self.dtype(value.value)

    # Pipes
    def _pipe(self, value:Data) -> Data:
        self._assign(value)
        return self

    # Comparisons
    def _eq(self, value:Data) -> Data:
        return DBool(self.value == self.dtype(value.value), dtype=bool, scope=self.scope)

    def _neq(self, value:Data) -> Data:
        return DBool(self.value != self.dtype(value.value), dtype=bool, scope=self.scope)
    
    def _lt(self, value:Data) -> Data:
        return DBool(self.value < self.dtype(value.value), dtype=bool, scope=self.scope)

    def _gt(self, value:Data) -> Data:
        return DBool(self.value > self.dtype(value.value), dtype=bool, scope=self.scope)

    def _lte(self, value:Data) -> Data:
        return DBool(self.value <= self.dtype(value.value), dtype=bool, scope=self.scope)

    def _gte(self, value:Data) -> Data:
        return DBool(self.value >= self.dtype(value.value), dtype=bool, scope=self.scope)
    
    # Bitwise
    def _bit_not(self) -> Data:
        return self.subclass(~self.value, self.dtype)
    
    def _bit_or(self, value:Data) -> Data:
        return self.subclass(self.value | value.value, self.dtype, scope=self.scope)
    
    def _bit_xor(self, value:Data) -> Data:
        return self.subclass(self.value ^ value.value, self.dtype, scope=self.scope)
    
    def _bit_and(self, value:Data) -> Data:
        return self.subclass(self.value & value.value, self.dtype, scope=self.scope)

    def _bit_shr(self, value:Data) -> Data:
        return self.subclass(self.value >> value.value, self.dtype, scope=self.scope)

    def _bit_shl(self, value:Data) -> Data:
        return self.subclass(self.value << value.value, self.dtype, scope=self.scope)
    
    # Math
    def _add(self, value:Data) -> Data:
        return self.subclass(self.value + value.value, self.dtype, scope=self.scope)
    
    def _sub(self, value:Data) -> Data:
        return self.subclass(self.value - value.value, self.dtype, scope=self.scope)

    def _mult(self, value:Data) -> Data:
        return self.subclass(self.value * value.value, self.dtype, scope=self.scope)
    
    def _div(self, value:Data) -> Data:
        return self.subclass(self.value / value.value, self.dtype, scope=self.scope)

    def _mod(self, value:Data) -> Data:
        return self.subclass(self.value % value.value, self.dtype, scope=self.scope)
    
    def _pow(self, value:Data) -> Data:
        return self.subclass(self.value % value.value, self.dtype, scope=self.scope)

    def _posate(self) -> Data:
        return self.subclass(+self.value, self.dtype, scope=self.scope)

    def _posate(self) -> Data:
        return self.subclass(-self.value, self.dtype, scope=self.scope)

    # Crement
    def _increment(self) -> Data:
        self.value += 1
        return self
    
    def _decrement(self) -> Data:
        self.value -= 1
        return self

    # Primary access
    def _member(self, name):
        # TODO
        return super()._member(name)

    def _index(self, index):
        # TODO
        return super()._index(index)

    def _call(self, args):
        # TODO
        return super()._call(args)
    
    # Type casting
    def _int(self):
        self.dtype = int
        self.value = int(self.value)

    def _float(self):
        self.dtype = float
        self.value = float(self.value)

    def _str(self):
        self.dtype = str
        self.value = str(self.value)

    def _bool(self):
        self.dtype = bool
        self.value = bool(self.value)

    def _null(self):
        self.dtype = None
        self.value = None
    
    def _any(self):
        self.dtype = Any
    

class DAny(DPrim):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)

class DInt(DPrim):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)
        self.subclass = DInt
                
class DFloat(DPrim):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)
        self.subclass = DFloat

class DBool(DPrim):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)
        self.subclass = DBool

class DNull(DPrim):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)
        self.subclass = DNull

class DString(Data):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)
        self.isIndexable = True
        self.isIterable = True

    def upper(self):
        # Convert to uppercase
        pass

    def lower(self):
        # Convert to lowercase
        pass

    def reverse(self):
        # Reverse string
        pass

    def trim(self, value:Data):
        # Shorten string by x number of chars
        pass

    def replace(self, old:Data, new:Data):
        # Replace substrings of old with new
        pass

    def reap(self, substr:Data, limit:Data):
        # Remove all substring instances in string
        pass

    def count(self, substr:Data):
        # Count number of substrings
        pass

    def split(self):
        # Split string into list
        pass


class DList(Data):
    
    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)
        self.isIndexable = True
        self.isIterable = True

    def _add(self, value:Data):
        pass
        # TODO override this to append 
    
    def append(self, value:Data):
        self._add(value)

    def insert(self, value:Data, index:Data):
        pass
    
    def remove(self, index:Data):
        pass

    def pluck(self, value:Data):
        pass
        
    def push(self, value:Data):
        pass

    def pop(self):
        pass

    def index(self, value:Data):
        pass

    def contains(self, value:Data):
        pass

    def concat(self, value:Data):
        pass

    def splay(self, value:Data):
        pass

    def join(self):
        pass
    
    def reverse(self):
        pass


class DDict(Data):

    def __init__(self, value, dtype, scope, name=None):
        super().__init__(value, dtype, scope, name)


class DFunc(Data):

    def __init__(self, value, dtype, scope, name = None):
        super().__init__(value, dtype, scope, name)
        self.isCallable = True

    def _call(self, args:Self) -> Data:
        raise RuntimeError('func call: todo')
    
