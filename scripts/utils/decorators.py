from types import FunctionType
from typing import Callable, Tuple, Literal, Any, Optional, NoReturn


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

    return wrapper


def print_return_code(callback: Callable) -> Callable:
    """
    Decorator for printing the return code of a function.
    """

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


def run_now(callback: Callable[[...], ...], *args, exc=Exception, **kwargs):
    class Wrapper:
        def __init__(self):
            try:
                self.result = callback(*args, **kwargs)
            except exc as e:
                self.e = e

        @property
        def keyword_arguments(self):
            return kwargs

        @property
        def position_arguments(self):
            return args

        @property
        def arguments(self):
            return self.position_arguments, self.keyword_arguments

        def __repr__(self):
            return self.result

    return Wrapper()


def curry(func: FunctionType) -> Callable:
    """
    Decorator for currying a function.
    """

    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        else:
            return (
                lambda *more_args, **more_kwargs:
                curried(*(args + more_args), **{**kwargs, **more_kwargs})
            )

    return curried
