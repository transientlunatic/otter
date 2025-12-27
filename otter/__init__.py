# -*- coding: utf-8 -*-

__author__ = 'Daniel Williams'
__email__ = 'daniel.williams@glasgow.ac.uk'

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("otter-report")
except PackageNotFoundError:
    # Package is not installed (e.g., during development); try setuptools_scm as a fallback.
    try:
        from setuptools_scm import get_version
        __version__ = get_version(root="..", relative_to=__file__)
    except Exception:
        __version__ = "unknown"


from .otter import *
