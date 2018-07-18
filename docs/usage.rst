.. _quickstart:
=================
Quick Start Guide
=================

To use Otter in a project you'll need to start by importing the package::

  import otter

Once we've done that, we can set up the report. When you do this you'll, as a very minimum requirement, need to know where the report should be saved. So, for example, if we wanted to produce a report in the present working directory (the same place that the Python script is running), we can set up a report like so::

  report = otter.Otter(filename="test.html")

An ``HTML`` formatted report called ``test.html`` will now be produced in the working directory. We can specify any allowed filepath on the machine, however, so something like::

  report = otter.Otter(filename="/home/daniel/www/important.html")

can be used to place the report in a specific directory. This can be a useful way of making sure that your reports are placed in a location which is web-accessible, which can be useful if you're working on a remote machine, or a computing cluster, for example.


We can add additional metadata to the report, such as the name of the author, and a title for the report. Some data might be ignored, and the metadata which is used to generate the report is dependent upon the template which you're using.::

  report = otter.Otter(filename="test.html", author="Daniel Williams", title="Test Report")

Once we've set-up the report, we can start adding content to it. We recommend doing this using a context manager, which means that a report is still produced, even if a problem causes your code to stop executing prematurely. This can be done using the ``with`` statement in Python: ::

  report = otter.Otter(filename="test.html")

  with report:
     report + "This is a sentence to add to the report."

This method of making the report means that you don't need to worry about explicitly writing-out the report; it's done automatically as we move through your script.

When you add a string to the report it will just get added to the text. We can produce more useful formatting as well, which is covered in the :ref:`formatting` tutorial, but simple formatting can be performed by including Markdown in the string. For example, ::

  with report:
     report + "#Heading"

will be parsed from Markdown to add a level-one heading to the document. You can review markdown syntax with this `Markdown primer <https://help.gamejolt.com/markdown>`_.

## Plots and Data

Otter can also handle the process of adding plots produced by ``matplotlib`` to your report. For example ::

  x = np.linspace(0,10, 100)
  y = np.sin(x)

  f, ax = plt.subplots(1,1)
  ax.plot(x,y)


  with report:
     report + f

This will add a plot of a sinusoid to the report.

Otter will automatically try and handle a number of other data formats automatically, and make them
aesthetically pleasing. Dictionaries get turned into tables, for example, as do numpy arrays, while lists are turned into HTML lists.

