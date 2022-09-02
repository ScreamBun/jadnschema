"""
JADN to JADN
"""
from typing import Union
from .baseWriter import WriterBase
from ..enums import CommentLevels
from ...schema import Schema


# Conversion Class
class JADNtoJADN(WriterBase):
    format = "jadn"

    def dumps(self, **kwargs) -> str:
        """
        Converts the JADN schema to JADN
        :return: JADN schema
        """
        return self._schema.dumps()  # strip=self._comm == CommentLevels.NONE)


# Writer Functions
def jadn_dump(schema: Union[str, dict, Schema], fname: str, source: str = "", comm: CommentLevels = CommentLevels.ALL, **kwargs):
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoJADN(schema, comm).dump(fname, source, **kwargs)


def jadn_dumps(schema: Union[str, dict, Schema], comm: CommentLevels = CommentLevels.ALL, **kwargs):
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoJADN(schema, comm).dumps(**kwargs)
