"""
JADN to JADN
"""
from typing import Union
from .baseWriter import BaseWriter
from ..enums import CommentLevels
from ...schema import Schema
__pdoc__ = {
    "JADNtoJADN.format": "File extension of the given format",
    "JADNtoJADN.escape_chars": "Characters that are not supported in the schema format and need to be removed/escaped",
    "JADNtoJADN.comment_multi": "Multiline comment characters; Tuple[START_CHAR, END_CHAR]",
    "JADNtoJADN.comment_single": "Single line comment character",
}


# Conversion Class
class JADNtoJADN(BaseWriter):  # pylint: disable=abstract-method
    format = "jadn"

    def dumps(self, **kwargs) -> str:
        """
        Converts the JADN schema to JADN
        :return: JADN schema
        """
        return self._schema.dumps()  # strip=self._comm == CommentLevels.NONE)


# Writer Functions
def jadn_dump(schema: Union[str, dict, Schema], fname: str, source: str = "", comm: CommentLevels = CommentLevels.ALL, **kwargs) -> None:
    """
    Convert the JADN schema to JADN and write it to the given file
    :param schema: Schema to convert
    :param fname: schema file to write
    :param source: source information
    :param comm: comment level
    :param kwargs: key/value args for the conversion
    """
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoJADN(schema, comm).dump(fname, source, **kwargs)


def jadn_dumps(schema: Union[str, dict, Schema], comm: CommentLevels = CommentLevels.ALL, **kwargs) -> str:
    """
    Convert the JADN schema to JADN
    :param schema: Schema to convert
    :param comm: comment level
    :param kwargs: key/value args for the conversion
    :return: JADN schema string
    """
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoJADN(schema, comm).dumps(**kwargs)
