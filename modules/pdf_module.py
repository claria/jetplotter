import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
import lhapdf
import fastnlo
from fastnlo import fastNLOLHAPDF
import numpy as np
import array

from modules.base_module import BaseModule
from util.root_tools import build_tgraph_from_lists

import logging
log = logging.getLogger('__name__')

def get_pdf(pdfset, q, flavour=21):
    """ Return the LHAPDF pdfset using errors."""

    pdfset = lhapdf.getPDFSet(pdfset)
    pdfs = pdfset.mkPDFs()

    xs = [x for x in np.logspace(-5, 0, 500)][:-1]
    xfxs = np.empty((len(xs), len(pdfs)))
    print flavour, q
    for imem in xrange(len(pdfs)):
        for ix, x in enumerate(xs):
            if flavour == 7:
                #DVAL 1-(-1)
                xfxs[ix,imem] = pdfs[imem].xfxQ(1, x, q) - pdfs[imem].xfxQ(-1, x, q)
            elif flavour == 8:
                #UVAL 2-(-2)
                xfxs[ix,imem] = pdfs[imem].xfxQ(2, x, q) - pdfs[imem].xfxQ(-2, x, q)
            elif flavour == 9:
                #Light sea: xS=2(xubar + xdbar + xsbar)
                xfxs[ix,imem] = 2* (pdfs[imem].xfxQ(-1, x, q) + pdfs[imem].xfxQ(-2, x, q) + pdfs[imem].xfxQ(-3, x, q))
            else:
                xfxs[ix,imem] = pdfs[imem].xfxQ(flavour, x, q)

    central = np.array([pdfset.uncertainty(xfxs[i]).central for i in range(len(xfxs))])
    errplus = np.array([pdfset.uncertainty(xfxs[i]).errplus for i in range(len(xfxs))])
    errminus = np.array([pdfset.uncertainty(xfxs[i]).errminus for i in range(len(xfxs))])

    return xs, central, errminus, errplus 

def get_pdf(pdfset, q, flavour=21, errortype='auto', start_member=None, end_member=None):
    """ Return the LHAPDF pdfset using errors."""

    pdfset = lhapdf.getPDFSet(pdfset)
    pdfs = pdfset.mkPDFs()

    if start_member is None:
        start_member = 0
    if end_member is None:
        end_member = len(pdfs)

    xs = [x for x in np.logspace(-5, 0, 500)][:-1]
    xfxs = np.empty((len(xs), len(pdfs)))
    print flavour, q
    for imem in xrange(len(pdfs)):
        for ix, x in enumerate(xs):
            if flavour == 7:
                #DVAL 1-(-1)
                xfxs[ix,imem] = pdfs[imem].xfxQ(1, x, q) - pdfs[imem].xfxQ(-1, x, q)
            elif flavour == 8:
                #UVAL 2-(-2)
                xfxs[ix,imem] = pdfs[imem].xfxQ(2, x, q) - pdfs[imem].xfxQ(-2, x, q)
            elif flavour == 9:
                #Light sea: xS=2(xubar + xdbar + xsbar)
                xfxs[ix,imem] = 2* (pdfs[imem].xfxQ(-1, x, q) + pdfs[imem].xfxQ(-2, x, q) + pdfs[imem].xfxQ(-3, x, q))
            else:
                xfxs[ix,imem] = pdfs[imem].xfxQ(flavour, x, q)

    if errortype == 'auto':
        central = np.array([pdfset.uncertainty(xfxs[i]).central for i in range(len(xfxs))])
        errplus = np.array([pdfset.uncertainty(xfxs[i]).errplus for i in range(len(xfxs))])
        errminus = np.array([pdfset.uncertainty(xfxs[i]).errminus for i in range(len(xfxs))])
    elif errortype == 'eig':
        central = xfxs.T[0]
        errplus = np.zeros(central.shape)
        errminus = np.zeros(central.shape)
        for i in range(start_member, end_member): 
                errplus += np.square(np.maximum(xfxs.T[i]-xfxs.T[0], 0.0))
                errminus += np.square(np.minimum(xfxs.T[i]-xfxs.T[0], 0.0))

        errplus = np.sqrt(errplus)
        errminus = np.sqrt(errminus)

    elif errortype == 'envelope':
        central = xfxs.T[0]
        errplus = np.zeros(central.shape)
        errminus = np.zeros(central.shape)
        for i in range(start_member, end_member): 
                errplus = np.maximum(xfxs.T[i]-xfxs.T[0], errplus)
                errminus = np.maximum(xfxs.T[0]-xfxs.T[i], errminus)
    else:
        raise ValueError('The passed errortype is not known.')

    return xs, central, errminus, errplus 



