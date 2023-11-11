from numbers import Real, Rational
from typing import Iterable, Optional


class Domain:
    class __consts:
        DEFINED_DOMAINS = (  # 定义好的集合
            'R', 'R+', 'R-', 'R*',
            'Z', 'Z+', 'Z-', 'Z*',
            'Q', 'Q+', 'Q-', 'Q*',
            'N', 'N+', 'N*',
        )
        inf = float('inf')  # 无穷大

        class TypeStates:  # 定义类型
            DEFINED_DOMAIN = 'DefinedDomain'
            SET = 'Set'
            INTERVAL = 'Interval'
            EMPTY = 'Empty'

    def __init__(self, domain, *args, left_closed: Optional[bool] = None, right_closed: Optional[bool] = None):
        """定义域"""
        if domain is None or (isinstance(domain, str) and domain.title() == self.__consts.TypeStates.EMPTY):
            # 空定义域
            self.__type = self.__consts.TypeStates.EMPTY
            return
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
            if domain[0] == self.__consts.inf:
                if domain[1] == self.__consts.inf:
                    self.__type = self.__consts.TypeStates.DEFINED_DOMAIN
                    self.domain = 'R'
                    return
                elif not self.right_closed and domain[1] == 0:
                    self.__type = self.__consts.TypeStates.DEFINED_DOMAIN
                    self.domain = 'R-'
                    return
            elif not self.left_closed and domain[0] == 0 and domain[1] == self.__consts.inf:
                self.__type = self.__consts.TypeStates.DEFINED_DOMAIN
                self.domain = 'R+'
                return
            self.domain = domain[0], domain[1]
            self.__type_check()
            return
        if isinstance(domain, Iterable):
            # Iterable 看作集合
            # dict 的 key 和 value 都算作定义域内的值
            self.domain = (
                set(domain.keys()) & set(domain.values())
                if isinstance(domain, dict)
                else set(domain)
            )
            self.__type = self.__consts.TypeStates.SET
            self.__type_check()
            return
        if all(isinstance(item, Real) for item in (domain, *args)):
            self.domain = {item for item in (domain, *args)}
            self.__type = self.__consts.TypeStates.SET

    def __type_check(self):
        if self.__type == self.__consts.TypeStates.SET:
            if not all(isinstance(i, Real) for i in self.domain):
                raise ValueError('Domain must be a set of real number')
            self.__iter__ = self.domain.__iter__()
            self.__contains__ = self.domain.__contains__
            return
        if self.__type == self.__consts.TypeStates.INTERVAL:
            if any(not isinstance(config, bool) for config in (self.left_closed, self.right_closed)):
                raise TypeError("Interval's closed config only allows boolean")
            if not all(isinstance(i, Real) for i in self.domain):
                raise TypeError('Interval only allows real number')

    def __contains__(self, item: Real):
        if self.__type == self.__consts.TypeStates.EMPTY:
            return False
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
        if self.__type == self.__consts.TypeStates.EMPTY:
            return 'Domain(Empty)'
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
