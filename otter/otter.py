# -*- coding: utf-8 -*-

import uuid
import os

import ConfigParser

from jinja2 import Template, Environment, FileSystemLoader

import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

class Otter():
    """Otter is a pythonic report writing system designed to produce HTML
    reports for long-running or complex jobs where and iPython
    notebook would be an impractical way of presenting information.
    """
    def __init__(self, filename, theme, **kwargs):
        """
        An Otter report is created by this class.

        Parameters
        ----------
        filename : str
           The path to the location of the report, for example `/home/me/www/report.html`.
        meta : dict
           A dictionary of metadata. This is likely to change very soon, but at present a dictionary is required for the title, subtitle, and author's name of the report.
        """

        # Attempt to load in default meta data from a config file
        # At the moment just the current directory, but should
        # extend to look in home directory and environment variable location too

        config = ConfigParser.ConfigParser()
        config.read('otter.cfg')
        self.meta = {}
        for option in config.options('meta'):
            self.meta[option] = config.get('meta', option)
        
        self.env = Environment(loader=FileSystemLoader(theme))
        
        self.reportfolder = filename+"_files"
        self.foldername = os.path.basename(filename)+"_files/"
        if not os.path.exists(self.reportfolder):
            os.makedirs(self.reportfolder)
        self.reportfile= open(filename,"w")
        self.meta.update(kwargs)
        self.items = []

    def __add__(self, item):
        return self.add(item)
        
    def add(self, item):
        self.items.append(item)
        return item

    def show(self):
        html = ''
        for item in self.items:
            html += repr(item)
        output_html = self.env.get_template('body.html').render(meta=self.meta, body=html)
        self._write(output_html)
        
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
    
    def write_image(self, url):
        html_str= """
        <div class="row">
          <img src="{}" style="max-width: 100%;" class="img-responsive"></img>
        </div>
        """.format(url)
        self._write(html_str)
        
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


