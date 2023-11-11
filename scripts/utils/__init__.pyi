from numbers import Real

from typing import Callable, Generator, Tuple, List, overload, Literal, Set, NoReturn, Iterable, TypeVar

RaiseError = TypeVar('RaiseError')
Stats = TypeVar('Stats')
__all__: List


class Mathematics:
    pi: str
    e: str
    i: complex
    inf: float
    infinity: float
    nan: float
    NaN: float
    tao: str
    phi: str
    g: Tuple[str, Literal['N/kg']]
    c: Tuple[int, Literal['m/s']]

    @staticmethod
    def sumG(func: Callable, start: int, end: int, *args, **kwargs) -> Generator: ...

    @staticmethod
    def sum(func: Callable, start: int, end: int, *args, **kwargs) -> int | float: ...

    @classmethod
    def C(cls, n: int, m: int) -> int: ...

    @classmethod
    def C2(cls, n: int, m: int) -> int: ...

    @classmethod
    def factorial(cls, n): ...


DefinedDomains = Literal[
    'R', 'R+', 'R-', 'R*', 'Z', 'Z+', 'Z-', 'Z*',
    'Q', 'Q+', 'Q-', 'Q*', 'N', 'N+', 'N*',
]


class Domain:
    class __consts:
        DEFINED_DOMAINS: Tuple[DefinedDomains]
        inf: float

        class TypeStates:
            DEFINED_DOMAIN: str
            SET: str
            INTERVAL: str

    domain: Tuple[Real, Real] | DefinedDomains | Set[Real]
    __type: Stats[__consts.TypeStates]
    left_closed: bool | RaiseError[AttributeError]
    right_closed: bool | RaiseError[AttributeError]

    @overload
    def __init__(self, domain: DefinedDomains): ...

    @overload
    def __init__(self, domain: Real, *args: Real): ...

    @overload
    def __init__(self, domain: Iterable[Real]): ...

    @overload
    def __init__(
            self,
            interval: List[Real, Real] | Tuple[Real, Real],
            /, *,
            left_closed: bool = ...,
            right_closed: bool = ...,
    ): ...

    def __type_check(self) -> None | NoReturn: ...

    def __contains__(self, item: Real) -> bool: ...

    def __repr__(self): ...
