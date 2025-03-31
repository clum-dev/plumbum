from typing import Any, Union, TypeAlias
from typing_extensions import Self, Type
from parser import *

ANY_PRIM = Union[int, float, bool, str, None]

    
class Data:

    isConst:bool
    isCallable:bool
    isIterable:bool
    isIndexable:bool

    value:Any
    dtype:Type
    parent:Self|None
    name:str
    level:int

    def __init__(self, value:Any, dtype:Type, parent:Self|None, name:str|None=None) -> None:

        self.value = value
        self.dtype = dtype
        self.parent = parent
        self.name = name

        self.isConst = False
        self.isCallable = False
        self.isIterable = False
        self.isIndexable = False

        if parent is None:
            self.level = 0
        else:
            self.level = parent.level + 1

    def __str__(self) -> str:
        if isinstance(self.value, Tree):
            return f'{self.name}: {repr(self.value.get_leftmost())} ({self.dtype})'

        return f'{self.name}: {repr(self.value)} ({self.dtype})'

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

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)

    def autocast(self, value:Any):
        if self.dtype is not Any:
            return self.dtype(value)
        return value

    # Assignment
    def _assign(self, value:Data):
        assert not self.isConst
        self.value = self.autocast(value.value)

    def _assign_add(self, value:Data):
        assert not self.isConst
        self.value += self.autocast(value.value)

    def _assign_sub(self, value:Data):
        assert not self.isConst
        self.value -= self.autocast(value.value)

    def _assign_mult(self, value:Data):
        assert not self.isConst
        self.value *= self.autocast(value.value)

    def _assign_div(self, value:Data):
        assert not self.isConst
        self.value /= self.autocast(value.value)

    def _assign_mod(self, value:Data):
        assert not self.isConst
        self.value %= self.autocast(value.value)

    # Pipes
    def _pipe(self, value:Data) -> Data:
        self._assign(value)
        return self

    # Comparisons
    def _eq(self, value:Data) -> Data:
        return DBool(self.value == self.autocast(value.value), dtype=bool, parent=self.parent)

    def _neq(self, value:Data) -> Data:
        return DBool(self.value != self.autocast(value.value), dtype=bool, parent=self.parent)
    
    def _lt(self, value:Data) -> Data:
        return DBool(self.value < self.autocast(value.value), dtype=bool, parent=self.parent)

    def _gt(self, value:Data) -> Data:
        return DBool(self.value > self.autocast(value.value), dtype=bool, parent=self.parent)

    def _lte(self, value:Data) -> Data:
        return DBool(self.value <= self.autocast(value.value), dtype=bool, parent=self.parent)

    def _gte(self, value:Data) -> Data:
        return DBool(self.value >= self.autocast(value.value), dtype=bool, parent=self.parent)
    
    # Bitwise
    def _bit_not(self) -> Data:
        return self.autocast(~self.value, self.dtype)
    
    def _bit_or(self, value:Data) -> Data:
        return self.autocast(self.value | value.value, self.dtype, parent=self.parent)
    
    def _bit_xor(self, value:Data) -> Data:
        return self.autocast(self.value ^ value.value, self.dtype, parent=self.parent)
    
    def _bit_and(self, value:Data) -> Data:
        return self.autocast(self.value & value.value, self.dtype, parent=self.parent)

    def _bit_shr(self, value:Data) -> Data:
        return self.autocast(self.value >> value.value, self.dtype, parent=self.parent)

    def _bit_shl(self, value:Data) -> Data:
        return self.autocast(self.value << value.value, self.dtype, parent=self.parent)
    
    # Math
    def _add(self, value:Data) -> Data:
        return self.autocast(self.value + value.value, self.dtype, parent=self.parent)
    
    def _sub(self, value:Data) -> Data:
        return self.autocast(self.value - value.value, self.dtype, parent=self.parent)

    def _mult(self, value:Data) -> Data:
        return self.autocast(self.value * value.value, self.dtype, parent=self.parent)
    
    def _div(self, value:Data) -> Data:
        return self.autocast(self.value / value.value, self.dtype, parent=self.parent)

    def _mod(self, value:Data) -> Data:
        return self.autocast(self.value % value.value, self.dtype, parent=self.parent)
    
    def _pow(self, value:Data) -> Data:
        return self.autocast(self.value % value.value, self.dtype, parent=self.parent)

    def _posate(self) -> Data:
        return self.autocast(+self.value, self.dtype, parent=self.parent)

    def _posate(self) -> Data:
        return self.autocast(-self.value, self.dtype, parent=self.parent)

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

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)


class DInt(DPrim):

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)


class DFloat(DPrim):

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)


class DBool(DPrim):

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)


class DNull(DPrim):

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)


class DString(Data):

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)
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
    
    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)
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

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)


class InstType(Enum):
    
    RET   = auto()
    CALL  = auto()
    LOADV = auto()
    LOADN = auto()
    STORE = auto()
    BINOP = auto()
    UNOP  = auto()

    PIPE  = auto()

    BUILD_STR = auto()
    BUILD_RANGE = auto()
    BUILD_SEQ = auto()
    BUILD_DEFAULTS = auto()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()


class Inst:
    
    name:InstType
    arg:TokType|Data

    def __init__(self, name:InstType, arg:TokType|Data|None=None) -> None:
        assert isinstance(name, InstType)
        self.name = name
        self.arg = arg

    def __str__(self) -> str:
        out = str(self.name)
        if self.arg is not None:
            out += f' ({self.arg})'
        return out

    def __repr__(self) -> str:
        return self.__str__()


class DScope(Data):

    d_locals:dict[str, Data]            # Local data lookup 
    insts:list[Inst]                    # Ordered instruction list

    call_args:list[str]                 # Lookup names for args
    call_non_defaults:int               # Number of non-default values
    call_store_mode:Any                 # e.g. |> for funcs (if used) - default |:

    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)
        
        self.isCallable = True

        self.d_locals = {}
        self.insts = []

        self.call_args = []
        self.call_non_defaults = 0
        self.call_store_mode = TokType.PIPE_PAIR

        self.value = DNull(None, None, self, name='_ret')    # default returns null

    def __str__(self):
        indent = '  ' * self.level
        indent2 = '  ' * (self.level + 1)

        out = super().__str__()
        out += f'\n{indent}Locals:\n'
        if len(self.d_locals.items()) == 0:
            out += f'{indent2}[Empty]'
        out += '\n'.join([f'{indent2}[{k}]\t{v}' for k,v in self.d_locals.items()])
        
        out += f'\n{indent}Insts:\n'
        if len(self.insts) == 0:
            out += f'{indent2}[Empty]'
        out += '\n'.join([f'{indent2}{i}' for i in self.insts])

        return out

    def lookup_local(self, name:str) -> Data|None:
        res = self.d_locals.get(name)
        if res is not None:
            return res
        elif self.parent is not None:
            return self.parent.lookup_local(name)
        return None
    
    def add_new_local(self, name:str):
        assert name not in self.d_locals.keys()
        self.d_locals[name] = DAny(None, Any, self, name=name)


class DFunc(DScope):
    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)

    def __str__(self):
        out = super().__str__()
        self.dtype:TParam
        indent = '  ' * self.level
        out += f'\n{indent}Ret: {self.dtype}'
        return out


class DStruct(DScope):
    def __init__(self, value, dtype, parent, name=None):
        super().__init__(value, dtype, parent, name)