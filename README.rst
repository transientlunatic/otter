===============================
Otter
===============================


Otter is a simple HTML report generator for Python jobs. Otter was
designed to produce reports on long-running jobs on remote machines,
and send them to a web server, but it's able to process many different
outputs from Python scripts, and convert them into neat and readible HTML pages.

Otter makes use of Twitter Bootstrap to make an easily themed layout for its output.

* Free software: ISC license
* Documentation: https://code.daniel-williams.co.uk/otter/

Quick Example
-------------

Otter can be used to produce reports containing a mixture of prose, data, and figures with minimal code. 

.. image:: images/screenshot.jpg

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


Features
--------

* TODO Add support for pandas data tables
* TODO Add support for custom headers and footers

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
