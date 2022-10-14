"""
JADN to HTML
"""
import json
import os

from typing import List, Union
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module
from .baseWriter import BaseWriter
from .utils import DocHTML
from ..enums import CommentLevels
from ...jadn import data_dir
from ...schema import Schema
from ...schema.definitions import Options, Array, ArrayOf, Choice, Enumerated, Map, MapOf, Record
from ...schema.definitions import DefTypes
__pdoc__ = {
    "JADNtoHTML.format": "File extension of the given format",
    "JADNtoHTML.escape_chars": "Characters that are not supported in the schema format and need to be removed/escaped",
    "JADNtoHTML.comment_multi": "Multiline comment characters; Tuple[START_CHAR, END_CHAR]",
    "JADNtoHTML.comment_single": "Single line comment character",
}


# Conversion Class
class JADNtoHTML(BaseWriter):
    format = "html"
    comment_multi = ("<!--", "-->")
    _themeFile = os.path.join(data_dir(), "theme.css")  # Default theme
    _scriptFile = os.path.join(data_dir(), "scripts.js")  # Default scripts

    def dumps(self, styles: str = None, **kwargs) -> str:  # pylint: disable=W0221
        """
        Converts the JADN schema to HTML
        :param styles: CSS or Less styles to add to the HTML
        :return: JSON schema
        """
        # Make initial tree
        doc, tag = DocHTML('<!DOCTYPE html>', lang='en').context()

        with tag('head'):
            tag('meta', charset='UTF-8')
            tag('title', self._schema.info.get("title", "JADN Schema Convert"))
            # tag('link', rel='stylesheet', href=f'{data_dir()}/theme.css', type='text/css')
            tag("style", self._loadStyles(styles), type="text/css")
            tag("script", self._loadScript(), type="text/javascript")

        with tag('body'):
            with tag("div", id="schema"):
                tag('h1', 'Schema')
                with tag("div", id="meta"):
                    self.makeHeader(tag)
                with tag("div", id="types"):
                    self.makeStructures(tag)

        return doc.getvalue(True)

    def makeHeader(self, tag: DocHTML.tag) -> None:
        """
        Create the headers for the schema
        :return: header for schema
        """
        with tag("table"):
            for key, val in self._schema.info.items():
                with tag("tr"):
                    tag("td", f'{key}:', klass="h")
                    tag("td", json.dumps(val), klass="s")

    def makeStructures(self, tag: DocHTML.tag) -> None:
        """
        Create the type definitions for the schema
        :return: type definitions for the schema
        """
        tag("h2", "Compound Types")
        primitives = []

        for type_def in self._schema.types.values():
            if type_def.is_structure() or type_def.is_selector():
                getattr(self, f"_format{type_def.data_type}")(type_def, tag=tag)
            else:
                mltiOpts = {} if type_def.data_type in ("Integer", "Number") else {"check": lambda x, y: x > 0 or y > 0}
                multi = type_def.__options__.multiplicity(**mltiOpts)
                multi = f"{{{multi}}}" if multi else ""
                fmt = f" /{type_def.__options__.format}" if type_def.__options__.format else ""
                primitives.append(dict(
                    Name=type_def.name,
                    Definition=f"{type_def.data_type}{multi}{fmt}",
                    Description=type_def.description
                ))

        tag("h2", "Primitive Types")
        self._makeHtmlTable(
            tag=tag,
            headers=dict(
                Name={"class": "b"},
                Definition={"class": "s"},
                Description={"class": "d"}
            ),
            rows=primitives,
            column_id="Name"
        )

    # Structure Formats
    def _formatArray(self, itm: Array, **kwargs) -> None:
        tag: DocHTML.tag = kwargs["tag"]
        name = self.formatStr(itm.name)
        tag("h3", name, id=name)
        if itm.description:
            tag("h4", itm.description)

        self._makeHtmlTable(
            tag=tag,
            headers={
                "ID": {"class": "n"},
                "Type": {"class": "s"},
                "#": {"class": "n"},
                "Description": {"class": "s"},
            },
            rows=self._makeTableRows(itm.__fields__.values(), "Array"),
            caption=f"{self.formatStr(itm.name)} (Array)"
        )

    def _formatArrayOf(self, itm: ArrayOf, **kwargs) -> None:
        tag: DocHTML.tag = kwargs["tag"]
        name = self.formatStr(itm.name)
        tag("h3", name, id=name)
        if itm.description:
            tag("h4", itm.description)
        value_type = self.formatStr(itm.__options__.get("vtype", "string"))
        multi = itm.__options__.multiplicity(0, 0, check=lambda x, y: x > 0 or y > 0)
        multi = f"{{{multi}}}" if multi else ""
        tag("p", f"{self.formatStr(itm.name)} (ArrayOf({value_type}){multi})")

    def _formatChoice(self, itm: Choice, **kwargs) -> None:
        tag: DocHTML.tag = kwargs["tag"]
        name = self.formatStr(itm.name)
        tag("h3", name, id=name)
        if itm.description:
            tag("h4", itm.description)

        opts = itm.__options__.dict(exclude_unset=True)
        self._makeHtmlTable(
            tag=tag,
            headers={
                "ID": {"class": "n"},
                "Name": {"class": "b"},
                "Type": {"class": "s"},
                "Description": {"class": "d"},
            },
            rows=self._makeTableRows(itm.__fields__.values(), "Choice"),
            caption=f"{self.formatStr(itm.name)} (Choice{f' {json.dumps(opts)}' if opts.keys() else ''})"
        )

    def _formatEnumerated(self, itm: Enumerated, **kwargs) -> None:
        tag: DocHTML.tag = kwargs["tag"]
        name = self.formatStr(itm.name)
        tag("h3", name, id=name)
        if itm.description:
            tag("h4", itm.description)

        rows = []
        if "id" in itm.__options__:
            headers = {"ID": {"class": "n"}}
            for f in itm.__enums__:
                rows.append({"ID": f.value.extra["id"], "Description": f"<span class=\"b\">{f.value.default}</span>::{f.value.description}"})
        else:
            headers = {"ID": {"class": "n"}, "Name": {"class": "b"}}
            for f in itm.__enums__:
                rows.append({"ID": f.value.extra["id"], "Name": f.value.default, "Description": f.value.description})

        headers["Description"] = {"class": "d"}
        self._makeHtmlTable(
            tag=tag,
            headers=headers,
            rows=rows,
            caption=f"{self.formatStr(itm.name)} (Enumerated{'.ID' if 'id' in itm.__options__ else ''})"
        )

    def _formatMap(self, itm: Map, **kwargs) -> None:
        tag: DocHTML.tag = kwargs["tag"]
        name = self.formatStr(itm.name)
        tag("h3", name, id=name)
        if itm.description:
            tag("h4", itm.description)

        multi = itm.__options__.multiplicity(check=lambda x, y: x > 0 or y > 0)
        multi = f"{{{multi}}}" if multi else ""

        self._makeHtmlTable(
            tag=tag,
            headers={
                "ID": {"class": "n"},
                "Name": {"class": "b"},
                "Type": {"class": "s"},
                "#": {"class": "n"},
                "Description": {"class": "d"},
            },
            rows=self._makeTableRows(itm.__fields__.values(), "Map"),
            caption=f"{self.formatStr(itm.name)} (Map{multi})"
        )

    def _formatMapOf(self, itm: MapOf, **kwargs) -> None:
        tag: DocHTML.tag = kwargs["tag"]
        name = self.formatStr(itm.name)
        tag("h3", name, id=name)
        if itm.description:
            tag("h4", itm.description)

        key_type = self.formatStr(itm.__options__.get("ktype", "string"))
        value_type = self.formatStr(itm.__options__.get("vtype", "string"))
        value_count = itm.__options__.multiplicity()
        tag("p", f"{self.formatStr(itm.name)} (MapOf({key_type}, {value_type})[{value_count}])")

    def _formatRecord(self, itm: Record, **kwargs) -> None:
        tag: DocHTML.tag = kwargs["tag"]
        name = self.formatStr(itm.name)
        tag("h3", name, id=name)
        if itm.description:
            tag("h4", itm.description)
        multi = itm.__options__.multiplicity(check=lambda x, y: x > 0 or y > 0)
        multi = f"{{{multi}}}" if multi else ""

        self._makeHtmlTable(
            tag=tag,
            headers={
                "id": {"class": "n"},
                "name": {"class": "b"},
                "type": {"class": "s"},
                "#": {"class": "n"},
                "description": {"class": "d"},
            },
            rows=self._makeTableRows(itm.__fields__.values(), "Record"),
            caption=f"{self.formatStr(itm.name)} (Record{multi})"
        )

    # Helper Functions
    def _loadStyles(self, styles: str = None) -> str:
        """
        Load the given styles
        :param styles: the CSS or Less file location
        :return:
        """
        if styles in ["", " ", None]:  # Check if theme exists
            if os.path.isfile(self._themeFile):
                with open(self._themeFile, "r", encoding="UTF-8") as f:
                    return f.read()
            else:
                return ""

        ext = os.path.splitext(styles)[1]
        if ext != ".css":  # Check valid theme format
            raise TypeError("Styles are not in css format")

        if os.path.isfile(styles):
            if ext == ".css":
                return open(styles, "r", encoding="UTF-8").read()
            raise ValueError("The style format specified is an unknown format")
        raise IOError(f"The style file specified does not exist: {styles}")

    def _loadScript(self) -> str:
        """
        Load the scripts
        :return:
        """
        if os.path.isfile(self._scriptFile):
            with open(self._scriptFile, "r", encoding="UTF-8") as f:
                return f.read()
        else:
            return ""

    def _makeHtmlTable(self, tag: DocHTML.tag, headers: dict, rows: list, caption: str = "", column_id: str = None) -> None:
        """
        Create a table using the given header and row values
        :param headers: table header names and attributes
        :param rows: row values
        :return: formatted HTML table
        """
        with tag("table"):
            # Caption
            if caption not in ["", " ", None]:
                tag("caption", caption)

            # Headers
            with tag("thead"):
                with tag("tr"):
                    for column, opts in headers.items():
                        tag("th", column, **opts)

            # Body
            with tag("tbody"):
                for row in rows:
                    with tag("tr"):
                        for column, opts in headers.items():
                            attrs = headers.get(column, {})
                            with tag("td", **attrs):
                                has_column = column in row if isinstance(row, dict) else hasattr(row, column)
                                column = column if has_column else self._table_field_headers.get(column, column)

                                if isinstance(column, str):
                                    cell = row.get(column, "")
                                else:
                                    cell = list(filter(None, [row.get(c, None) for c in column]))
                                    cell = cell[0] if len(cell) == 1 else ""
                                td_id = cell

                                if column == "type" and isinstance(cell, tuple):
                                    td_id, desc = cell
                                    if td_id not in DefTypes:
                                        tag("a", f"{td_id}", href=f"#{td_id}")
                                        cell = ""
                                    else:
                                        cell = td_id
                                    cell += desc

                                elif column == "options" and isinstance(cell, Options):
                                    cell = cell.multiplicity(1, 1, True)
                                cell = str(cell)
                                tag("span", " " if cell == "" else cell, **({"id": td_id} if column_id == column else {}))

    def _makeTableRows(self, fields: List[ModelField], dataType: str) -> List[dict]:
        rows = []
        for field in fields:
            info = field.field_info
            row = {
                "id": info.extra["id"],
                "name": field.alias,
                "type": "",
                "options": info.extra["options"],
                "description": info.description
            }

            # Field Type
            field_type = info.extra['type']
            desc = {
                "ArrayOf": lambda o: f"({o.get('vtype', 'String')})",
                "MapOf": lambda o: f"({o.get('ktype', 'String')}, {o.get('vtype', 'String')})",
                "String": lambda o: f"(%{o.pattern}%)" if o.pattern else ""
            }.get(field_type, lambda o: "")(info.extra["options"])
            desc += f" /{info.extra['options'].format}" if info.extra['options'].format else ""
            row["type"] = field_type, desc
            rows.append(row)
        return rows


# Writer Functions
def html_dump(schema: Union[str, dict, Schema], fname: str, source: str = "", comm: CommentLevels = CommentLevels.ALL, **kwargs) -> None:
    """
    Convert the JADN schema to HTML and write it to the given file
    :param schema: Schema to convert
    :param fname: schema file to write
    :param source: source information
    :param comm: comment level
    :param kwargs: key/value args for the conversion
    """
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoHTML(schema, comm).dump(fname, source, **kwargs)


def html_dumps(schema: Union[str, dict, Schema], comm: CommentLevels = CommentLevels.ALL, **kwargs) -> str:
    """
    Convert the JADN schema to HTML
    :param schema: Schema to convert
    :param comm: comment level
    :param kwargs: key/value args for the conversion
    :return: HTML string
    """
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoHTML(schema, comm).dumps(**kwargs)
