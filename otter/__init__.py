# -*- coding: utf-8 -*-

__author__ = 'Daniel Williams'
__email__ = 'daniel.williams@glasgow.ac.uk'

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Python < 3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("otter-report")
except PackageNotFoundError:
    # Package is not installed
    __version__ = "unknown"


from .otter import *
