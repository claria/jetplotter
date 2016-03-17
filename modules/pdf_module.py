import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import numpy as np
import os
import sys
import array

import lhapdf

from modules.base_module import BaseModule
from util.root_tools import build_tgraph_from_lists
from util.pdf import PDF

import logging
log = logging.getLogger('__name__')


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
            q2 = settings.get('q2', 2)

            pdf = PDF(pdfset, flavors=[flavour], q2=q2)

            x = pdf.get_x()
            y = pdf.get_pdf_central(flavour)
            pdf_unc = pdf.get_pdf_uncert(flavour)

            graph = build_tgraph_from_lists(x, y, yerrl=pdf_unc[0], yerru=pdf_unc[1])
            config['objects'].setdefault('{0}'.format(id), {})['obj'] = graph

            if pdf._has_var:
                mod_unc = pdf.get_mod_uncert(flavour)
                graph = build_tgraph_from_lists(x, y, yerrl=mod_unc[0], yerru=mod_unc[1])
                config['objects'].setdefault('_{0}_modunc'.format(id), {})['obj'] = graph

                par_unc = pdf.get_par_uncert(flavour)
                graph = build_tgraph_from_lists(x, y, yerrl=par_unc[0], yerru=par_unc[1])
                config['objects'].setdefault('_{0}_modunc'.format(id), {})['obj'] = graph

                modexp_unc = np.sqrt(np.square(mod_unc) + np.square(pdf_unc))

                graph = build_tgraph_from_lists(x, y, yerrl=modexp_unc[0], yerru=modexp_unc[1])
                config['objects'].setdefault('_{0}_modexpunc'.format(id), {})['obj'] = graph

                tot_unc = np.sqrt(np.square(pdf_unc) + np.square(mod_unc) + np.square(par_unc))

                graph = build_tgraph_from_lists(x, y, yerrl=tot_unc[0], yerru=tot_unc[1])
                config['objects'].setdefault('_{0}_totunc'.format(id), {})['obj'] = graph



