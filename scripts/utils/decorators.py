from types import FunctionType, MethodType, BuiltinFunctionType
from typing import Callable, Tuple, Literal, Any, Optional, NoReturn

__all__ = [
    'print_return', 'add_return_code', 'print_return_code',
    'curry', 'print_arguments',
]


def curry(callback: Callable | FunctionType | MethodType | BuiltinFunctionType) -> Callable:
    """
    Decorator for currying a function.
    """

    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= callback.__code__.co_argcount:
            return callback(*args, **kwargs)
        # else:
        return (
            lambda *more_args, **more_kwargs:
            curried(*args, *more_args, **kwargs, **more_kwargs)
        )

    return curried


def print_return(callback: Callable) -> Callable:
    """
    Decorator for printing the return value of a function.
    """

    def wrapper(*args, **kwargs):
        result = callback(*args, **kwargs)
        print(f'Callable: {callback.__name__} returns {result}')
        return result

    return wrapper


def add_return_code(callback: Callable) -> Callable[[...], Tuple[Literal[0, 1], Any]]:
    """
    Decorator for printing the return code of a function.
    if an exception(as e) is raised, it will return (1, e)
    if not, it will return (0, result)
    """

    def wrapper(*args, **kwargs) -> Tuple[Literal[0, 1], Any]:
        try:
            result = callback(*args, **kwargs)
        except Exception as e:
            return 1, e
        else:
            return 0, result

    wrapper.has_return_code = True
    return wrapper


def print_return_code(callback: Callable) -> Callable:
    """
    Decorator for printing the return code of a function.
    """
    if hasattr(callback, 'has_return_code') and callback.has_return_code:
        def _res(*args, **kwargs):
            code, result = callback(*args, **kwargs)
            print(f'Callable: {callback.__name__} returns with code {code}')
            return result

        return _res

    # else:
    class Wrapper:
        def __init__(self, __call):
            self.__e = None  # type: Optional[Exception]
            self.__callback = __call

        def __call__(self, *args, **kwargs):
            try:
                result = self.__callback(*args, **kwargs)
                code = 0
            except Exception as e:
                print(f'Callable: {self.__callback.__name__} raises an exception.')
                code = 1
                self.__e = e
            print(f'Return code of callable: {self.__callback.__name__} is {code}')
            return result

        def get_exception(self) -> Exception | NoReturn:
            if self.__e is None:
                raise RuntimeError('No Exception is raised.')
            return self.__e

    return Wrapper(callback)


def print_arguments(callback: Callable) -> Callable:
    """
    Decorator for printing the arguments of a callable.
    """

    def wrapper(*args, **kwargs):
        print(f'Callable: {callback.__name__} is called with arguments: {args}, {kwargs}')
        return callback(*args, **kwargs)

    return wrapper
