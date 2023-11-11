from numbers import Real
from typing import Literal, TypeVar, Tuple, Set, overload, Iterable, List, Iterator, Never

__DefinedDomains = Literal[
    'R', 'R+', 'R-', 'R*', 'Z', 'Z+', 'Z-', 'Z*',
    'Q', 'Q+', 'Q-', 'Q*', 'N', 'N+', 'N*',
]
__RaiseError = TypeVar('__RaiseError')
__Stats = TypeVar('__Stats')


class Domain:
    class __consts:
        DEFINED_DOMAINS: Tuple[__DefinedDomains]
        inf: float

        class TypeStates:
            DEFINED_DOMAIN: str
            SET: str
            INTERVAL: str
            EMPTY: str

    domain: Tuple[Real, Real] | __DefinedDomains | Set[Real, ...]
    __type: str | __DefinedDomains
    left_closed: bool | __RaiseError[AttributeError]
    right_closed: bool | __RaiseError[AttributeError]

    @overload
    def __init__(self, domain: __DefinedDomains): ...

    @overload
    def __init__(self, domain: Real, *args: Real): ...

    @overload
    def __init__(self, domain: Iterable[Real, ...]): ...

    @overload
    def __init__(
            self,
            interval: List[Real, Real] | Tuple[Real, Real],
            /,
            *,
            left_closed: bool = ...,
            right_closed: bool = ...,
    ): ...

    def __type_check(self) -> None | Never: ...

    def __contains__(self, item: Real) -> bool: ...

    def __repr__(self): ...

    if __type == __consts.TypeStates.SET:
        def __iter__(self) -> Iterator[int]: ...
