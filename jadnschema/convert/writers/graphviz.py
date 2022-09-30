"""
JADN to GraphViz
"""
import json
import re

from typing import Union, get_args
from graphviz import Digraph
from pydantic.fields import ModelField  # pylint: disable=no-name-in-module
from .baseWriter import WriterBase
from ..enums import CommentLevels
from ...schema import Schema
from ...schema.definitions import Primitive
from ...utils import FrozenDict
StandardField = dict

GraphStyles = FrozenDict({
    "links": True,              # Show link edges (dashed)
    "attributes": False,        # Show node attributes connected to entities (ellipse)
    "attr_color": "palegreen",  # Attribute ellipse fill color
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
        "bgcolor": "transparent"
    }
})


# Conversion Class
class JADNtoGraphViz(WriterBase):  # pylint: disable=abstract-method
    format = "gv"
    comment_single = "#"
    comment_multi = (comment_single, "")
    atypes = (*(d.__name__ for d in get_args(Primitive)), "Enumerated")

    def dumps(self, **kwargs) -> str:
        """
        Converts the JADN schema to JADN
        :return: JSON schema
        """
        dot = Digraph(name="G", **GraphStyles.dotfile)
        dot.attr(**GraphStyles.dotattr)
        node_link = {t.name: f"n{i}" for i, t in enumerate(self._schema.types.values()) if t.data_type not in self.atypes}
        for idx, type_def in enumerate(self._schema.types.values()):
            node_attrs = {}
            if type_def.data_type in self.atypes:
                node_attrs.update(shape="ellipse", fillcolor=GraphStyles.attr_color)
            if GraphStyles.attributes or not node_attrs:
                if "<->" in type_def.description:
                    node_attrs.update(shape="hexagon")
                dot.node(name=f"n{idx}", label=type_def.name, **node_attrs)
                if type_def.has_fields():
                    for field in type_def.__fields__.values():
                        if field.field_info.extra["type"] in node_link:
                            dot.edge(f"n{idx}", node_link[field.field_info.extra["type"]], **self._fieldAttrs(field))
        return f"{self.makeHeader()}\n\n{dot.source}".replace("\t", " "*4)

    def makeHeader(self):
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

    def _fieldAttrs(self, field: ModelField) -> dict:
        field_opts, _ = field.field_info.extra["options"].split()
        attrs = {"style": "dashed"} if field_opts.link or "<=" in field.field_info.description else {}
        if GraphStyles.links or not attrs:
            if GraphStyles.edge_label:
                attrs.update(label=field.name)
            if GraphStyles.multiplicity:
                multi_f = field.field_info.extra["options"].multiplicity(1, 1, True)
                multi_r = m.group(1) if (m := re.search(r"\[([^]]+)]", field.field_info.description)) else "1"
                attrs.update(headlabel=multi_f, taillabel=multi_r)
        return attrs


# Writer Functions
def dot_dump(schema: Union[str, dict, Schema], fname: str, source: str = "", comm: CommentLevels = CommentLevels.ALL, **kwargs):
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoGraphViz(schema, comm).dump(fname, source, **kwargs)


def dot_dumps(schema: Union[str, dict, Schema], comm: CommentLevels = CommentLevels.ALL, **kwargs):
    comm = comm if comm in CommentLevels else CommentLevels.ALL
    return JADNtoGraphViz(schema, comm).dumps(**kwargs)
