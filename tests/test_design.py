"""Tests for object dispatch, escaping, figure embedding and report writing."""

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from collections import OrderedDict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from otter import otter, html, plot
from otter import bootstrap as bt


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "report.html")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def render(self, obj):
        report = otter.Otter(self.test_file, title="T")
        report + obj
        report.show()
        with open(self.test_file, encoding="utf-8") as f:
            return f.read()


class TestDispatch(TempDirCase):
    def test_dict_subclass_is_rendered_as_table(self):
        content = self.render(OrderedDict(alpha="one"))
        self.assertIn("<table", content)
        self.assertIn("alpha", content)

    def test_custom_subclass_of_registered_type(self):
        class MyList(list):
            pass
        self.assertIn("<ol", self.render(MyList(["a", "b"])))

    def test_repr_html_protocol(self):
        class Thing:
            def _repr_html_(self):
                return "<b id='thing'>hello</b>"
        self.assertIn("<b id='thing'>hello</b>", self.render(Thing()))

    def test_repr_html_returning_none_falls_back_to_text(self):
        class Thing:
            def _repr_html_(self):
                return None
            def __str__(self):
                return "plain"
        self.assertIn("plain", self.render(Thing()))

    def test_html_protocol_is_trusted(self):
        class Safe:
            def __html__(self):
                return "<i>trusted</i>"
        self.assertIn("<i>trusted</i>", self.render(Safe()))

    def test_unknown_objects_are_escaped(self):
        class Evil:
            def __str__(self):
                return "<script>alert(1)</script>"
        content = self.render(Evil())
        self.assertNotIn("<script>alert(1)</script>", content)
        self.assertIn("&lt;script&gt;", content)

    def test_numbers_render(self):
        self.assertIn("42", self.render(42))

    def test_register_handler(self):
        class Money:
            def __init__(self, v):
                self.v = v
        html.register_handler(Money, lambda m: "<span class='money'>{}</span>".format(m.v))
        try:
            self.assertIn("<span class='money'>5</span>", self.render(Money(5)))
        finally:
            del html.handlers[Money]

    def test_raw_html(self):
        content = self.render(html.RawHTML("<div id='d3-target'></div><script>1+1</script>"))
        self.assertIn("<div id='d3-target'></div><script>1+1</script>", content)


class TestElements(unittest.TestCase):
    def test_multiple_attributes_are_separated(self):
        out = repr(html.Table(cl="a", id="b"))
        self.assertIn("<table class='a' id='b'>", out)

    def test_attribute_values_are_escaped(self):
        out = repr(html.Table(title="x' onclick='evil"))
        self.assertNotIn("onclick='evil", out)

    def test_iadd_returns_the_element(self):
        el = html.HTMLElement()
        el += "text"
        self.assertIsInstance(el, html.HTMLElement)
        self.assertIn("text", repr(el))

    def test_multi_column_row_rejects_direct_add(self):
        with self.assertRaises(ValueError):
            bt.Row(3) + "text"

    def test_single_column_row_accepts_direct_add(self):
        row = bt.Row(1)
        row + "text"
        self.assertIn("text", repr(row))


class TestFigures(TempDirCase):
    def tearDown(self):
        plt.close("all")
        super().tearDown()

    def make_figure(self):
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        return fig

    def test_png_embedded_by_default(self):
        content = self.render(self.make_figure())
        self.assertIn("data:image/png;base64,", content)

    def test_figure_subclass_is_handled(self):
        class MyFigure(matplotlib.figure.Figure):
            pass
        fig = plt.figure(FigureClass=MyFigure)
        self.assertIn("data:image/png;base64,", self.render(fig))

    def test_svg(self):
        content = self.render(plot.Figure(self.make_figure(), fmt="svg"))
        self.assertIn("data:image/svg+xml;base64,", content)

    def test_bad_format_rejected(self):
        with self.assertRaises(ValueError):
            plot.Figure(self.make_figure(), fmt="gif")

    def test_filename_saves_file_and_still_embeds(self):
        path = os.path.join(self.test_dir, "fig.png")
        content = self.render(plot.Figure(self.make_figure(), filename=path))
        self.assertTrue(os.path.getsize(path) > 0)
        self.assertIn("data:image/png;base64,", content)

    def test_importing_otter_does_not_force_a_backend(self):
        code = (
            "import matplotlib; matplotlib.use('svg'); import otter; "
            "assert matplotlib.get_backend().lower() == 'svg', matplotlib.get_backend()"
        )
        subprocess.run([sys.executable, "-c", code], check=True)


class TestWriting(TempDirCase):
    def test_context_manager_returns_report(self):
        report = otter.Otter(self.test_file)
        with report as r:
            self.assertIs(r, report)

    def test_report_written_on_exit(self):
        report = otter.Otter(self.test_file, title="T")
        with report:
            report + "# Heading"
        self.assertTrue(os.path.exists(self.test_file))

    def test_no_temporary_files_left_behind(self):
        report = otter.Otter(self.test_file)
        report + "text"
        report.show()
        report.show()
        leftovers = [f for f in os.listdir(self.test_dir) if f.endswith(".tmp")]
        self.assertEqual(leftovers, [])

    def test_failed_write_keeps_previous_report(self):
        report = otter.Otter(self.test_file)
        report + "first"
        report.show()
        class Bad:
            def encode(self, *a):
                raise RuntimeError
        with self.assertRaises(Exception):
            report._write(Bad())
        with open(self.test_file) as f:
            self.assertIn("first", f.read())
        self.assertEqual([f for f in os.listdir(self.test_dir) if f.endswith(".tmp")], [])

    @unittest.skipIf(os.name == "nt", "POSIX permissions")
    def test_report_is_readable_like_a_normal_file(self):
        report = otter.Otter(self.test_file)
        report + "text"
        report.show()
        mode = stat.S_IMODE(os.stat(self.test_file).st_mode)
        self.assertNotEqual(mode, 0o600)

    def test_missing_parent_directory_is_created(self):
        nested = os.path.join(self.test_dir, "a", "b", "report.html")
        report = otter.Otter(nested)
        report + "text"
        report.show()
        self.assertTrue(os.path.exists(nested))


if __name__ == "__main__":
    unittest.main()
