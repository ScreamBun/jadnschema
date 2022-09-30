"""
Conversion utilities
"""
import copy
import re

from typing import Callable, Tuple, Union
from lxml.etree import Comment, Element, tostring  # pylint: disable=E0611
from lxml.html import builder
# TODO: format css styles in DocHTML


class Doc:
    """
    Base class generating html/xml documents using context managers
    """
    # Context vars
    parent: Union[None, 'Doc.Tag']
    # Class vars
    init: str
    value: None

    def __init__(self, init: str = None, **kwargs):
        # Context vars
        self.parent = None
        # Class Vars
        self.init = init or ''
        self.value = None

    def context(self) -> Tuple['Doc', Callable]:
        return self, self.tag

    def getvalue(self, pretty: bool = False) -> str:
        return tostring(self.value, pretty_print=pretty, doctype=self.init).decode()

    def tag(self, tag_name: str, text: str = None, **kwargs) -> 'Doc.Tag':
        tmp = self.__class__.Tag(self, tag_name, text, **kwargs)
        (self.parent or self).value.append(tmp.value)
        return tmp

    class Tag:
        """
        Base class for html/xml elements using context managers
        """
        # Context vars
        doc: 'Doc'
        parent: Union[None, 'Tag']
        # Class vars
        value: Element

        def __init__(self, doc: 'Doc', tag_name: str, text: str = None, **kwargs):
            # Context vars
            self.doc = doc
            self.parent = None
            # Class Vars
            self.value = None

        def __enter__(self):
            self.parent = self.doc.parent
            self.doc.parent = self
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            (self.parent or self.doc).value.append(self.value)
            self.doc.parent = self.parent

        def comment(self, msg: str):
            self.value.append(Comment(f" {msg.strip()} "))


class DocHTML(Doc):
    """
    class generating html documents using context managers
    """
    # Context vars
    parent: Union[None, 'Tag']
    # Class vars
    init: str
    value: builder.HTML

    def __init__(self, init: str = None, **kwargs):
        super().__init__(init, **kwargs)
        self.value = builder.HTML(**kwargs)

    def getvalue(self, pretty: bool = False) -> str:
        args = {'doctype': self.init} if self.init else {}
        val = copy.deepcopy(self.value)
        if pretty:
            self._indent(val)
        return tostring(val, method='html', **args).decode().replace("\t", " "*4)

    def _indent(self, elem, level=0):
        indent = '\n' + level * '\t'
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = f'{indent}\t'
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for e in elem:
                self._indent(e, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent

    def _format_css(self, css):
        """
        Format the CSS to a predefined standard
        :param css: CSS string to format
        :return: formatted CSS
        """
        line_breaks = ("\*/", "{", "}", ";")  # pylint: disable=anomalous-backslash-in-string
        css_formatted = re.sub(rf"(?P<term>{'|'.join(line_breaks)})", r"\g<term>\n", css)
        css_formatted = css_formatted[:-1]

        return "\n".join(re.sub(r"\s{4}", "\t", l) for l in css_formatted.split("\n"))

    class Tag(Doc.Tag):
        # Context vars
        doc: 'DocHTML'
        parent: Union[None, 'Tag']
        # Class vars
        value: builder.E

        def __init__(self, doc: 'DocHTML', tag_name: str, text: str = None, **kwargs):
            super().__init__(doc, tag_name, text, **kwargs)
            if cls := kwargs.pop('klass', None):
                kwargs['class'] = cls
            child = (text, ) if text else ()
            self.value = getattr(builder, tag_name.upper())(*child, **kwargs)


class DocXML(Doc):
    """
    Base class generating xml documents using context managers
    """
    # Context vars
    parent: Union[None, 'DocXML.Tag']
    # Class vars
    init: str
    value: Element

    def __init__(self, init: str = None, **kwargs):
        super().__init__(init, **kwargs)
        if root_tag := kwargs.pop("root_tag", None):
            self.value = Element(root_tag, **kwargs)
        else:
            self.value = Element("xml", **kwargs)

    class Tag(Doc.Tag):
        # Context vars
        doc: 'DocXML'
        parent: Union[None, 'Tag']
        # Class vars
        value: Element

        def __init__(self, doc: 'DocXML', tag_name: str, text: str = None, **kwargs):
            super().__init__(doc, tag_name, text, **kwargs)
            if cls := kwargs.pop('klass', None):
                kwargs['class'] = cls
            self.value = Element(tag_name, attrib=kwargs)
            if text:
                self.value.text = text


__all__ = [
    'DocHTML',
    'DocXML'
]
