import logging
import math

import ROOT

from modules.base_module import BaseModule
from modules.helpers import get_tgrapherrors

log = logging.getLogger(__name__)


class FitObj(BaseModule):
    """ Calls the fit function on an object.

        The function to be fitted is passed via a dict str, e.g.
        --fit-obj id:'{"fcn":"[0] + [1]/x**[2]", "fcn_0":[1.0, 1.0, 1.0]}'
    """

    def __init__(self):
        super(FitObj, self).__init__()
        self.arg_group.add_argument('--fit-obj', nargs='+', default=[], type='str2kvdict', help='')

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
            if 'N' not in options:
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
        self.arg_group.add_argument('--trigger-efficiency-fit', nargs='+', default=[], type='str2kvdict', help='')

    def __call__(self, config):
        for id, settings in config['trigger_efficiency_fit']:
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            eff_fcn = ROOT.TF1("eff_fcn", "(1./2.)*(1 + TMath::Erf((x-[0])/(sqrt(2)*[1])))")

            print 'Fitting id {0}'.format(id)
            eff_fcn.SetParameters(100., 20.0, 1.)
            res = config['objects'][id]['obj'].Fit("eff_fcn", "SEX0", "")

            xmin = eff_fcn.GetX(0.5)
            eff_fcn.SetRange(xmin, 1000)
            res = config['objects'][id]['obj'].Fit("eff_fcn", "SREX0", "")
            xmin = eff_fcn.GetParameter(0)
            xmin = eff_fcn.GetX(0.7)
            eff_fcn.SetRange(xmin, 1000)
            res = config['objects'][id]['obj'].Fit("eff_fcn", "SREX0", "")

            x99 = math.ceil(eff_fcn.GetX(0.99))
            print 'x99 at {0:.2f}'.format(x99)
            # Add label with the efficiency factor
            text = '.99 eff. at {0} GeV'.format(x99)
            config['ax_texts'].append(text + '?_bottomright_')

            print res.Get()
            print res.Status()
            if res.Get() == None or res.Status() != 0:
                raise Exception('Could not fit that function shit.')

            vfitter = ROOT.TVirtualFitter.GetFitter()
            eff_fcn.SetNpx(1000)
            xmin, xmax = config['objects'][id]['obj'].GetXaxis().GetXmin(), config['objects'][id][
                'obj'].GetXaxis().GetXmax()
            eff_fcn.SetRange(xmin, xmax)
            eff_error_graph = get_tgrapherrors(eff_fcn, vfitter)

            id_fit = 'fit_{0}'.format(id.strip('_'))
            config['objects'].setdefault(id_fit, {})['obj'] = eff_error_graph
