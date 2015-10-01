""" Demonstrates the callback mechanism. This function will be called
    after the building of the config.
"""

import util.callbacks as callbacks

@callbacks.register('before_parsing')
def before_parsing(*args, **kwargs):

    config = kwargs['config']
    config['objects'].setdefault('hwppnompinohad', {})['input'] = "~/dust/dijetana/ana/CMSSW_7_2_3/HWPP_EE5C_FLAT_NOMPINOHAD.root?gen_yb0ys0/h_genptavg"
    config['objects'].setdefault('hwppmpihad', {})['input'] =  "~/dust/dijetana/ana/CMSSW_7_2_3/HWPP_EE5C_FLAT_MPIHAD.root?gen_yb0ys0/h_genptavg"
    config['objects'].setdefault('qcdp8nompinohad', {})['input'] = "~/dust/dijetana/ana/CMSSW_7_2_3/P8_CUETP8S1_FLAT_NOMPINOHAD.root?gen_yb0ys0/h_genptavg"
    config['objects'].setdefault('qcdp8mpihad', {})['input'] = "~/dust/dijetana/ana/CMSSW_7_2_3/P8_CUETP8S1_FLAT_MPIHAD.root?gen_yb0ys0/h_genptavg"

    config["y_lims"] = ["0.8", "1.4"]
    config["x_lims"] = ["50.", "3000."]
    config["x_log"] =  True
    config["x_label"] = "_ptavg_"
    config["y_label"] = "NP Correction"
    config["ax_texts"] = ["_cmsp_", "_yb0ys0_?_upperleft_"] 


@callbacks.register('after_input_modules')
def after_input_modules(*args, **kwargs):

    config = kwargs['config']
    config['objects']['qcdp8mpihad']['obj'].Divide(config['objects']['qcdp8nompinohad']['obj'])
    del config['objects']['qcdp8nompinohad']
    config['objects']['hwppmpihad']['obj'].Divide(config['objects']['hwppnompinohad']['obj'])
    del config['objects']['hwppnompinohad']

    config['ana_modules'] += ['FitObj']
    config['fit_obj'] = [('qcdp8mpihad', {
                                            "fcn": "[0] + [1]/x**[2]", 
                                            "fcn_0": [1.0, 1.0, 1.0], 
                                            "options": "I"
                                            }),
                         ('hwppmpihad', {
                                            "fcn": "[0] + [1]/x**[2]", 
                                            "fcn_0": [1.0, 1.0, 1.0], 
                                            "options": "I"
                                            }),
        ]

