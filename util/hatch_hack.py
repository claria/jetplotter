#!/usr/bin/python
import numpy as np
import matplotlib
import matplotlib.hatch as hatch
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Polygon, Patch, Rectangle
from matplotlib.legend_handler import HandlerPatch, HandlerNpoints, HandlerBase
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
        legline1 = Line2D(xdata, ydata*1.5)
        legline2 = Line2D(xdata, ydata*0.5)

        self.update_prop(legline1, orig_handle, legend)
        self.update_prop(legline2, orig_handle, legend)


        legline1.set_transform(trans)
        legline2.set_transform(trans)

        return [legline1, legline2]

class HandlerPatch2(HandlerBase):
    """
    Handler for Patch instances.
    """
    def __init__(self, **kw):
        HandlerBase.__init__(self, **kw)

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        p1 = Rectangle(xy=(-xdescent, -ydescent),
                       width=width, height=height)
        p2 = Rectangle(xy=(-xdescent, -ydescent),
                       width=width, height=height)
        self.update_prop(p1, orig_handle, legend)
        self.update_prop(p2, orig_handle, legend)
        p2.set_facecolor('none')
        p1.set_transform(trans)
        p2.set_transform(trans)
        return [p1,p2]


Legend.update_default_handler_map({ErrorLine2D: HandlerErrorLine2D()})
Legend.update_default_handler_map({Patch: HandlerPatch2()})
