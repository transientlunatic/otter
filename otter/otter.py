# -*- coding: utf-8 -*-

#import uuid
import os
import stat
import tempfile
import importlib
from .html import *
from configparser import ConfigParser

from jinja2 import Template, Environment, FileSystemLoader

from importlib.resources import files
default_config = files(__package__).joinpath('otter.conf').read_bytes()



class Otter():
    """
    Otter is a pythonic report writing system designed to produce HTML
    reports for long-running or complex jobs where and iPython
    notebook would be an impractical way of presenting information.
    """
    def __init__(self, filename, theme_location=None, config_file=None, **kwargs):
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
        config = ConfigParser()
        config.read_string(default_config.decode('utf-8'))
        if config_file:
            with open(config_file) as cf:
                config.read_string(cf.read())
        self.meta = {}

        if config.has_section("meta"):
            for option in config['meta']:
                self.meta[option] = config.get('meta', option)
            for option in kwargs.items():
                self.meta[option[0]] = option[1]

        theme = None

        if theme_location:
            theme = theme_location
        elif config.has_option("theme", "name"):
            try:
                theme_module = importlib.import_module(config.get("theme", "name"))
                # Try to get the path from the module
                if hasattr(theme_module, '__path__') and len(theme_module.__path__) > 0:
                    theme = theme_module.__path__[0]
                elif hasattr(theme_module, '__file__'):
                    theme = os.path.dirname(theme_module.__file__)
                else:
                    theme = None
            except (ImportError, ModuleNotFoundError):
                # If import fails, try other theme resolution methods
                theme = None

        # If theme is still None, try to get location from config
        if theme is None and config.has_option("theme", "location"):
            theme = config.get("theme", "location")

        # If still no theme, use default
        if theme is None:
            print("Cannot find theme in the config file. Using the default theme.")
            theme = str(files(__package__).joinpath("themes/default"))

        self.env = Environment(loader=FileSystemLoader(theme))

        self.reportfolder = filename+"_files"
        self.foldername = os.path.basename(filename)+"_files/"
        if not os.path.exists(self.reportfolder):
            os.makedirs(self.reportfolder)
        #self.reportfile= open(filename,"w")
        self.reportfile = filename
        self.meta.update(kwargs)
        self.items = []

    # Make an otter report work as a context manager
    def __enter__(self):
        """
        Execute this code when the context manager is created.

        Right now, Otter doesn't actually need anything to be done at the 
        creation of a context, but that should really change at some point in
        the future. The report is returned so that ``with report as r:`` works.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        When the context ends, the report needs to be rendered.
        """
        self.show()
        
    def __add__(self, item):
        return self.add(item)
        
    def add(self, item):
        if isinstance(item, HTMLElement):
            self.items.append(item)
        else:
            item_ = HTMLElement()
            item_ + item
            self.items.append(item_)
        return self

    def show(self):
        html = ''
        for item in self.items:
            html += repr(item)
        output_html = self.env.get_template('body.html').render(meta=self.meta, body=html)
        self._write(output_html)
        
    def _write(self, text):
        """
        Write the report to disk atomically, so that someone reading a report
        from a web server while a long job is still running never sees a
        half-written file. The directory is created if it doesn't exist.
        """
        directory = os.path.dirname(os.path.abspath(self.reportfile))
        os.makedirs(directory, exist_ok=True)

        # Keep the permissions of an existing report, or use the umask default,
        # so that the web server can still read the file (mkstemp makes it 0600).
        try:
            mode = stat.S_IMODE(os.stat(self.reportfile).st_mode)
        except FileNotFoundError:
            umask = os.umask(0)
            os.umask(umask)
            mode = 0o666 & ~umask

        fd, tmp = tempfile.mkstemp(dir=directory, prefix=".otter-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text)
            os.chmod(tmp, mode)
            os.replace(tmp, self.reportfile)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise
