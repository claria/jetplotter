import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
import lhapdf
import numpy as np

from modules.base_module import BaseModule
from util.root_tools import build_tgraph_from_lists

import logging
log = logging.getLogger('__name__')

def get_pdf(pdfset, q, flavour=21):
    """ Return the LHAPDF pdfset using errors."""

    pdfset = lhapdf.getPDFSet(pdfset)
    pdfs = pdfset.mkPDFs()

    xs = [x for x in np.logspace(-5, 0, 500)]
    xfxs = np.empty((len(xs), len(pdfs)))
    for imem in xrange(len(pdfs)):
        for ix, x in enumerate(xs):
            xfxs[ix,imem] = pdfs[imem].xfxQ(flavour, x, q)

    central = np.array([pdfset.uncertainty(xfxs[i]).central for i in range(len(xfxs))])
    errplus = np.array([pdfset.uncertainty(xfxs[i]).errplus for i in range(len(xfxs))])
    errminus = np.array([pdfset.uncertainty(xfxs[i]).errminus for i in range(len(xfxs))])

    return xs, central, errminus, errplus 

def get_correlation(pdfset, fnlo_table, flavour=21):
    """ Return the correlation between the fnlo table in a bin vs. pdfset flavour."""

    pdfset = lhapdf.getPDFSet(pdfset)
    pdfs = pdfset.mkPDFs()

    xs = [x for x in np.logspace(-5, 0, 500)]
    xfxs = np.empty((len(xs), len(pdfs)))
    for imem in xrange(len(pdfs)):
        for ix, x in enumerate(xs):
            xfxs[ix,imem] = pdfs[imem].xfxQ(flavour, x, q)

    central = np.array([pdfset.uncertainty(xfxs[i]).central for i in range(len(xfxs))])
    errplus = np.array([pdfset.uncertainty(xfxs[i]).errplus for i in range(len(xfxs))])
    errminus = np.array([pdfset.uncertainty(xfxs[i]).errminus for i in range(len(xfxs))])

    return xs, central, errminus, errplus 


class PDFModule(BaseModule):
    """ The PDF sets are read from the LHAPDF file and converted into a TGraph using
        errors. The predefined error calculation method of LHAPDF is used to determine
        the PDF uncertainties.

        Requires that LHAPDF is installed and that the correct PYTHONPATH is set to include
        the LHAPDF library.

        Options:
          --input-pdfsets id:pdfset=Ct10nlo?flavour=21?q=100.0
    """

    def __init__(self):
        super(PDFModule, self).__init__()
        self.arg_group.add_argument('--input-pdfsets', nargs='+', type='str2kvdict',
                help='Input a LHAPDF 6 pdf set. id:pdfset=CT10nlo?flavour=21?q=100')

    def __call__(self, config):
        for id, settings in config['input_pdfsets']:
            pdfset = settings.get('pdfset', '')
            flavour = settings.get('flavour', 21)
            q = settings.get('q', 10)
            xs, central, down, up = get_pdf(pdfset, flavour, q)
            graph = build_tgraph_from_lists(xs, central, yerrl=down, yerru=up)
            config['objects'].setdefault(id, {})['obj'] = graph


