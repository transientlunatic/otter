# -*- coding: utf-8 -*-

__author__ = 'Daniel Williams'
__email__ = 'daniel.williams@glasgow.ac.uk'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


from .otter import *
