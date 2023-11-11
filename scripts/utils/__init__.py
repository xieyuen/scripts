import functools
from numbers import Real, Rational
from typing import Generator, Callable, Iterable

from scripts.utils import exceptions
from scripts.utils.jsobj import JSObject
from scripts.utils.logger import logger
from scripts.utils.string_to import str2bool

__all__ = [
    'Mathematics', 'logger', 'exceptions', 'str2bool',
    'JSObject',
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


class Domain:
    class __consts:
        DEFINED_DOMAINS = (
            'R', 'R+', 'R-', 'R*',
            'Z', 'Z+', 'Z-', 'Z*',
            'Q', 'Q+', 'Q-', 'Q*',
            'N', 'N+', 'N*',
        )
        inf = float('inf')

        class TypeStates:
            DEFINED_DOMAIN = 'DefinedDomain'
            SET = 'Set'
            INTERVAL = 'Interval'

    def __init__(self, domain, *args, **kwargs):
        """定义域"""
        if domain in self.__consts.DEFINED_DOMAINS:
            # 定义好的集合(`R`, `Q`, `Z`, `N` 等)
            self.__type = self.__consts.TypeStates.DEFINED_DOMAIN
            self.domain = domain
            return
        if isinstance(domain, (list, tuple)):
            if len(domain) != 2:  # 两个的认为是区间，否则认为是集合
                self.domain = set(domain)
                self.__type = self.__consts.TypeStates.SET
                self.__type_check()
                return
            self.__type = self.__consts.TypeStates.INTERVAL
            self.left_closed = kwargs.get('left_closed', isinstance(domain, list))
            self.right_closed = kwargs.get('right_closed', isinstance(domain, list))
            self.domain = *domain,
            self.__type_check()
            return
        if isinstance(domain, Iterable):
            # 这些 Iterable 看作集合
            # dict 的 key 和 value 都算作定义域内的值
            self.domain = (
                set(domain.keys()) & set(domain.values())
                if isinstance(domain, dict)
                else set(domain)
            )
            self.__type = self.__consts.TypeStates.SET
            self.__type_check()
            return
        if all(isinstance(i, Real) for i in (domain, *args)):
            self.domain = {domain, *args}
            self.__type = self.__consts.TypeStates.SET

    def __type_check(self):
        if self.__type == self.__consts.TypeStates.SET:
            if not all(isinstance(i, Real) for i in self.domain):
                raise ValueError('Domain must be a set of real number')
        if self.__type == self.__consts.TypeStates.INTERVAL:
            if not all(isinstance(i, Real) for i in self.domain):
                raise TypeError('Interval only allows real number')

    def __contains__(self, item: Real):
        if self.__type == self.__consts.TypeStates.SET:
            # set 直接 `in`
            return item in self.domain
        if self.__type == self.__consts.TypeStates.DEFINED_DOMAIN:
            # 常用的集合
            res = {
                'R': isinstance(item, Real),
                'Z': isinstance(item, int),
                'Q': isinstance(item, Rational),
                'N': isinstance(item, int) and item >= 0,
            }
            res['R*'] = res['R'] and item != 0
            res['Q*'] = res['Q'] and item != 0
            res['Z*'] = res['Z'] and item != 0

            res['R+'] = res['R*'] and item > 0
            res['R-'] = res['R*'] and item < 0

            res['Q+'] = res['Q*'] and item > 0
            res['Q-'] = res['Q*'] and item < 0

            res['Z+'] = res['Z*'] and item > 0
            res['Z-'] = res['Z*'] and item < 0

            res['N+'] = res['N*'] = res['Z+']

            return res[self.domain]
        if self.__type == self.__consts.TypeStates.INTERVAL:
            # 区间
            left, right = self.domain
            # 左无穷
            if left == self.__consts.inf:
                if right == self.__consts.inf:
                    return isinstance(item, Real)
                return (
                    item <= right
                    if self.right_closed
                    else item < right
                )
            # 右无穷
            if right == self.__consts.inf:
                return (
                    left <= item
                    if self.left_closed
                    else left < item
                )
            return (
                    (
                        left <= item
                        if self.left_closed
                        else left < item
                    ) and (
                        item <= right
                        if self.right_closed
                        else item < right
                    )
            )

    def __repr__(self):
        if self.__type in (
                self.__consts.TypeStates.SET,
                self.__consts.TypeStates.DEFINED_DOMAIN,
        ):
            return f'Domain({self.domain})'
        if self.__type == self.__consts.TypeStates.INTERVAL:
            return (
                    'Domain'
                    + ('[' if self.left_closed else '(')
                    + f'{self.domain[0]}, {self.domain[1]}'
                    + (']' if self.right_closed else ')')
            )


if __name__ == '__main__':
    print(f'{isinstance(Domain(1,2,3,4,6,3,7,1), Iterable) = }')
    print(Domain([1, 2]).left_closed)
