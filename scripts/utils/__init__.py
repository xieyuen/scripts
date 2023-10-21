from typing import Generator, Union, Callable

from scripts.utils import logger, exceptions, randomnum
from scripts.utils.randomnum import str2bool

__all__ = [
    'Mathematics', 'logger', 'exceptions', 'randomnum', 'str2bool'
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
    c: tuple[int, str] = 299792458, 'm/s'

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
