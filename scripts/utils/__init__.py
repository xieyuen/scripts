import functools
from typing import Generator, Union, Callable

from scripts.utils import exceptions
from scripts.utils.logger import logger
from scripts.utils.randomnum import str2bool
from scripts.utils.jsobj import JSObject

__all__ = [
    'Mathematics', 'logger', 'exceptions', 'str2bool',
    'JSObject',
]


class Mathematics:
    pi: str = '3.141592653589793'
    e: str = '2.718281828459045'
    i: complex = 1j
    inf = infinity = float('inf')  # type: float
    nan = NaN = float('nan')  # type: float
    tao: str = '6.283185307179586'
    phi: str = '1.618033988749894'
    g: tuple[str] = '9.80665', 'N/kg'
    c: tuple[int, str] = 2_9979_2458, 'm/s'

    @staticmethod
    def sumG(
            func: Callable,
            _from: int,
            _to: int,
            *args, **kwargs
    ) -> Generator:
        for i in range(_from, _to):
            yield func(i, *args, **kwargs)

    @classmethod
    def sum(cls,
            func: Callable,
            _from: int,
            _to: int,
            *args, **kwargs
            ) -> Union[int, float]:
        return sum(cls.sumG(func, _from, _to, *args, **kwargs))

    @classmethod
    def C(cls, n, m):
        return cls.factorial(n) / (
            cls.factorial(m) * cls.factorial(n - m)
        )

    @classmethod
    def C2(cls, n, m):
        if m == 0:
            return 1
        if m == 1:
            return n
        return cls.C2(n - 1, m - 1) + cls.C2(n - 1, m)

    @classmethod
    @functools.lru_cache
    def factorial(cls, n):
        if n == 0:
            return 1
        if n == 1:
            return 1
        return n * cls.factorial(n - 1)
