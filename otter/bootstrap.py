"""
Implements a means of using the Bootstrap html and css toolkit to make the report.
"""

from .html import HTMLElement
from itertools import cycle
import markdown
import tabulate

from .html import *
            
class Row(HTMLElement):
    def __init__(self, cols=1, size='md', hclass=''):
        """
        Add a new row to the grid.

        Parameters
        ----------
        cols : int, list, tuple, or iterable
           Either the number of columns desired, or an array of the widths. 
           The widths are specified in twelfths of the full width, so for example 
           `cols = [4,4,4]` makes three columns each one-third of a page wide. 

        size : {'xs', 'sm', 'md', 'lg'}
           The size of the column, according to the Bootstrap responsive design. Defaults to 'md'.

        hclass : str or iterable
           Adds a class to each column. If an iterable is provided then a seperate class
           can be applied to each column.
        """
        
        self.rowopen = "<div class='row'>"
        self.rowclose = "</div>"
        
        if hasattr(cols, '__getitem__'):
            self.columns = [Column(width, size, hclass) for width, hclass in zip(cols, cycle(hclass))]
        elif isinstance(cols, int):
            width = int(12/cols)
            self.columns = [Column(width, size, hclass) for _ in range(cols)]

    # We want this to degrade nicely so if there's only one column we interface directly with the row
    def __add__(self, item):
        if len(self.columns)==1:
            self.columns[0] + item
        else:
            # Need to throw an error
            pass
        
            
    def __getitem__(self, i):
        return self.columns[i]

    def __setitem__(self, i, item):
        self.columns[i].content = markdown.markdown(item, output_format='xhtml5')
        
    def __repr__(self):
        output = ''
        output += self.rowopen
        for column in self.columns:
            output += repr(column)
        output += self.rowclose
        return output

    
    def __str__(self):
        return self.__repr__()

class Column(HTMLElement):
    def __init__(self, width=12, size="md", hclass=""):
        self.width = width
        self.size = size
        self.hclass = hclass
        self.colopen = "<div class='col-{size}-{width} {hclass}'>"
        self.colclose = "</div>"
        self.content = []

    def __repr__(self):
        output = ''
        output += self.colopen.format(size=self.size, width=self.width, hclass=self.hclass)
        for content in self.content:
                output += str(content)
        output += self.colclose
        return output
    
    def __str__(self):
        return self.__repr__()

# class Collapse(HTMLElement):
#     """
#     Creates a bootstrap collapsable div.
#     """
#     def __init__(self, text
    
class Alert(HTMLElement):
    """
    Creates a Bootstrap alert object in the report.
    """
    def __init__(self, text='',style='info',  hclass=''):
        self.alertopen = "<div class='alert alert-{}' role='alert'>".format(style)
        self.alertclose = "</div>"
        self.content = text

    def __repr__(self):
        output = ''
        output += self.alertopen
        output += self.content
        output += self.alertclose
        return output
        
    def __str__(self):
        return self.__repr__()


class Label(HTMLElement):
    def __init__(self, text="", style="default"):
        """
        Make a new label element.
        """
        self.opening = "<span class='label label-{}'>".format(style)
        self.closing = "</span>"
        self.content = text
    def __repr__(self):
        output = ''
        return self.opening + self.content + self.closing
    def __str__(self):
        return self.__repr__()
    
class Panel(HTMLElement):
    """
    Creates a Bootstrap panel object in the report.
    """
    def __init__(self, title='', footer = '', style='default', hclass=''):
        self.title = title
        self.footer = footer
        self.style = style
        self.hclass = hclass

        self.panopen = "<div class='panel panel-{style} {hclass}'>"
        self.panclose = "</div>"

        self.panbody = "<div class='panel-body'>{}</div>"
        self.panheader = "<div class='panel-heading'>{}</div>"
        self.panfooter = "<div class='panel-footer'>{}</div>"
        
        self.content = []


    def __repr__(self):
        output = ''
        output += self.panopen.format(style=self.style, hclass=self.hclass)
        if self.panheader != '': output += self.panheader.format(self.title)
        contents = ""
        for content in self.content:
                contents += str(content)
        output += self.panbody.format(contents)
        if self.footer != '': output += self.panfooter.format(self.footer)
        output += self.panclose
        return output

    __str__ = __repr__
