import functools
from typing import Generator, Callable, Iterable

from scripts.utils import exceptions
from scripts.utils.jsobj import JSObject
from scripts.utils.logger import logger
from scripts.utils.string_to import str2bool

__all__ = [
    'Mathematics', 'logger', 'exceptions', 'str2bool',
    'JSObject', 'dedup',
]


class Mathematics:
    pi = '3.141592653589793'
    e = '2.718281828459045'
    i = 1j
    inf = infinity = float('inf')
    nan = NaN = float('nan')
    tao = '6.283185307179586'
    phi = '1.618033988749894'
    g = '9.80665', 'N/kg'
    c = 2_9979_2458, 'm/s'

    @staticmethod
    def sumG(
            func: Callable,
            start: int,
            end: int,
            *args, **kwargs
    ) -> Generator:
        for i in range(start, end):
            yield func(i, *args, **kwargs)

    @staticmethod
    def sum(
            func: Callable,
            start: int,
            end: int,
            *args, **kwargs
    ) -> int | float:
        return sum(Mathematics.sumG(func, start, end, *args, **kwargs))

    @classmethod
    def C(cls, n: int, m: int) -> int:
        return cls.factorial(n) / (
                cls.factorial(m) * cls.factorial(n - m)
        )

    @classmethod
    def C2(cls, n: int, m: int) -> int:
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


def dedup(li: Iterable) -> Generator:
    inLi = []
    for index, item in enumerate(li):
        if item not in inLi:
            inLi.append(item)
            yield item
