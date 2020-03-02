.. otter documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Otter - A Python Report Generator
=================================

Otter is a package for Python which is designed to make outputting and managing the results of programs which may take a long time to run,
orwhich may produce a very large quantity of results.
It was designed for handling the output requirements of data analysis pipelines used in astrophysics,
but it's capable of handling a wide range of data outputs.

Otter is also highly customisable, and you can use the ``liquid`` templating language to produce new output templates.

Quick Example
-------------

Otter can be used to produce reports containing a mixture of prose, data, and figures with minimal code. 

.. image:: images/screenshot.jpg
	   :width: 800px

This report was generated with just a small number of lines of Python: ::

	   import otter
	   import otter.bootstrap as bt

	   report = otter.Otter("index.html", author="Daniel Williams", title="Test Page", author_email= "daniel.williams@ligo.org")


	   with report:
	       report + "#Section Title"

	       report + "Lorem ipsum dolor sit amet..."


	   with report:

	       row = bt.Row(3)

	   import numpy as np
	   import matplotlib.pyplot as plt

	   with report:
	       f, ax = plt.subplots(1,1)
	       x = np.linspace(0,10, 100)
	       ax.plot(x, np.sin(x))

	       row[1] + f

	       row[0] + {"mass": "1kg", "price": "$1000", "area": 400}

	       report + row

	   with report:
	       report + "##Subsection Header"
	       report + "Fusce vel lectus ultricies,... "  

Contents
========

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   formatting
   contributing
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

