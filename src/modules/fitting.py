import numpy as np
import ROOT

from src.modules.base_module import BaseModule
from src.modules.helpers import get_tgrapherrors

import logging
log = logging.getLogger(__name__)


class FitObj(BaseModule):
    """ Calls the fit function on an object.

        The function to be fitted is passed via a dict str, e.g.
        --fit-obj id:'{"fcn":"[0] + [1]/x**[2]", "fcn_0":[1.0, 1.0, 1.0]}'
    """

    def __init__(self):
        super(FitObj, self).__init__()
        self.parser.add_argument('--fit-obj', nargs='+', default=[], type='str2kvdict', help='')

    def __call__(self, config):
        for id, settings in config['fit_obj']:
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            fcn_name = 'fit_{0}'.format(id)
            fcn = ROOT.TF1(fcn_name, settings['fcn'])

            if 'fcn_0' in settings:
                fcn.SetParameters(*settings['fcn_0'])
            options = settings.get('options', '')

            xmin, xmax = config['objects'][id]['obj'].GetXaxis().GetXmin(), config['objects'][id][
                'obj'].GetXaxis().GetXmax()
            # Do the fit
            if not 'N' in options:
                options += 'N'
            print options
            config['objects'][id]['obj'].Fit(fcn_name, options)
            vfitter = ROOT.TVirtualFitter.GetFitter()
            fcn.SetNpx(1000)
            fcn.SetRange(xmin, xmax)
            errorgraph = get_tgrapherrors(fcn, vfitter)
            # TODO fix this shit
            # config['objects']['fit_{0}'.format(id)] = copy.deepcopy(config['objects'][id])
            new_obj_name = 'fit_{0}'.format(id)
            config['objects'].setdefault(new_obj_name, {})['obj'] = errorgraph



class TriggerEfficiencyFit(BaseModule):
    """ Calls the fit function on an object.

        The function to be fitted is passed via a dict str, e.g.
        --fit-obj id:'{"fcn":"[0] + [1]/x**[2]", "fcn_0":[1.0, 1.0, 1.0]}'
    """

    def __init__(self):
        super(TriggerEfficiencyFit, self).__init__()
        self.parser.add_argument('--trigger-efficiency-fit', nargs='+', default=[], type='str2kvdict', help='')

    def __call__(self, config):
        for id, settings in config['trigger_efficiency_fit']:
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            eff_fcn = ROOT.TF1("eff_fcn", "(1./2.)*(1 + TMath::Erf((x-[0])/(sqrt(2)*[1])))")
            # res_fcn = ROOT.TF1("res_fcn", "sqrt(TMath::Sign(1.,[0])*(([0]/x)**2) + (([1]**2)/x)*(x**[2]) + [3]**2)")


            # threshold = float(eff.GetName().split('_')[1].replace('PFJET',''))
            print 'Fitting id {0}'.format(id_res)
            res_fcn.SetParameters(100., 20.0, 1.)
            res = eff.Fit("eff_fcn", "EX0", "")

            xmin = res_fcn.GetX(0.5)
            res_fcn.SetRange(xmin, 1000)
            res = eff.Fit("eff_fcn", "rEX0", "")
            xmin = res_fcn.GetParameter(0)
            xmin = res_fcn.GetX(0.7)
            res_fcn.SetRange(xmin, 1000)
            res = eff.Fit("eff_fcn", "rEX0", "")

            x99 = res_fcn.GetX(0.99)

            if res.Get() == None or res.Status() != 0:
                raise Exception('Could not fit that function shit.')

            vfitter = ROOT.TVirtualFitter.GetFitter()
            eff_fcn.SetNpx(1000)
            eff_fcn.SetRange(xmin, xmax)
            eff_error_graph = get_tgrapherrors(eff_fcn, vfitter)

            id_fit = 'fit_{0}'.format(id.strip('_'))
            config['objects'].setdefault(id_fit, {})['obj'] = eff_error_graph




