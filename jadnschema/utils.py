from typing import Callable


def addKey(d: dict, k: str = None) -> Callable:
    def wrapped(fun: Callable, key: str = k) -> Callable:
        d[key if key else fun.__name__] = fun
        return fun
    return wrapped


def ellipsis_str(val: str, cut: int = 100) -> str:
    if len(val)> cut:
        return f"{val[:cut]}..."
    return val


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))