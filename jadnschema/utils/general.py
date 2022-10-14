"""
General Utils
"""
import sys

from typing import Any, Callable


def addKey(d: dict, k: str = None) -> Callable:
    """
    Decorator to append a function to a dict, referencing the function name or given key as the key in the dict
    :param d: dict to append the key/func onto
    :param k: key to use on the dict
    :return: original function
    """
    def wrapped(fun: Callable, key: str = k) -> Callable:
        d[key if key else fun.__name__] = fun
        return fun
    return wrapped


def ellipsis_str(val: str, cut: int = 100) -> str:
    """
    Terminate a string larger than 'cut' characters and append an ellipsis
    :param val: string to limit the size of
    :param cut: number of characters to terminate string at
    :return: original string or ellipsis string
    """
    if len(val) > cut:
        return f"{val[:cut]}..."
    return val


def safe_cast(val: Any, to_type: type, default: Any = None) -> Any:
    """
    Cast the given value to the given type safely without an exception being thrown
    :param val: value to cast
    :param to_type: type to cast as
    :param default: default value if casting fails
    :return: cast value or given default/None
    """
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def toStr(s: Any) -> str:
    """
    Convert a given type to a default string
    :param s: item to convert to a string
    :return: converted string
    """
    return s.decode(sys.getdefaultencoding(), 'backslashreplace') if hasattr(s, 'decode') else str(s)


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super().__get__(objtype)

    def __set__(self, obj, value):
        super().__set__(type(obj), value)

    def __delete__(self, obj):
        super().__delete__(type(obj))
