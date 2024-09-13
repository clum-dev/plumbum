from typing import Any
from typing_extensions import Self

class Data:

    isConst:bool
    isCallable:bool
    isIterable:bool
    isIndexable:bool

    value:Self|list[Self]
    dtype:Any

    def __init__(self, value, dtype) -> None:
        self.value, self.dtype = value, dtype

    # Magic methods
    def _len(self):
        assert self.isIterable
        raise NotImplementedError(self._len.__name__)

    # Assignment
    def _assign(self, value:Self):
        assert not self.isConst
        raise NotImplementedError(self._assign.__name__)

    def _assign_add(self, value:Self):
        assert not self.isConst
        raise NotImplementedError(self._assign_add.__name__)

    def _assign_sub(self, value:Self):
        assert not self.isConst
        raise NotImplementedError(self._assign_sub.__name__)

    def _assign_mult(self, value:Self):
        assert not self.isConst
        raise NotImplementedError(self._assign_mult.__name__)

    def _assign_div(self, value:Self):
        assert not self.isConst
        raise NotImplementedError(self._assign_div.__name__)

    def _assign_mod(self, value:Self):
        assert not self.isConst
        raise NotImplementedError(self._assign_mod.__name__)

    # Pipes
    def _pipe_dist(self, value:Self):
        assert value.isIterable
        raise NotImplementedError(self._pipe_dist.__name__)
    
    def _pipe_funnel(self, value:Self):
        assert self.isIterable
        raise NotImplementedError(self._pipe_funnel.__name__)
    
    def _pipe_pair(self, value:Self):
        assert self.isIterable and value.isIterable
        raise NotImplementedError(self._pipe_pair.__name__)

    def _pipe_map(self, value:Self):
        raise NotImplementedError(self._pipe_map.__name__)
    
    def _pipe_filter(self, value:Self):
        raise NotImplementedError(self._pipe_filter.__name__)

    def _pipe_reduce(self, value:Self):
        raise NotImplementedError(self._pipe_reduce.__name__)
    
    def _pipe_member(self, value:Self):
        raise NotImplementedError(self._pipe_reduce.__name__)

    def _pipe_zip(self):
        raise NotImplementedError(self._pipe_zip.__name__)
    
    def _pipe_flatten(self):
        raise NotImplementedError(self._pipe_flatten.__name__)
    
    def _pipe_any(self):
        raise NotImplementedError(self._pipe_any.__name__)
    
    def _pipe_each(self, value:Self):
        raise NotImplementedError(self._pipe_each.__name__)
    
    def _pipe_sum(self):
        raise NotImplementedError(self._pipe_sum.__name__)

    def _pipe(self, value:Self):
        raise NotImplementedError(self._pipe.__name__)
    
    # Boolean Logic
    def _or(self, value:Self):
        raise NotImplementedError(self._or.__name__)

    def _and(self, value:Self):
        raise NotImplementedError(self._and.__name__)
    
    def _not(self):
        raise NotImplementedError(self._not.__name__)
    
    # Comparisons
    def _eq(self, value:Self):
        raise NotImplementedError(self._eq.__name__)

    def _neq(self, value:Self):
        raise NotImplementedError(self._neq.__name__)

    def _lt(self, value:Self):
        raise NotImplementedError(self._lt.__name__)

    def _gt(self, value:Self):
        raise NotImplementedError(self._gt.__name__)
    
    def _lte(self, value:Self):
        raise NotImplementedError(self._lte.__name__)
    
    def _gte(self, value:Self):
        raise NotImplementedError(self._gte.__name__)
        
    # Bitwise
    def _bit_not(self):
        raise NotImplementedError(self._bit_not.__name__)

    def _bit_or(self, value:Self):
        raise NotImplementedError(self._bit_or.__name__)

    def _bit_xor(self, value:Self):
        raise NotImplementedError(self._bit_xor.__name__)

    def _bit_and(self, value:Self):
        raise NotImplementedError(self._bit_and.__name__)
    
    def _bit_shr(self, value:Self):
        raise NotImplementedError(self._bit_shr.__name__)
    
    def _bit_shl(self, value:Self):
        raise NotImplementedError(self._bit_shl.__name__)
        
    # Math
    def _add(self, value:Self):
        raise NotImplementedError(self._add.__name__)
    
    def _sub(self, value:Self):
        raise NotImplementedError(self._sub.__name__)
    
    def _mult(self, value:Self):
        raise NotImplementedError(self._mult.__name__)
    
    def _div(self, value:Self):
        raise NotImplementedError(self._div.__name__)

    def _mod(self, value:Self):
        raise NotImplementedError(self._mod.__name__)

    def _pow(self, value:Self):
        raise NotImplementedError(self._pow.__name__)

    # Crement
    def _increment(self):
        raise NotImplementedError(self._increment.__name__)
    
    def _decrement(self):
        raise NotImplementedError(self._decrement.__name__)

    # Primary access
    def _member(self, name:Self):
        raise NotImplementedError(self._member.__name__)
    
    def _index(self, index:Self):
        raise NotImplementedError(self._index.__name__)
    
    def _call(self, args:Self):
        raise NotImplementedError(self._call.__name__)

    # Type casting
    def _int(self):
        raise NotImplementedError(self._int.__name__)
    
    def _float(self):
        raise NotImplementedError(self._float.__name__)
        
    def _String(self):
        raise NotImplementedError(self._String.__name__)
    
    def _bool(self):
        raise NotImplementedError(self._bool.__name__)
        
    def _null(self):
        raise NotImplementedError(self._null.__name__)

    def _any(self):
        raise NotImplementedError(self._any.__name__)


class String(Data):

    def __init__(self, value, dtype) -> None:
        super().__init__(value, dtype)
        self.isCallable = False
        self.isConst = False
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

class List(Data):
    
    def __init__(self, value, dtype) -> None:
        super().__init__(value, dtype)
        self.isCallable = False
        self.isConst = False
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

