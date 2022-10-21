from enum import Enum
from typing import Dict, List, Union
from terminaltables import AsciiTable, GithubFlavoredMarkdownTable


class Alignment(str, Enum):
    ALIGN_LEFT = 'left'
    ALIGN_CENTER = 'center'
    ALIGN_RIGHT = 'right'


class TableFormat(Enum):
    Ascii = AsciiTable
    MarkDown = GithubFlavoredMarkdownTable


def basic_style(horizontal: str = "-", vertical: str = "|", intersect: str = "+") -> dict:
    styles = {}
    shared_positions = ("F_INNER", "H_INNER", "INNER")
    hv_shared_positions = ("F_OUTER_LEFT", "F_OUTER_RIGHT", "H_OUTER_LEFT", "H_OUTER_RIGHT")
    for position in (*shared_positions, "OUTER_BOTTOM", "OUTER_TOP", "OUTER_LEFT", "OUTER_RIGHT"):
        styles[f"CHAR_{position}_HORIZONTAL"] = horizontal

    for position in (*shared_positions, *hv_shared_positions, "OUTER_BOTTOM"):
        styles[f"CHAR_{position}_VERTICAL"] = vertical

    for position in (*shared_positions, *hv_shared_positions, "OUTER_TOP"):
        styles[f"CHAR_{position}_INTERSECT"] = intersect
    styles.update(
        CHAR_OUTER_BOTTOM_LEFT=intersect,
        CHAR_OUTER_BOTTOM_RIGHT=intersect,
        CHAR_OUTER_TOP_LEFT=intersect,
        CHAR_OUTER_TOP_RIGHT=intersect
    )
    return styles


class TableStyle(Enum):
    STYLE_BASIC = basic_style()
    STYLE_NONE = {
        "inner_column_border": False,
        "inner_footing_row_border": False,
        "inner_heading_row_border": False,
        "inner_row_border": False,
        "outer_border": False
    }


ColumnAlignment = Union[List[Alignment], Dict[int, Alignment]]
TableStyles = {
    "inner_column_border": False,
    "inner_footing_row_border": False,
    "inner_heading_row_border": False,
    "inner_row_border": False,
    "outer_border": False
}


__all__ = [
    "Alignment",
    "ColumnAlignment",
    "TableFormat",
    "TableStyle",
    "TableStyles",
    "basic_style"
]
