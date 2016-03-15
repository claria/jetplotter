# make sure you have the correct imports,
# they may differ depending on the matplotlib version
import matplotlib.backends.backend_pdf
from matplotlib.backends.backend_pdf import Name, Op
from matplotlib.transforms import Affine2D, Bbox, BboxBase, TransformedPath
from matplotlib.path import Path

def setCustomHatchWidth(customWidth):

    def _writeHatches(self):
        hatchDict = dict()
        sidelen = 72.0
        for hatch_style, name in self.hatchPatterns.iteritems():
            ob = self.reserveObject('hatch pattern')
            hatchDict[name] = ob
            res = { 'Procsets':
                    [ Name(x) for x in "PDF Text ImageB ImageC ImageI".split() ] }
            self.beginStream(
                ob.id, None,
                { 'Type': Name('Pattern'),
                  'PatternType': 1, 'PaintType': 1, 'TilingType': 1,
                  'BBox': [0, 0, sidelen, sidelen],
                  'XStep': sidelen, 'YStep': sidelen,
                  'Resources': res })

            # lst is a tuple of stroke color, fill color,
            # number of - lines, number of / lines,
            # number of | lines, number of \ lines
            rgb = hatch_style[0]
            self.output(rgb[0], rgb[1], rgb[2], Op.setrgb_stroke)
            if hatch_style[1] is not None:
                rgb = hatch_style[1]
                self.output(rgb[0], rgb[1], rgb[2], Op.setrgb_nonstroke,
                            0, 0, sidelen, sidelen, Op.rectangle,
                            Op.fill)

            self.output(customWidth, Op.setlinewidth)

            # TODO: We could make this dpi-dependent, but that would be
            # an API change
            self.output(*self.pathOperations(
                    Path.hatch(hatch_style[2]),
                    Affine2D().scale(sidelen),
                    simplify=False))
            self.output(Op.stroke)

            self.endStream()
            self.writeObject(self.hatchObject, hatchDict)
    matplotlib.backends.backend_pdf.PdfFile.writeHatches = _writeHatches
