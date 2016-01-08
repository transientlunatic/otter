# -*- coding: utf-8 -*-

import uuid
import os

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

class Otter():
    """Otter is a pythonic report writing system designed to produce HTML
    reports for long-running or complex jobs where and iPython
    notebook would be an impractical way of presenting information.
    """
    def __init__(self, filename, meta):
        """
        An Otter report is created by this class.

        Parameters
        ----------
        filename : str
           The path to the location of the report, for example `/home/me/www/report.html`.
        meta : dict
           A dictionary of metadata. This is likely to change very soon, but at present a dictionary is required for the title, subtitle, and author's name of the report.
        """
        
        self.reportfolder = filename+"_files"
        self.foldername = os.path.basename(filename)+"_files/"
        if not os.path.exists(self.reportfolder):
            os.makedirs(self.reportfolder)
        self.reportfile= open(filename,"w")
        self.meta = meta
        self.write_preamble()
        
    def _write(self, text):
        self.reportfile.write(text)

    def _mkdir_recursive(self, path):
        """
        Recursively create the directories required for the report.
        Based off code from http://stackoverflow.com/questions/6004073/how-can-i-create-directories-recursively
        by `Mars'.
        """
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            self._mkdir_recursive(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)
    
    def write_preamble(self):
        html_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="icon" href="../../favicon.ico">
        """
        self._write(html_str)

        html_str="""
        <title>{0[title]}</title>

        <!-- Bootstrap core CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
        
        </head>
        <body>
        <div class="container">
        """.format(self.meta)
        self._write(html_str)

    def write_footer(self):
        html_str="""
	<hr />
	<div class="row">
		<div class="col-md-4">Report created by Otter.</div>
	</div>

        </div> <!-- close the whole container -->
        </body>
        </html>
        
        """
        self._write(html_str)
        self.reportfile.close()


    def write_page_header(self):
        
        html_str = """
        <div class="row">

        <div class="page-header">
           <h1>{0[title]} <small>{0[subtitle]}</small></h1>
        <p><span class="glyphicon glyphicon-user" aria-hidden="true"></span> {0[author]}</p>
        </div>
        """.format(self.meta)
        self._write(html_str)

    def write_row(self, text):
        html_str= """
        <div class="row">
          {}
        </div>
        """.format(text)
        self._write(html_str)

    def write_header(self, level, text):
        html_str= """
        <div class="row">
        <h{0}> 
          {1}
        </h{0}>
        </div>
        """.format(level,text)
        self._write(html_str)

    def write_image(self, url):
        html_str= """
        <div class="row">
          <img src="{}" style="max-width: 100%;" class="img-responsive"></img>
        </div>
        """.format(url)
        self._write(html_str)

    def write_breadcrumb(self, crumbs):
        start ="""
        <ol class="breadcrumb">
        """
        self._write(start)
        for level in crumbs:
            crumb, link = level[0], level[1]
            self._write("""<li><a href="{0}">{1}</a></li>""".format(link, crumb))
        self._write("""</ol>""")
        
    def write_warning(self, warning, text):
        """
        <div class="row">
        <div class="alert alert-{}" role="alert">{}</div>
        </div>
        """.format(warning,text)

    def write_plot(self, figure=None, filename=None):
        if filename==None:
            filename = "{}.png".format(uuid.uuid4().hex)
	if figure:
        	figure.savefig(self.reportfolder+"/"+filename, dpi=300)
	else:
		plt.savefig(self.reportfolder+"/"+filename, dpi=300)
        self.write_image(self.foldername+filename)


