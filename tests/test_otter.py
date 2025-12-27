#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_otter
----------------------------------

Tests for `otter` module.
"""

import unittest
import tempfile
import os
import shutil

from otter import otter
from otter import html
from otter import bootstrap as bt


class TestOtterBasics(unittest.TestCase):
    """Test basic Otter functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_report.html")

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            try:
                shutil.rmtree(self.test_dir)
            except (OSError, PermissionError):
                # On some platforms (e.g., Windows), files may not be released immediately.
                import time
                time.sleep(0.1)
                shutil.rmtree(self.test_dir)

    def test_otter_creation(self):
        """Test that an Otter report can be created."""
        report = otter.Otter(self.test_file, title="Test Report")
        self.assertIsInstance(report, otter.Otter)
        self.assertEqual(report.reportfile, self.test_file)

    def test_otter_creates_folder(self):
        """Test that Otter creates a folder for report files."""
        report = otter.Otter(self.test_file)
        self.assertTrue(os.path.exists(report.reportfolder))

    def test_otter_context_manager(self):
        """Test that Otter works as a context manager."""
        report = otter.Otter(self.test_file, title="Test Report")
        report + "# Test Heading"
        report + "This is a test paragraph."
        report.show()
        
        # Check that the file was created
        self.assertTrue(os.path.exists(self.test_file))
        
        # Check that the file contains content
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn("Test Heading", content)

    def test_otter_add_content(self):
        """Test adding content to Otter report."""
        report = otter.Otter(self.test_file, title="Test Report")
        report.add("Test content")
        self.assertEqual(len(report.items), 1)


class TestHTMLElement(unittest.TestCase):
    """Test HTML element functionality."""

    def test_html_element_creation(self):
        """Test that an HTML element can be created."""
        element = html.HTMLElement("Test content")
        self.assertIsInstance(element, html.HTMLElement)

    def test_html_element_repr(self):
        """Test HTML element string representation."""
        element = html.HTMLElement("Test")
        output = repr(element)
        self.assertIn("Test", output)

    def test_ordered_list(self):
        """Test ordered list creation."""
        ol = html.OrderedList()
        ol + ["Item 1", "Item 2", "Item 3"]
        output = repr(ol)
        self.assertIn("<ol", output)
        self.assertIn("<li>", output)
        self.assertIn("Item 1", output)

    def test_table_creation(self):
        """Test table creation."""
        table = html.Table()
        self.assertIsInstance(table, html.Table)
        output = repr(table)
        self.assertIn("<table", output)

    def test_dict_to_table(self):
        """Test dictionary to table conversion."""
        test_dict = {"key1": "value1", "key2": "value2"}
        table = html.dict_to_table(test_dict)
        output = repr(table)
        self.assertIn("key1", output)
        self.assertIn("value1", output)


class TestBootstrap(unittest.TestCase):
    """Test Bootstrap components."""

    def test_row_creation_with_int(self):
        """Test creating a row with integer columns."""
        row = bt.Row(3)
        self.assertEqual(len(row.columns), 3)

    def test_row_creation_with_list(self):
        """Test creating a row with list of column widths."""
        # Providing an iterable hclass is required when cols is a list
        row = bt.Row([4, 4, 4], hclass=['', '', ''])
        self.assertEqual(len(row.columns), 3)

    def test_row_repr(self):
        """Test row string representation."""
        row = bt.Row(2)
        output = repr(row)
        self.assertIn("<div class='row'>", output)
        self.assertIn("</div>", output)

    def test_column_creation(self):
        """Test creating a column."""
        col = bt.Column(width=6, size="md")
        self.assertEqual(col.width, 6)
        self.assertEqual(col.size, "md")

    def test_container_creation(self):
        """Test creating a container."""
        container = bt.Container()
        self.assertIsInstance(container, bt.Container)
        output = repr(container)
        self.assertIn("<div class='container'>", output)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
