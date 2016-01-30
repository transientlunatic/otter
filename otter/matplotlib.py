"""
Implements an interface with the Matplotlib plotting library in order to add plots to a report.
"""

import uuid
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

class Figure():
    def __init__(self, report, figure=None, filename=None):
        if filename==None:
            filename = "{}.png".format(uuid.uuid4().hex)
	if figure:
        	figure.savefig(report.reportfolder+"/"+filename, dpi=300)
	else:
		plt.savefig(self.reportfolder+"/"+filename, dpi=300)
        self.url = report.foldername+filename
    
    def __repr__(self):
        html_str= """
          <img src="{}" style="max-width: 100%;" class="img-responsive"></img>
        """.format(self.url)
        return html_str
