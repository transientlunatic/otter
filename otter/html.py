
from functools import partial

import numpy
import markdown
import tabulate
from markupsafe import escape
from matplotlib.figure import Figure as MplFigure

from . import plot

# Try to import pandas, but make it optional
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    pd = None
    PANDAS_AVAILABLE = False

md_extensions = [
    'markdown.extensions.tables',
    'markdown.extensions.extra'
    ]


def _find_handler(cls):
    """
    Find the handler for a class, searching its method resolution order so
    that subclasses (``OrderedDict``, ``Figure`` subclasses, ...) are handled
    by the handler for their parent.
    """
    for klass in cls.__mro__:
        handler = handlers.get(klass)
        if handler is not None:
            return handler
    return None


def register_handler(cls, handler):
    """
    Register a function which converts instances of ``cls`` (and its
    subclasses) into something which renders as HTML.

    Parameters
    ----------
    cls : type
       The type of object to handle.
    handler : callable
       Called with the object; must return an object whose ``str()`` is an
       HTML fragment, such as a string, an :class:`HTMLElement`, or
       :class:`RawHTML`.
    """
    handlers[cls] = handler


def convert(item):
    """
    Convert an arbitrary object into something which renders as HTML.

    The following are tried in order:

    1. :class:`HTMLElement` instances are used as they are.
    2. Objects with an ``__html__`` method (the markupsafe convention) are
       trusted to already be HTML.
    3. Handlers registered with :func:`register_handler`, matched on the
       object's type or any of its parent types.
    4. Objects with a ``_repr_html_`` method (the Jupyter convention, which
       many plotting and table libraries implement).
    5. Anything else is rendered as escaped plain text.
    """
    if isinstance(item, HTMLElement):
        return item
    if hasattr(item, "__html__"):
        return RawHTML(item.__html__())
    handler = _find_handler(type(item))
    if handler is not None:
        return handler(item)
    repr_html = getattr(item, "_repr_html_", None)
    if callable(repr_html):
        rendered = repr_html()
        if isinstance(rendered, tuple):  # (html, metadata) form
            rendered = rendered[0]
        if rendered is not None:
            return RawHTML(rendered)
    return str(escape(str(item)))


class HTMLElement(object):
    tag = None
    childtag = None
    def __init__(self, content=None, **kwargs):
        self.content = []
        self.meta = kwargs
        if content:
            self.__add__(content)

    def __repr__(self):
        output = ""
        attributes = ""
        for attr, val in self.meta.items():
            if attr == "cl":
                attr = "class"
            attributes += " {}='{}'".format(attr, escape(val))
        if self.tag:
            output += "<{}{}>".format(self.tag, attributes)
        for item in self.content:
            if self.childtag:
                output += "<{0}>{1}</{0}>".format(self.childtag, str(item))
            else:
                output += str(item)
        if self.tag:
            output += "</{}>".format(self.tag)
        return output

    def __str__(self):
        return self.__repr__()

    def __iadd__(self, item):
        self.__add__(item)
        return self

    def __add__(self, item):
        self.content.append(convert(item))


class RawHTML(HTMLElement):
    """
    An element containing HTML which is inserted into the report exactly as
    given, without escaping. This is the way to embed things like d3 or
    Plotly output; only use it with HTML you trust.
    """
    def __init__(self, html=""):
        super().__init__()
        self.html = str(html)

    def __add__(self, item):
        self.html += str(convert(item))

    def __repr__(self):
        return self.html

    def __html__(self):
        return self.html


class OrderedList(HTMLElement):
    tag = "ol"
    childtag = "li"

    def __add__(self, items):
        for item in items:
            self.content.append(convert(item))


      
class Table(HTMLElement):
    tag = "table"

class Row(HTMLElement):
    tag = "tr"
    childtag = "td"
    
    def __add__(self, items):
        for item in items:
            self.content.append(convert(item))

def dict_to_table(dictionary):
    table = Table(cl="table table-sm table-striped table-bordered")
    for key, val in dictionary.items():
        table + Row([key, val])
    return table

def my_html_row_with_attrs(celltag, cell_values, colwidths, colaligns):
    alignment = { "left":    '',
                  "right":   ' style="text-align: right;"',
                  "center":  ' style="text-align: center;"',
                  "decimal": ' style="text-align: right;"' }
    values_with_attrs =\
        ["<{0}{1} class=\"my-cell\">{2}</{0}>"
            .format(celltag, alignment.get(a, ''), c)
         for c, a in zip(cell_values, colaligns)]
    return "<tr class=\"my-row\">" + \
            "".join(values_with_attrs).rstrip() + \
            "</tr>"
MyHTMLFormat = tabulate.TableFormat(
        lineabove=tabulate.Line("<table class=\"table table-sm\">", "", "", ""),
        linebelowheader=None,
        linebetweenrows=None,
        linebelow=tabulate.Line("</table>", "", "", ""),
        headerrow=partial(my_html_row_with_attrs, "th"),
        datarow=partial(my_html_row_with_attrs, "td"),
        padding=0, with_header_hide=None)

def dataframe_to_table(df):
    """Convert a pandas DataFrame to an HTML table using tabulate."""
    return tabulate.tabulate(df, headers='keys', tablefmt=MyHTMLFormat)

handlers = {
    str: lambda x: markdown.markdown(str(x), output_format='xhtml5', extensions=md_extensions),
    MplFigure: plot.Figure,
    list: OrderedList,
    dict: dict_to_table,
    numpy.ndarray: lambda x: tabulate.tabulate(x, tablefmt=MyHTMLFormat)
}

# Add pandas DataFrame handler if pandas is available
if PANDAS_AVAILABLE:
    handlers[pd.DataFrame] = dataframe_to_table
