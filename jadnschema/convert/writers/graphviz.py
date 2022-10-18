"""
JADN to GraphViz
"""
import json
import re

from typing import Union
from graphviz import Digraph
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module
from .baseWriter import BaseWriter
from ..enums import CommentLevels
from ..helpers import register_writer
from ...schema import Schema
from ...schema.consts import OPTION_ID, PRIMITIVE_TYPES
from ...schema.definitions import DefinitionBase, ArrayOf, MapOf
from ...utils import FrozenDict
__all__ = ["JADNtoGraphViz", "dot_dump", "dot_dumps"]
__pdoc__ = {
    "JADNtoGraphViz.format": "File extension of the given format",
    "JADNtoGraphViz.escape_chars": "Characters that are not supported in the schema format and need to be removed/escaped",
    "JADNtoGraphViz.comment_multi": "Multiline comment characters; Tuple[START_CHAR, END_CHAR]",
    "JADNtoGraphViz.comment_single": "Single line comment character"
}

GraphStyles = FrozenDict({
    "links": True,              # Show link edges (dashed)
    "attributes": False,        # Show node attributes connected to entities (ellipse)
    "attr_color": "palegreen",  # Attribute ellipse fill color
    "bgcolor": "white",         # Graph background color
    "edge_label": True,         # Show field name on edges
    "multiplicity": True,       # Show multiplicity on edges
    "dotfile": {                # Options defined in GraphViz "Node, Edge and Graph Attributes"
        "graph_attr": {
            "fontname": "Times",
            "fontsize": "12"
        },
        "node_attr": {
            "fontname": "Arial",
            "fontsize": "8",
            "shape": "box",
            "style": "filled",
            "fillcolor": "lightskyblue1"
        },
        "edge_attr": {
            "fontname": "Arial",
            "fontsize": "7",
            "arrowsize": "0.5",
            "labelangle": "45.0",
            "labeldistance": "0.9"
        }
    },
    "dotattr": {
        "bgcolor": "white"
    }
})
ShapeTypes = FrozenDict({
    # Primitive
    "Binary": "ellipse",
    "Boolean": "ellipse",
    "Integer": "ellipse",
    "Number": "ellipse",
    "String": "ellipse",
    # Selector
    "Enumerated": "ellipse",
    "Choice": "diamond",
    # Structured
    "Array": "rectangle",
    "ArrayOf": "rectangle",
    "Map": "rectangle",
    "MapOf": "rectangle",
    "Record": "rectangle"
})


# Conversion Class
@register_writer
class JADNtoGraphViz(BaseWriter):  # pylint: disable=abstract-method
    format = "gv"
    comment_single = "#"
    comment_multi = (comment_single, "")

    def dumps(self, **kwargs) -> str:
        dot = Digraph(name="G", **GraphStyles.dotfile)
        dot.attr(**GraphStyles.dotattr)
        node_link = {t.name: f"n{i}" for i, t in enumerate(self._schema.types.values())}

        for idx, type_def in enumerate(self._schema.types.values()):
            node_attrs = {"shape": ShapeTypes.get(type_def.data_type, "rectangle")}
            if type_def.data_type in PRIMITIVE_TYPES:
                node_attrs["fillcolor"] = GraphStyles.attr_color
            if "<->" in type_def.description:
                node_attrs.update(shape="hexagon")
            dot.node(name=f"n{idx}", label=f"{type_def.name}({type_def.data_type})", **node_attrs)

            if type_def.has_fields() and type_def.data_type != "Enumerated":
                for field in type_def.__fields__.values():
                    self._nestedLink(idx, field, dot, node_link, type_def)
            elif type_def.data_type in ("ArrayOf", "MapOf"):
                self._nestedLink(idx, type_def, dot, node_link)
        return f"{self.makeHeader()}\n\n{dot.source}".replace("\t", " "*4)

    def makeHeader(self) -> str:
        """
        Create the header for the schema
        :return: header for schema
        """
        def mkrow(k, v):
            if isinstance(v, (dict, list)) or hasattr(v, "schema"):
                v = v.schema() if hasattr(v, "schema") else v
                v = json.dumps(v)
            return f"{k}: {v}"

        info = self._schema.info.schema()
        header = [f"{self.comment_single} {mkrow(k, v)}" for k, v in info.items()]
        return "\n".join(header)

    # Helpers
    def _fieldAttrs(self, field: Union[ModelField, ArrayOf, MapOf]) -> dict:
        if isinstance(field, ModelField):
            required = field.required
            opts = field.field_info.extra["options"]
            desc = field.field_info.description
        else:
            required = True
            opts = field.__options__
            desc = field.description

        attrs = {} if required else {"style": "dashed"}
        if GraphStyles.links:
            if GraphStyles.edge_label:
                attrs.update(label=field.name)
            if GraphStyles.multiplicity:
                multi_f = opts.multiplicity(1, 1, True)
                multi_r = m.group(1) if (m := re.search(r"\[([^]]+)]", desc)) else "1"
                if multi_r != "1":
                    attrs.update(headlabel=multi_f, taillabel=multi_r)
        return attrs

    def _nestedLink(self, idx: int, field: Union[ModelField, ArrayOf, MapOf], dot: Digraph, links: dict, parent: DefinitionBase = None) -> None:
        if isinstance(field, ModelField):
            opts = field.field_info.extra["options"]
            if field.field_info.extra["type"] in links:
                dot.edge(f"n{idx}", links[field.field_info.extra["type"]], **self._fieldAttrs(field))
        else:
            opts = field.__options__

        for k in ("ktype", "vtype", "enum"):
            if val := opts.get(k, None):
                val = val[1:] if val.startswith((OPTION_ID["enum"], OPTION_ID["pointer"])) else val
                if val in links:
                    attrs = self._fieldAttrs(field)
                    if parent:
                        attrs["label"] = k if attrs["label"] == parent.name else f"{k}: {attrs['label']}"
                    else:
                        attrs["label"] = k
                    dot.edge(f"n{idx}", links[val], **attrs)


# Writer Functions
def dot_dump(schema: Union[str, dict, Schema], fname: str, source: str = "", comm: CommentLevels = CommentLevels.ALL, **kwargs) -> None:
    """
    Convert the JADN schema to GraphViz/Dot and write it to the given file
    :param schema: Schema to convert
    :param fname: schema file to write
    :param source: source information
    :param comm: comment level
    :param kwargs: key/value args for the conversion
    """
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoGraphViz(schema, comm).dump(fname, source, **kwargs)


def dot_dumps(schema: Union[str, dict, Schema], comm: CommentLevels = CommentLevels.ALL, **kwargs) -> str:
    """
    Convert the JADN schema to GraphViz/Dot
    :param schema: Schema to convert
    :param comm: comment level
    :param kwargs: key/value args for the conversion
    :return: GraphViz/Dot schema string
    """
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoGraphViz(schema, comm).dumps(**kwargs)
