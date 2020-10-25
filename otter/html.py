
import matplotlib, numpy
from . import plot
import markdown
import tabulate

md_extensions = [
    'markdown.extensions.tables',
    'markdown.extensions.extra'
    ]


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
            if attr=="cl": attr="class"
            attributes += """{}='{}'""".format(attr, val)
        if self.tag: output += "<{} {}>".format(self.tag, attributes)
        for item in self.content:
            if self.childtag:
                output += "<{0}>{1}</{0}>".format(self.childtag, str(item))
            else:
                output += str(item)
        if self.tag: output += "</{}>".format(self.tag)
        return output

    def __str__(self):
        return self.__repr__()
    
    def __iadd__(self, item):
        self.__add__(item)
        return self.content
        
    def __add__(self, item):
        #if isinstance(item, list) and isinstance(item[0], list):
        #    self.content.append( )

        if type(item) in handlers.keys():
            self.content.append(handlers[type(item)](item))
        else:
            self.content.append(item)


class OrderedList(HTMLElement):
    tag = "ol"
    childtag = "li"

    def __add__(self, items):
        for item in items:
            if type(item) in handlers.keys():
                self.content.append(handlers[type(item)](item))
            else:
                self.content.append(item)


      
class Table(HTMLElement):
    tag = "table"

class Row(HTMLElement):
    tag = "tr"
    childtag = "td"
    
    def __add__(self, items):
        for item in items:
            if type(item) in handlers.keys():
                self.content.append(handlers[type(item)](item))
            else:
                self.content.append(item)

def dict_to_table(dictionary):
    table = Table(cl="table table-sm table-striped table-bordered")
    for key, val in dictionary.items():
        table + Row([key, val])
    return table

handlers = {
    str: lambda x: markdown.markdown(str(x), output_format='xhtml5', extensions=md_extensions),
    matplotlib.figure.Figure: plot.Figure,
    list: OrderedList,
    dict: dict_to_table,
    numpy.ndarray: lambda x: tabulate.tabulate(x, tablefmt=MyHTMLFormat)
}

from functools import partial
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
