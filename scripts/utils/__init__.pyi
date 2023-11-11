from typing import Callable, Generator, Tuple, List, Literal

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
