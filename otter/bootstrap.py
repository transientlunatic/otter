"""
Implements a means of using the Bootstrap html and css toolkit to make the report.
"""


from itertools import cycle

class Row():
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
        if len(self.columns==1):
            self.columns[0] + item
        else:
            # Need to throw an error
            pass

    def __set__(self, item):
        if len(self.columns==1):
            self.columns[0] = item
        else:
            # Need to throw an error
            pass
            
    def __getitem__(self, i):
        return self.columns[i]
    
    def __setitem__(self, i, item):
        self.columns[i] = item
        
    def __repr__(self):
        output = ''
        output += self.rowopen
        for column in self.columns:
            output += repr(column)
        output += self.rowclose
        return output

class Column():
    def __init__(self, width, size, hclass):
        self.width = width
        self.size = size
        self.hclass = hclass
        self.colopen = "<div class='col-{size}-{width} {hclass}'>"
        self.colclose = "</div>"
        self.content = ''

    def __iadd__(self, item):
        self.__add__(item)
        
    def __add__(self, item):
        self.content += item

    def __set__(self, instance, item):
        self.content = item

    def __repr__(self):
        output = ''
        output += self.colopen.format(size=self.size, width=self.width, hclass=self.hclass)
        output += self.content
        output += self.colclose
        return output
