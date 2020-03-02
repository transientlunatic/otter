"""
Implements an interface with the Matplotlib plotting library in order to add plots to a report.
"""

import uuid
import matplotlib
matplotlib.use('Agg')
import base64

from io import BytesIO

import matplotlib.pyplot as plt

class Figure():
    def __init__(self, figure, filename=None, dpi=300):

        self.image = BytesIO()

        if filename==None:
            figure.savefig(self.image, dpi=dpi)
                
        self.bitstring = base64.encodestring(self.image.getvalue())
    
    def __repr__(self):
        html_str= r"""<img src="data:image/png;base64,{}" style="max-width: 100%;" class="img-responsive"/>""".format(self.bitstring.decode("utf-8"))
        return html_str
