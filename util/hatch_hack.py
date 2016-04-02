#!/usr/bin/python
import numpy as np
import matplotlib
import matplotlib.hatch as hatch
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Polygon, Patch
from matplotlib.legend_handler import HandlerPatch, HandlerNpoints
from matplotlib.legend import Legend
from matplotlib.path import Path

class ThickNorthEastHatch(hatch.HatchPatternBase):
    def __init__(self, hatch, density):
        self.num_lines = int((hatch.count('s') + hatch.count('x') +
                          hatch.count('X')) * density)
        print(density)
        self.thickness = int(hatch.count('l'))/72.
        if self.num_lines:
            self.num_vertices = (self.num_lines + 1) * 5
        else:
            self.num_vertices = 0

    def set_vertices_and_codes(self, vertices, codes):
        steps = np.linspace(-0.5, 0.5, self.num_lines + 1, True)
        vertices[0::5, 0] = 0.0 + steps
        vertices[0::5, 1] = 0.0 - steps

        vertices[1::5, 0] = 1.0 + steps
        vertices[1::5, 1] = 1.0 - steps
        vertices[2::5, 0] = 1.0 + steps + self.thickness
        vertices[2::5, 1] = 1.0 - steps
        vertices[3::5, 0] = 0.0 + steps + self.thickness
        vertices[3::5, 1] = 0.0 - steps
        vertices[4::5, 0] = 0.0 + steps
        vertices[4::5, 1] = 0.0 - steps

        codes[0::5] = Path.MOVETO
        codes[1::5] = Path.LINETO
        codes[2::5] = Path.LINETO
        codes[3::5] = Path.LINETO
        codes[4::5] = Path.LINETO

matplotlib.hatch._hatch_types.append(ThickNorthEastHatch)


class HandlerPatch2(HandlerPatch):

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        p = self._create_patch(legend, orig_handle,
                               xdescent, ydescent, width, height, fontsize)
        self.update_prop(p, orig_handle, legend)
        # p.set_fill(True)
        p.set_hatch('slll')
        p.set_transform(trans)
        return [p]

    def legend_artist(self, legend, orig_handle,
                       fontsize, handlebox):
        """
        Return the artist that this HandlerBase generates for the given
        original artist/handle.
        Parameters
        ----------
        legend : :class:`matplotlib.legend.Legend` instance
            The legend for which these legend artists are being created.
        orig_handle : :class:`matplotlib.artist.Artist` or similar
            The object for which these legend artists are being created.
        fontsize : float or int
            The fontsize in pixels. The artists being created should
            be scaled according to the given fontsize.
        handlebox : :class:`matplotlib.offsetbox.OffsetBox` instance
            The box which has been created to hold this legend entry's
            artists. Artists created in the `legend_artist` method must
            be added to this handlebox inside this method.
        """
        xdescent, ydescent, width, height = self.adjust_drawing_area(
                 legend, orig_handle,
                 handlebox.xdescent, handlebox.ydescent,
                 handlebox.width, handlebox.height,
                 fontsize)
        artists = self.create_artists(legend, orig_handle,
                                      xdescent, ydescent, width, height,
                                      fontsize, handlebox.get_transform())

        # create_artists will return a list of artists.
        for a in artists:
            handlebox.add_artist(a)
            a.set_rasterized(True)

        return artists[0]




# Legend.update_default_handler_map({Patch: HandlerPatch2()})

class ErrorLine2D(Line2D):
    pass

class HandlerErrorLine2D(HandlerNpoints):
    """
    Handler for Line2D instances.
    """
    def __init__(self, marker_pad=0.3, numpoints=None, **kw):
        HandlerNpoints.__init__(self, marker_pad=marker_pad, numpoints=numpoints, **kw)

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        xdata, xdata_marker = self.get_xdata(legend, xdescent, ydescent,
                                             width, height, fontsize)

        ydata = ((height - ydescent) / 2.) * np.ones(xdata.shape, float)
        legline1 = Line2D(xdata, ydata*1.4)
        legline2 = Line2D(xdata, ydata*0.6)

        self.update_prop(legline1, orig_handle, legend)
        self.update_prop(legline2, orig_handle, legend)


        legline1.set_transform(trans)
        legline2.set_transform(trans)

        return [legline1, legline2]


Legend.update_default_handler_map({ErrorLine2D: HandlerErrorLine2D()})
