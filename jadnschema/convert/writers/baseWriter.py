"""
Base JADN Schema Writer
"""
import re

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, NoReturn, Tuple, Union
from ..enums import CommentLevels
from ...schema import Schema
from ...schema.definitions import Definition


class WriterBase:
    format: str = None
    escape_chars: Tuple[str, ...] = (" ", )
    comment_multi: Tuple[str, str] = ("<!--", "-->")
    comment_single: str = ""
    # Helper Vars
    _schema: Schema
    _exports: List[str]
    _comm: CommentLevels
    _customFields = Dict[str, str]
    # Non Override
    _definition_order: Tuple[str, ...] = ()
    _indent: str = " " * 2
    _title_overrides: Dict[str, str] = {}

    def __init__(self, schema: Union[dict, str, Schema], comm: str = CommentLevels.ALL):
        if isinstance(schema, Schema):
            self._schema = schema
        elif isinstance(schema, dict):
            self._schema = Schema.parse_obj(schema)
        elif Path(schema).exists():
            self._schema = Schema.parse_file(schema)
        else:
            self._schema = Schema.parse_raw(schema)
        self._exports = getattr(self._schema.info, "exports", [])
        self._comm = comm if comm in CommentLevels else CommentLevels.ALL
        self._customFields = {t.name: t.data_type for t in self._schema.types.values()}

    def dump(self, fname: Union[str, Path], source: str = None, **kwargs) -> NoReturn:
        output = fname if fname.endswith(self.format) else f"{fname}.{self.format}"
        with open(output, "w", encoding="UTF-8") as f:
            if source:
                prefix, suffix = self.comment_multi
                f.write(f"{prefix} Generated from {source}, {datetime.ctime(datetime.now())} {suffix}\n".strip())
            f.write(self.dumps(**kwargs))

    def dumps(self, **kwargs) -> Any:
        raise NotImplementedError(f"{self.__class__.__name__} does not implement `dumps` as a class function")

    # Structure Formats
    def _typeFormat(self, itm: Definition, **kwargs):
        print(f"{self.__class__.__name__}: format {itm.name}({itm.data_type}) not converted")

    # Structures
    _formatArray = _typeFormat
    _formatArrayOf = _typeFormat
    _formatChoice = _typeFormat
    _formatEnumerated = _typeFormat
    _formatMap = _typeFormat
    _formatMapOf = _typeFormat
    _formatRecord = _typeFormat
    # Primitives
    _formatBinary = _typeFormat
    _formatBoolean = _typeFormat
    _formatInteger = _typeFormat
    _formatNumber = _typeFormat
    _formatString = _typeFormat

    def _makeStructures(self, default: Any = None, **kwargs) -> Dict[str, Union[dict, str]]:
        structs = {}
        for def_name, def_cls in self._schema.types.items():
            df = getattr(self, f"_format{def_cls.data_type}", self._typeFormat)
            if conv := df(def_cls, **kwargs):
                structs[def_name] = conv
            else:
                structs[def_name] = default
        return structs

    def _makeStructuresString(self, default: Any = None, **kwargs) -> str:
        defs = self._makeStructures(default, **kwargs)
        def_str = ''
        for def_name in self._definition_order:
            def_str += defs.pop(def_name, '')
        def_str += '\n'.join(defs.values())
        return def_str

    def formatTitle(self, title: str) -> str:
        words = [self._title_overrides.get(w, w) for w in title.split("-")]
        return " ".join(words)

    def formatStr(self, s: str) -> str:
        escape_chars = list(filter(None, self.escape_chars))
        if s == "*":
            return "unknown"
        if len(escape_chars) > 0:
            return re.compile(rf"[{''.join(escape_chars)}]").sub('_', s)
        return s
