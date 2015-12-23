# -*- coding: utf-8 -*-

import uuid
import os
import matplotlib.pyplot as plt

class Otter():
    def __init__(self, filename, meta):
        self.reportfile= open(filename,"w")
        self.reportfolder = filename+"_files"
        self.foldername = os.path.basename(filename)+"_files/"
        if not os.path.exists(self.reportfolder):
            os.makedirs(self.reportfolder)
        self.meta = meta
        self.write_preamble()
        
    def _write(self, text):
        self.reportfile.write(text)
        
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

    def write_image(self, url):
        html_str= """
        <div class="row">
          <img src="{}" style="max-width: 100%;" class="img-responsive"></img>
        </div>
        """.format(url)
        self._write(html_str)

    def write_plot(self, filename=None):
        if filename==None:
            filename = "{}.png".format(uuid.uuid4().hex)
        plt.savefig(self.reportfolder+"/"+filename, dpi=300)
        self.write_image(self.foldername+filename)


