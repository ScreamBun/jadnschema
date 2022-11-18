"""
JADN to JADN
"""
from pathlib import Path
from typing import Union
from .baseReader import BaseReader
from ..helpers import register_reader
from ....schema import Schema
__pdoc__ = {
    "JADNtoJADN.format": "File extension of the given format"
}


# Conversion Class
@register_reader
class JADNtoJADN(BaseReader):  # pylint: disable=abstract-method
    format = "jadn"

    def parse_schema(self, **kwargs) -> Schema:
        return Schema.load(self._schema)


# Writer Functions
def jadn_load(schema: Union[str, Path], **kwargs) -> Schema:
    """
    Convert the JADN schema to JADN and write it to the given file
    :param schema: Schema to convert
    :param kwargs: key/value args for the conversion
    """
    return JADNtoJADN.load(schema).parse_schema(**kwargs)


def jadn_loads(schema: Union[bytes, bytearray, str], **kwargs) -> Schema:
    """
    Convert the JADN schema to JADN
    :param schema: Schema to convert
    :param kwargs: key/value args for the conversion
    :return: JADN schema string
    """
    return JADNtoJADN.loads(schema).parse_schema(**kwargs)
