from typing import Any

class Data:

    isConst:bool
    isCallable:bool
    isIterable:bool
    isIndexable:bool

    value:Any
    dtype:Any

    def __init__(self, value, dtype) -> None:
        self.value, self.dtype = value, dtype

    # Assignment
    def _assign(self, value):
        raise NotImplementedError(self._assign.__name__)

    def _assign_add(self, value):
        raise NotImplementedError(self._assign_add.__name__)

    def _assign_sub(self, value):
        raise NotImplementedError(self._assign_sub.__name__)

    def _assign_mult(self, value):
        raise NotImplementedError(self._assign_mult.__name__)

    def _assign_div(self, value):
        raise NotImplementedError(self._assign_div.__name__)

    def _assign_mod(self, value):
        raise NotImplementedError(self._assign_mod.__name__)

    # Pipes
    def _pipe_dist(self, value):
        raise NotImplementedError(self._pipe_dist.__name__)
    
    def _pipe_funnel(self, value):
        raise NotImplementedError(self._pipe_funnel.__name__)
    
    def _pipe_pair(self, value):
        raise NotImplementedError(self._pipe_pair.__name__)

    def _pipe_map(self, value):
        raise NotImplementedError(self._pipe_map.__name__)
    
    def _pipe_filter(self, value):
        raise NotImplementedError(self._pipe_filter.__name__)

    def _pipe_reduce(self, value):
        raise NotImplementedError(self._pipe_reduce.__name__)
    
    def _pipe_member(self, value):
        raise NotImplementedError(self._pipe_reduce.__name__)

    def _pipe_zip(self):
        raise NotImplementedError(self._pipe_zip.__name__)
    
    def _pipe_flatten(self):
        raise NotImplementedError(self._pipe_flatten.__name__)
    
    def _pipe_any(self):
        raise NotImplementedError(self._pipe_any.__name__)
    
    def _pipe_each(self, value):
        raise NotImplementedError(self._pipe_each.__name__)
    
    def _pipe_sum(self):
        raise NotImplementedError(self._pipe_sum.__name__)

    def _pipe(self, value):
        raise NotImplementedError(self._pipe.__name__)
    
    # Boolean Logic
    def _or(self, value):
        raise NotImplementedError(self._or.__name__)

    def _and(self, value):
        raise NotImplementedError(self._and.__name__)
    
    def _not(self):
        raise NotImplementedError(self._not.__name__)
    
    # Comparisons
    def _eq(self, value):
        raise NotImplementedError(self._eq.__name__)

    def _neq(self, value):
        raise NotImplementedError(self._neq.__name__)

    def _lt(self, value):
        raise NotImplementedError(self._lt.__name__)

    def _gt(self, value):
        raise NotImplementedError(self._gt.__name__)
    
    def _lte(self, value):
        raise NotImplementedError(self._lte.__name__)
    
    def _gte(self, value):
        raise NotImplementedError(self._gte.__name__)
        
    # Bitwise
    def _bit_not(self):
        raise NotImplementedError(self._bit_not.__name__)

    def _bit_or(self, value):
        raise NotImplementedError(self._bit_or.__name__)

    def _bit_xor(self, value):
        raise NotImplementedError(self._bit_xor.__name__)

    def _bit_and(self, value):
        raise NotImplementedError(self._bit_and.__name__)
    
    def _bit_shr(self, value):
        raise NotImplementedError(self._bit_shr.__name__)
    
    def _bit_shl(self, value):
        raise NotImplementedError(self._bit_shl.__name__)
        
    # Math
    def _add(self, value):
        raise NotImplementedError(self._add.__name__)
    
    def _sub(self, value):
        raise NotImplementedError(self._sub.__name__)
    
    def _mult(self, value):
        raise NotImplementedError(self._mult.__name__)
    
    def _div(self, value):
        raise NotImplementedError(self._div.__name__)

    def _mod(self, value):
        raise NotImplementedError(self._mod.__name__)

    def _pow(self, value):
        raise NotImplementedError(self._pow.__name__)

    # Crement
    def _increment(self):
        raise NotImplementedError(self._increment.__name__)
    
    def _decrement(self):
        raise NotImplementedError(self._decrement.__name__)

    # Primary access
    def _member(self, name):
        raise NotImplementedError(self._member.__name__)
    
    def _index(self, index):
        raise NotImplementedError(self._index.__name__)
    
    def _call(self, args):
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

    def upper(self):
        pass

    def lower(self):
        pass

    def reverse(self):
        pass

    def trim(self, ):
        pass

    def reap(self):
        pass

    def count(self):
        pass
