import logging

import ROOT

from modules.base_module import BaseModule
from modules.helpers import get_tgrapherrors

log = logging.getLogger(__name__)


class ResolutionAna(BaseModule):
    """ Fits the resolution from a TH2D assuming gaussian errors. """

    def __init__(self):
        super(ResolutionAna, self).__init__()
        self.arg_group.add_argument('--resolution', nargs='+', default=[], help='')

    def __call__(self, config):
        ROOT.TVirtualFitter.SetMaxIterations(9999)
        res_pars = {}
        for id in config['resolution']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            gen_bins = config['objects'][id]['obj'].GetNbinsY()
            resolution_graph = ROOT.TGraphErrors(gen_bins)
            for i in xrange(1, gen_bins + 1):
                # Get slice of 2d histogram
                pt_bin_obj = config['objects'][id]['obj'].ProjectionX("{0}_slice_{1}".format(id, i), i, i)
                # Continue if histogram if empty
                if pt_bin_obj.GetEntries() < 1:
                    continue
                # If fit fails continue instead of failing
                id_slice = '_{0}_slice_{1}'.format(id.strip('_'), i)
                res = pt_bin_obj.Fit("gaus", "SQO")
                fcn = pt_bin_obj.GetFunction("gaus")
                if res.Get() == None or res.Status() != 0:
                    continue
                xmin, xmax = pt_bin_obj.GetXaxis().GetXmin(), pt_bin_obj.GetXaxis().GetXmax()
                vfitter = ROOT.TVirtualFitter.GetFitter()
                fcn.SetNpx(1000)
                fcn.SetRange(xmin, xmax)
                error_graph = get_tgrapherrors(fcn, vfitter)

                # Omit bin with too large errors > 5%
                if (fcn.GetParError(2) / fcn.GetParameter(2)) > 0.05:
                    continue
                # Uncomment to save also individual gauss fits to dict
                config['objects'].setdefault(id_slice, {})
                config['objects'][id_slice]['obj'] = pt_bin_obj
                config['objects'].setdefault('{0}_fit'.format(id_slice), {})
                config['objects']['{0}_fit'.format(id_slice)]['obj'] = error_graph
                resolution_graph.SetPoint(i, config['objects'][id]['obj'].GetYaxis().GetBinCenter(i),
                                          fcn.GetParameter(2))
                resolution_graph.SetPointError(i, config['objects'][id]['obj'].GetYaxis().GetBinWidth(i) / 2.,
                                               fcn.GetParError(2))
            # Store TGraph and fit TGraph
            id_res = 'resolution_{0}'.format(id.strip('_'))
            config['objects'].setdefault(id_res, {})
            config['objects'][id_res]['obj'] = resolution_graph

            res_fcn = ROOT.TF1("res_fcn", "sqrt(TMath::Sign(1.,[0])*([0]/x)**2 + (([1]**2)/x)*(x**[3]) + [2]**2)")
            # res_fcn = ROOT.TF1("res_fcn", "sqrt(TMath::Sign(1.,[0])*([0]/x)**2 + (([1]**2)/x) + [2]**2)")
            # res_fcn = ROOT.TF1("res_fcn", "sqrt(TMath::Sign(1.,[0])*([0]**2) + ((x)**[1])*([2]**2/x) + [3]**2)")
            res_fcn.SetParameters(5., 1.0, 0.03, -0.5)
            res_fcn.SetRange(0., 9999.)
            print 'Fitting id {0}'.format(id_res)
            res = resolution_graph.Fit("res_fcn", "RSOEX0", "")
            if res.Get() == None or res.Status() != 0:
                raise Exception('Fit Failed')
            res_pars[id] = [res_fcn.GetParameter(0),res_fcn.GetParameter(1),res_fcn.GetParameter(2),res_fcn.GetParameter(3)]
            xmin, xmax = resolution_graph.GetXaxis().GetXmin(), resolution_graph.GetXaxis().GetXmax()
            vfitter = ROOT.TVirtualFitter.GetFitter()
            res_fcn.SetNpx(1000)
            res_fcn.SetRange(xmin, xmax)
            res_error_graph = get_tgrapherrors(res_fcn, vfitter)

            config['objects'].setdefault('{0}_fit'.format(id_res), {})['obj'] = res_error_graph
        print res_pars
        for k,v in res_pars.iteritems():
            print '\'{0}\' : {1},'.format(k, v)
