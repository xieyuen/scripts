from typing import Any

from scripts.constants import string_to as constants


def str2bool(obj: str) -> bool | TypeError | ValueError:
    if not isinstance(obj, str):
        return TypeError('什么叫做 str to bool?')
    if obj.lower() in constants.ALL_TRUE:
        return True
    elif obj.lower() in constants.ALL_FALSE:
        return False
    else:
        return ValueError(f'{obj} 不是有效的 bool 值')


def str2None(obj: str) -> None | ValueError:
    if obj.lower() not in constants.ALL_NULL:
        return ValueError(f'{obj} 不是有效的空值')


def str2pyobj(obj: str) -> Any | ValueError:
    try:
        res = eval(obj)
    except NameError:
        if isinstance(str2bool(obj), bool):
            return str2bool(obj)
        return ValueError(f'{obj} 不是有效的 python 对象')
    except:
        return ValueError(f'{obj} 不是有效的 python 对象')
    else:
        return res
