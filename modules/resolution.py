import logging

import ROOT

from modules.base_module import BaseModule
from modules.helpers import get_tgrapherrors
from math import exp

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
                print 'ptbin', i, config['objects'][id]['obj'].GetYaxis().GetBinLowEdge(i), config['objects'][id]['obj'].GetYaxis().GetBinLowEdge(i+1)
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
            # if res.Get() == None or res.Status() != 0:
                # raise Exception('Fit Failed')
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


def fnc_dscb(x_pars, par):
    """ double sided crystalball function."""
    x = x_pars[0]
    (N, mu, sig, a1, p1, a2, p2) = par
    # print 'N, mu, sig, a1, p1, a2, p2'
    # print N, mu, sig, a1, p1, a2, p2
    try:
        u = (x-mu)/sig
        A1 = (p1/abs(a1))**p1 * exp(-a1 *a1/2.)
        B1 = p1/abs(a1) - abs(a1)
        A2 = (p2/abs(a2))**p2 * exp(-a2 *a2/2.)
        B2 = p2/abs(a2) - abs(a2)
    except ValueError as e:
        print e
        print 'N, mu, sig, a1, p1, a2, p2'
        print N, mu, sig, a1, p1, a2, p2
        raise


    if (u < -a1):
        return N*A1*(B1-u)**(-p1)
    elif (u < a2):
        return N*exp(-u*u/2.)
    else:
        return N*A2*(B2+u)**(-p2)

# double fnc_dscb(double*xx,double*pp)
# {
#   double x   = xx[0];
#   // gaussian core
#   double N   = pp[0];//norm
#   double mu  = pp[1];//mean
#   double sig = pp[2];//variance
#   // transition parameters
#   double a1  = pp[3];
#   double p1  = pp[4];
#   double a2  = pp[5];
#   double p2  = pp[6];
#   
#   double u   = (x-mu)/sig;
#   double A1  = TMath::Power(p1/TMath::Abs(a1),p1)*TMath::Exp(-a1*a1/2);
#   double A2  = TMath::Power(p2/TMath::Abs(a2),p2)*TMath::Exp(-a2*a2/2);
#   double B1  = p1/TMath::Abs(a1) - TMath::Abs(a1);
#   double B2  = p2/TMath::Abs(a2) - TMath::Abs(a2);
#
#   double result(N);
#   if      (u<-a1) result *= A1*TMath::Power(B1-u,-p1);
#   else if (u<a2)  result *= TMath::Exp(-u*u/2);
#   else            result *= A2*TMath::Power(B2+u,-p2);
#   return result;
# }


class CrystalBallResolutionAna(BaseModule):
    """ Fits the resolution from a TH2D assuming gaussian errors. """

    def __init__(self):
        super(CrystalBallResolutionAna, self).__init__()
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
                print 'ptbin', i, config['objects'][id]['obj'].GetYaxis().GetBinLowEdge(i), config['objects'][id]['obj'].GetYaxis().GetBinLowEdge(i+1)
                pt_bin_obj = config['objects'][id]['obj'].ProjectionX("{0}_slice_{1}".format(id, i), i, i)
                # Continue if histogram if empty
                if pt_bin_obj.GetEntries() < 1:
                    continue
                # If fit fails continue instead of failing
                id_slice = '_{0}_slice_{1}'.format(id.strip('_'), i)

                # Start with gaussian fit
                res = pt_bin_obj.Fit("gaus", "SQO")
                if res.Get() == None or res.Status() != 0:
                    continue
                gauss_fcn = pt_bin_obj.GetFunction("gaus")
                p_norm = gauss_fcn.GetParameter(0)
                p_mean = gauss_fcn.GetParameter(1)
                p_sigma = gauss_fcn.GetParameter(2)

                cb_fcn = ROOT.TF1('crystalball', fnc_dscb, 0.5, 1.5, 7)

                cb_fcn.SetParameter(0, p_norm)
                cb_fcn.SetParameter(1, p_mean)
                cb_fcn.SetParameter(2, p_sigma)
                cb_fcn.SetParameter(3, 2.0)
                cb_fcn.SetParameter(4, 5.0)
                cb_fcn.SetParameter(5, 2.5)
                cb_fcn.SetParameter(6, 5.0)

                cb_fcn.SetParLimits(3, 1., 5.)
                cb_fcn.SetParLimits(5, 1., 5.)

                cb_fcn.SetParLimits(4, 0.01, 25.)
                cb_fcn.SetParLimits(6, 0.01, 25.)

                res = pt_bin_obj.Fit("crystalball", "SO")
                if res.Get() == None or res.Status() != 0:
                    continue

                xmin, xmax = pt_bin_obj.GetXaxis().GetXmin(), pt_bin_obj.GetXaxis().GetXmax()
                vfitter = ROOT.TVirtualFitter.GetFitter()
                cb_fcn.SetNpx(1000)
                cb_fcn.SetRange(xmin, xmax)
                error_graph = get_tgrapherrors(cb_fcn, vfitter)

                # Omit bin with too large errors > 5%
                if (cb_fcn.GetParError(2) / cb_fcn.GetParameter(2)) > 0.05 or cb_fcn.GetParameter(2)> 0.20:
                    print 'stat. error too large. Omit bin.'
                    continue

                # Uncomment to save also individual gauss fits to dict
                config['objects'].setdefault(id_slice, {})
                config['objects'][id_slice]['obj'] = pt_bin_obj
                config['objects'].setdefault('{0}_fit'.format(id_slice), {})
                config['objects']['{0}_fit'.format(id_slice)]['obj'] = error_graph
                resolution_graph.SetPoint(i, config['objects'][id]['obj'].GetYaxis().GetBinCenter(i),
                                          cb_fcn.GetParameter(2))
                resolution_graph.SetPointError(i, config['objects'][id]['obj'].GetYaxis().GetBinWidth(i) / 2.,
                                               cb_fcn.GetParError(2))
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
            # if res.Get() == None or res.Status() != 0:
                # raise Exception('Fit Failed')
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
