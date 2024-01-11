from enum import auto
from numbers import Real, Rational
from typing import Iterable, Optional, Set, Tuple, Literal

__all__ = ['Domain']


class Consts:
    DEFINED_DOMAINS = (  # 定义好的集合
        'R', 'R+', 'R-', 'R*',
        'Z', 'Z+', 'Z-', 'Z*',
        'Q', 'Q+', 'Q-', 'Q*',
        'N', 'N+', 'N*',
    )
    inf = float('inf')  # 无穷大


class TypeStates:  # 定义类型
    DEFINED_DOMAIN = auto()
    SET = auto()
    INTERVAL = auto()
    EMPTY = auto()


class Domain:
    __type: auto
    __domain: (
        Set[Real, ...] | Tuple[Real, Real]
        | Literal[
            'R', 'R+', 'R-', 'R*',
            'Z', 'Z+', 'Z-', 'Z*',
            'Q', 'Q+', 'Q-', 'Q*',
            'N', 'N+', 'N*', 'Empty'
        ]
    )

    def __init__(self, domain=None, *args, left_closed: Optional[bool] = None, right_closed: Optional[bool] = None):
        """定义域"""
        if domain is None:
            # 空定义域
            self.__type = TypeStates.EMPTY
            self.__domain = 'Empty'
            return
        if domain in Consts.DEFINED_DOMAINS:
            # 定义好的集合(`R`, `Q`, `Z`, `N` 等)
            self.__type = TypeStates.DEFINED_DOMAIN
            self.__domain = domain
            return
        while isinstance(domain, (list, tuple)):
            if len(domain) != 2:  # 两个的认为是区间，否则认为是集合，在下边的 Iterable case 处理
                break
            self.__type = TypeStates.INTERVAL
            # 是否闭区间
            self.left_closed = (
                left_closed
                if left_closed is not None
                else isinstance(domain, list)
            )
            self.right_closed = (
                right_closed
                if right_closed is not None
                else isinstance(domain, list)
            )
            # 有些是可以换成R+R*等等的
            if domain[0] == Consts.inf:
                if domain[1] == Consts.inf:
                    self.__type = TypeStates.DEFINED_DOMAIN
                    self.__domain = 'R'
                    return
                elif not self.right_closed and domain[1] == 0:
                    self.__type = TypeStates.DEFINED_DOMAIN
                    self.__domain = 'R-'
                    return
            elif not self.left_closed and domain[0] == 0 and domain[1] == Consts.inf:
                self.__type = TypeStates.DEFINED_DOMAIN
                self.__domain = 'R+'
                return
            self.__domain = domain[0], domain[1]
            self.__type_check()
            return
        if isinstance(domain, Iterable):
            # Iterable 看作集合
            # dict 的 key 和 value 都算作定义域内的值
            self.__domain = (
                set(domain.keys()) & set(domain.values())
                if isinstance(domain, dict)
                else set(i for i in domain if isinstance(i, Real))
            )
            self.__type = TypeStates.SET
            self.__type_check()
            return
        if all(isinstance(item, Real) for item in (domain, *args)):
            self.__domain = {item for item in (domain, *args)}
            self.__type = TypeStates.SET

    def __type_check(self):
        if self.__type == TypeStates.SET:
            if not all(isinstance(i, Real) for i in self.__domain):
                raise ValueError('Domain must be a set of real number')
            self.__iter__ = self.__domain.__iter__()
            self.__contains__ = self.__domain.__contains__
            return
        if self.__type == TypeStates.INTERVAL:
            if any(not isinstance(config, bool) for config in (self.left_closed, self.right_closed)):
                raise TypeError("Closed configurations of interval only allows boolean")
            if not all(isinstance(i, Real) for i in self.__domain):
                raise TypeError('Interval only allows real number')

    def __contains__(self, item: Real):
        if self.__type == TypeStates.EMPTY:
            return False
        if self.__type == TypeStates.DEFINED_DOMAIN:
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

            return res[self.__domain]
        if self.__type == TypeStates.INTERVAL:
            # 区间
            left, right = self.__domain
            # 左无穷
            if left == Consts.inf:
                if right == Consts.inf:
                    return isinstance(item, Real)
                return (
                    item <= right
                    if self.right_closed
                    else item < right
                )
            # 右无穷
            if right == Consts.inf:
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
        if self.__type == TypeStates.EMPTY:
            return 'Domain(Empty)'
        if self.__type in (
                TypeStates.SET,
                TypeStates.DEFINED_DOMAIN,
        ):
            return f'Domain({self.__domain})'
        if self.__type == TypeStates.INTERVAL:
            return (
                    'Domain'
                    + ('[' if self.left_closed else '(')
                    + f'{self.__domain[0]}, {self.__domain[1]}'
                    + (']' if self.right_closed else ')')
            )
