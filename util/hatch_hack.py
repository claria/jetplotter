#!/usr/bin/python
import numpy as np
import matplotlib
import matplotlib.hatch as hatch
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
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
