"""
Base Schema Reader
"""
from io import BytesIO, StringIO
from pathlib import Path
from typing import Union
from ....schema import Schema
__pdoc__ = {
    "BaseReader.format": "File extension of the given format"
}


class BaseReader:
    format: str = None
    # Helpers
    _schema: Union[BytesIO, StringIO]

    @classmethod
    def load(cls, fname: Union[str, Path], **kwargs) -> "BaseReader":
        """
        Load a schema for parsing from a file
        :param fname: file to read from
        :param kwargs: key/value args to use for loading
        :return: BaseReader instance
        """
        inst = cls()
        kwargs.setdefault("mode", "r")
        kwargs.setdefault("encoding", "utf-8")
        cls_io = StringIO if kwargs["mode"] == "r" else BytesIO
        if isinstance(fname, str):
            with open(fname, mode=kwargs["mode"], encoding=kwargs["encoding"]) as f:
                inst._schema = cls_io(f.read())
        elif isinstance(fname, Path):
            with fname.open(mode=kwargs["mode"], encoding=kwargs["encoding"]) as f:
                inst._schema = cls_io(f.read())
        else:
            raise TypeError("Unknown type given for `fname`")
        return inst

    @classmethod
    def loads(cls, schema: Union[bytes, bytearray, str], **kwargs) -> "BaseReader":
        """
        Load a schema for parsing from a byte string or string
        :param schema: value to read
        :param kwargs: key/value args to use for loading
        :return: BaseReader instance
        """
        inst = cls()
        if isinstance(schema, (bytes, bytearray)):
            inst._schema = BytesIO(schema)
        if isinstance(schema, str):
            inst._schema = StringIO(schema)
        else:
            raise TypeError("Unknown type given for `fname`")
        return inst

    def parse_schema(self) -> Schema:
        """
        Parse the schema into JADN format
        """
        raise NotImplementedError
