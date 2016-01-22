# -*- coding: utf-8 -*-

import uuid
import os

from jinja2 import Template, Environment, FileSystemLoader

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

class Otter():
    """Otter is a pythonic report writing system designed to produce HTML
    reports for long-running or complex jobs where and iPython
    notebook would be an impractical way of presenting information.
    """
    def __init__(self, filename, theme, meta):
        """
        An Otter report is created by this class.

        Parameters
        ----------
        filename : str
           The path to the location of the report, for example `/home/me/www/report.html`.
        meta : dict
           A dictionary of metadata. This is likely to change very soon, but at present a dictionary is required for the title, subtitle, and author's name of the report.
        """

        self.env = Environment(loader=FileSystemLoader(theme))
        
        self.reportfolder = filename+"_files"
        self.foldername = os.path.basename(filename)+"_files/"
        if not os.path.exists(self.reportfolder):
            os.makedirs(self.reportfolder)
        self.reportfile= open(filename,"w")
        self.meta = meta

        self.items = []
        
        self.write_preamble()

    def __add__(self, item):
        return self.add(item)
        
    def add(self, item):
        self.items.append(item)
        return item

    def show(self):
        html = ''
        for item in self.items:
            html += repr(item)
        self._write(html)
        
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
        head = self.env.get_template('head.html')
        self._write(head.render(meta=self.meta))

    def write_footer(self):
        footer = self.env.get_template('footer.html')
        self._write(footer.render(meta=self.meta))
        self.reportfile.close()


    def write_page_header(self):
        header = self.env.get_template('header.html')
        self._write(header.render(meta=self.meta))

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
        html_str = """
        <div class="row">
        <div class="alert alert-{}" role="alert">{}</div>
        </div>
        """.format(warning,text)
        self._write(html_str)

    def write_plot(self, figure=None, filename=None):
        if filename==None:
            filename = "{}.png".format(uuid.uuid4().hex)
	if figure:
        	figure.savefig(self.reportfolder+"/"+filename, dpi=300)
	else:
		plt.savefig(self.reportfolder+"/"+filename, dpi=300)
        self.write_image(self.foldername+filename)


