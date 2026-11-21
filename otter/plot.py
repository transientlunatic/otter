"""
Implements an interface with the Matplotlib plotting library in order to add plots to a report.

Importing this module does not change the Matplotlib backend; figures are
rendered with ``Figure.savefig``, which does not need a particular backend.
"""

import base64

from io import BytesIO

_MIME_TYPES = {
    "png": "image/png",
    "svg": "image/svg+xml",
}


class Figure():
    """
    A Matplotlib figure, embedded in the report as a self-contained image.

    Parameters
    ----------
    figure : matplotlib.figure.Figure
       The figure to embed.
    filename : str, optional
       If given, the figure is also saved to this path.
    dpi : int
       The resolution of a PNG figure. Ignored for SVG.
    fmt : {'png', 'svg'}
       The image format. SVG is vector, so it stays sharp when zoomed and
       is usually smaller than a 300 dpi PNG for line plots.
    """
    def __init__(self, figure, filename=None, dpi=300, fmt="png"):
        if fmt not in _MIME_TYPES:
            raise ValueError(
                "fmt must be one of {}, not {!r}".format(sorted(_MIME_TYPES), fmt)
            )
        self.fmt = fmt
        self.image = BytesIO()
        figure.savefig(self.image, format=fmt, dpi=dpi)

        if filename is not None:
            figure.savefig(filename, format=fmt, dpi=dpi)

        self.bitstring = base64.b64encode(self.image.getvalue())

    def __repr__(self):
        return (
            """<img src="data:{};base64,{}" style="max-width: 100%;" class="img-responsive"/>"""
            .format(_MIME_TYPES[self.fmt], self.bitstring.decode("utf-8"))
        )

    # Marks the output as HTML so that it is not escaped when added to a report.
    __html__ = __repr__
