from typing import Any, NoReturn

from scripts.constants import string_to as constants


def str2bool(obj: str) -> bool | NoReturn:
    if not isinstance(obj, str):
        assert False, '什么叫做 str to bool?'
    if obj.lower() in constants.ALL_TRUE:
        return True
    elif obj.lower() in constants.ALL_FALSE:
        return False
    else:
        assert False, f'{obj} 不是有效的 bool 值'


def str2None(obj: str) -> None | NoReturn:
    if obj.lower() not in constants.ALL_NULL:
        assert False, f'{obj} 不是有效的空值'


def str2pyobj(obj: str) -> Any | ValueError:
    try:
        res = eval(obj)
    except NameError:
        if isinstance(str2bool(obj), bool):
            return str2bool(obj)
        raise ValueError(f'{obj} 不是有效的 python 对象')
    except:
        raise ValueError(f'{obj} 不是有效的 python 对象')
    else:
        return res