def get_correlation(pdfset_name, fnlo_table, flavour=21):
    """ Return the correlation between the fnlo table in a bin vs. pdfset flavour."""

    pdfset = lhapdf.getPDFSet(pdfset_name)
    pdfs = pdfset.mkPDFs()
    print fnlo_table
    fnlo = fastNLOLHAPDF(str(fnlo_table), str(pdfset_name))

    xs_binedges = np.array([x for x in np.logspace(-5, 0, 500)])
    xs = xs_binedges[:-1] + (xs_binedges[1:] - xs_binedges[:-1])/2.
    qvals = np.array(fnlo.GetQScales(1))
    crosssection = np.empty((len(pdfs), fnlo.GetNObsBin()))
    xfxs = np.empty((len(xs), len(qvals), len(pdfs), ))
    for imem in xrange(len(pdfs)):
        fnlo.SetLHAPDFMember(imem)
        fnlo.CalcCrossSection()
        crosssection[imem] = np.array(fnlo.GetCrossSection())

    for ix, x in enumerate(xs):
        for imem in xrange(len(pdfs)):
            for iq, q in enumerate(qvals):
                xfxs[ix, iq, imem] = pdfs[imem].xfxQ(flavour, x, q)


    corr = np.empty((len(xs), len(qvals)))
    for ix, x in enumerate(xs):
        for iq, q in enumerate(qvals):
            corr[ix, iq] = pdfset.correlation(crosssection.T[iq], xfxs[ix,iq])
    return xs_binedges, range(len(qvals)+1), corr


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
                help='Input a LHAPDF 6 pdf set. id:pdfset=CT10nlo|flavour=21|q=100')

    def __call__(self, config):
        for id, settings in config['input_pdfsets']:
            pdfset = settings.get('pdfset', '')
            flavour = settings.get('flavour', 21)
            q = settings.get('q', 10)
            errortype = settings.get('errortype', 'auto')
            start_member = settings.get('start_member', None)
            end_member = settings.get('end_member', None)
            xs, central, down, up = get_pdf(pdfset, q, flavour, errortype=errortype, start_member=start_member, end_member=end_member)
            graph = build_tgraph_from_lists(xs, central, yerrl=down, yerru=up)
            config['objects'].setdefault(id, {})['obj'] = graph




class PDFCorrelationModule(BaseModule):
    """ The PDF sets are read from the LHAPDF file and converted into a TGraph using
        errors. The predefined error calculation method of LHAPDF is used to determine
        the PDF uncertainties.

        Requires that LHAPDF is installed and that the correct PYTHONPATH is set to include
        the LHAPDF library.

        Options:
          --input-pdfsets id:pdfset=Ct10nlo?flavour=21?q=100.0
    """

    def __init__(self):
        super(PDFCorrelationModule, self).__init__()
        self.arg_group.add_argument('--input-pdfcorr', nargs='+', type='str2kvdict',
                help='Input a LHAPDF 6 pdf set. id:pdfset=CT10nlo|flavour=21|q=100')

    def __call__(self, config):
        for id, settings in config['input_pdfcorr']:
            pdfset = settings.get('pdfset', '')
            fnlotable = settings.get('fnlotable', '')
            flavour = settings.get('flavour', 21)
            x, q, corr = get_correlation(pdfset, fnlotable, flavour)
            print corr
            x_bins = array.array('d', x) 
            q_bins = array.array('d', q) 
            corr_histo = ROOT.TH2D('pdf_corr', 'pdf_corr', len(x_bins) -1, x_bins, len(q_bins) -1, q_bins)
            print len(x_bins)
            print len(q_bins)
            for i in range(len(x_bins)-1):
                for j in range(len(q_bins)-1):
                    # print i, j
                    corr_histo.SetBinContent(i,j, corr[i,j])
            config['objects'].setdefault(id, {})['obj'] = corr_histo


