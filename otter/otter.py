# -*- coding: utf-8 -*-

#import uuid
import os

import ConfigParser

from jinja2 import Template, Environment, FileSystemLoader

from pkg_resources import resource_string, resource_stream, resource_filename
default_config = resource_stream(__name__, 'otter.conf')

class Otter():
    """Otter is a pythonic report writing system designed to produce HTML
    reports for long-running or complex jobs where and iPython
    notebook would be an impractical way of presenting information.
    """
    def __init__(self, filename, config_file=None, **kwargs):
        """
        An Otter report is created by this class.

        Parameters
        ----------
        filename : str
           The path to the location of the report, for example `/home/me/www/report.html`.
        config_file: str
           The location of the config file which should be used to generate the report.
        """

        # Attempt to load in default meta data from a config file
        # At the moment just the current directory, but should
        # extend to look in home directory and environment variable location too

        config = ConfigParser.ConfigParser()
        #if not config_file:
        config.readfp(default_config)
        if config_file:
            config.read(config_file)
        self.meta = {}
        
        for option in config.options('meta'):
            self.meta[option] = config.get('meta', option)
        for option in kwargs.items():
            self.meta[option[0]] = option[1]
            
        try:
            theme = config.get("theme", "location")
        except:
            print("Cannot find theme in the config file. Using the default theme.")
            try:
                theme = resource_filename(__name__, "themes/default/")
            except:
                print("No theme files found.")
            
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
        return self

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



