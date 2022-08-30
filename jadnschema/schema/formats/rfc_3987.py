"""
JADN RFC3987 Formats
"""
import rfc3987

from typing import Optional
from ...utils import addKey

RFC3987_Formats = {}


@addKey(d=RFC3987_Formats, k="iri")
def iri(val: str) -> Optional[Exception]:
    """
    Validate an IRI - RFC 3987
    :param val: IRI instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        return TypeError(f"iri given is not expected string, given {type(val)}")

    try:
        rfc3987.parse(val, rule="IRI")
    except Exception as e:  # pylint: disable=broad-except
        # TODO: change to better exception
        return e


@addKey(d=RFC3987_Formats, k="iri-reference")
def iri_reference(val: str) -> Optional[Exception]:
    """
    Validate an IRI-Reference - RFC 3987
    :param val: IRI-Reference instance to validate
    :return: None or Exception
    """
    if not isinstance(val, str):
        return TypeError(f"iri given is not expected string, given {type(val)}")

    try:
        rfc3987.parse(val, rule="IRI_reference")
    except Exception as e:  # pylint: disable=broad-except
        # TODO: change to better exception
        return e


__all__ = [
    # Format Dict
    "RFC3987_Formats",
    # Format Funcs
    "iri",
    "iri_reference"
]
