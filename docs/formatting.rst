.. _advancedformatting:

=========================
Advanced Formatting Guide
=========================

Otter is capable of using features from the Twitter Bootstrap library
to produce reports with more complicated formatting, such as columns
and boxes.

Starting with a basic report,::

  import otter
  import otter.bootstrap as bt

  report = otter.Otter(filename="test.html")

we can start by adding a ``bt.Row``. These are the building-blocks of a bootstrap-based layout. Here we'll make one with three columns.::

  row = bt.Row(cols=3)
  row[1] + "This is some text for the middle column"

  with report:
     report + row
  
We can then add text, data, or plots to each of the three columns in the same way as the text was added to the 1st column above, and in the same way that we could do without the additional formatting instructions for columns.
  
  
