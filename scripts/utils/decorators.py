from typing import Callable


def print_return(callback: Callable) -> Callable:
    """
    Decorator for printing the return value of a function.
    """

    def wrapper(*args, **kwargs):
        result = callback(*args, **kwargs)
        print(f'Callable: {callback.__name__} returns {result}')
        return result

    return wrapper


def add_return_code(callback: Callable) -> Callable:
    """
    Decorator for printing the return code of a function.
    if an exception(as e) is raised, it will return (1, e)
    if not, it will return (0, result)
    """

    def wrapper(*args, **kwargs):
        try:
            result = callback(*args, **kwargs)
        except Exception as e:
            return 1, e
        else:
            return 0, result

    return wrapper
