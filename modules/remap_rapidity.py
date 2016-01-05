import collections
import logging

import ROOT
from ROOT import TGraphErrors

from modules.base_module import BaseModule
from util.root_tools import get_tgraphasymm_from_histos

log = logging.getLogger(__name__)

class RemapRapidity(BaseModule):
    """Calls the Project3D function."""

    def __init__(self):
        super(RemapRapidity, self).__init__()
        self.arg_group.add_argument('--remap', nargs='+', type=str, default=[], help='')

    def __call__(self, config):
        for id in config['remap']:
            obj = config['objects'][id]['obj']

            tg_orig = TGraphErrors(obj)

            tg_remap = tg_orig.Clone('remap_tgraph')

            for i in xrange(tg_orig.GetN()):
                origX, origY = ROOT.Double(0), ROOT.Double(0)
                tg_orig.GetPoint(i, origX, origY)

                remapX = origX + origY
                remapY = origX
                tg_remap.SetPoint(i, remapX, remapY)


            config['objects'][id]['obj'] = tg_remap

class RemapRapidity2D(BaseModule):
    """Calls the Project3D function."""

    def __init__(self):
        super(RemapRapidity2D, self).__init__()
        self.arg_group.add_argument('--remap', nargs='+', type=str, default=[], help='')

    def __call__(self, config):
        for id in config['remap']:
            obj = config['objects'][id]['obj']

            nbins = obj.GetNbinsX() * obj.GetNbinsY()
            print obj.GetXaxis().GetXbins()
            # h2_new = ROOT.TH2D('blah', 'blah',
                               # obj.GetXaxis().GetNbins(), obj.GetXaxis().GetXbins(),
                               # obj.GetXaxis().GetNbins(), obj.GetXaxis().GetXbins())
            h2_new = obj.ProjectionXY()
            ROOT.SetOwnership(h2_new, 0)

            for x in xrange(1, obj.GetNbinsX() + 1):
                for y in xrange(1, obj.GetNbinsY() + 1):
                    xval = obj.GetXaxis().GetBinCenter(x)
                    yval = obj.GetYaxis().GetBinCenter(y) + obj.GetBinContent(x,y)
                    zval = obj.GetYaxis().GetBinCenter(y)

                    # h2_new.SetPoint(h2_new.GetN(), xval, yval, zval)
                    i = h2_new.FindBin(xval, yval)
                    print xval, yval, zval
                    h2_new.SetBinContent(i, zval)
                    h2_new.SetBinError(i, 0.)

            config['objects'][id]['obj'] = h2_new
            h2_new.Print('all')
