"""
JADN RFC3339 Formats
"""
import strict_rfc3339

from datetime import datetime, date, time
from ... import utils

RFC3339_Formats = {}


@utils.addKey(d=RFC3339_Formats, k="date-time")
def datetime(val: str) -> datetime:
    """
    Validate a datetime - RFC 3339 § 5.6
    :param val: DateTime instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"datetime given is not expected string, given {type(val)}")

    try:
        strict_rfc3339.validate_rfc3339(val)
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err
    return datetime.fromisoformat(val)


@utils.addKey(d=RFC3339_Formats)
def date(val: str) -> date:
    """
    Validate a date - RFC 3339 § 5.6
    :param val: Date instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"date given is not expected string, given {type(val)}")
    try:
        d = datetime(f"{val}T00:00:00")
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err
    return d.date()


@utils.addKey(d=RFC3339_Formats)
def time(val: str) -> time:
    """
    Validate a time - RFC 3339 § 5.6
    :param val: Time instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        raise TypeError(f"time given is not expected string, given {type(val)}")
    try:
        d = datetime(f"1970-01-01T{val}")
    except Exception as err:  # pylint: disable=broad-except
        # TODO: change to better exception
        raise ValueError from err
    return d.time()


__all__ = [
    # Format Dict
    "RFC3339_Formats",
    # Format Funcs
    "date",
    "datetime",
    "time"
]
