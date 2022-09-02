from typing import Any, Callable, Type


def addKey(d: dict, k: str = None) -> Callable:
    def wrapped(fun: Callable, key: str = k) -> Callable:
        d[key if key else fun.__name__] = fun
        return fun
    return wrapped


def ellipsis_str(val: str, cut: int = 100) -> str:
    if len(val)> cut:
        return f"{val[:cut]}..."
    return val


def safe_cast(val: Any, to_type: Type, default: Any = None) -> Any:
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


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return super().__get__(objtype)

    def __set__(self, obj, value):
        super().__set__(type(obj), value)

    def __delete__(self, obj):
        super().__delete__(type(obj))
