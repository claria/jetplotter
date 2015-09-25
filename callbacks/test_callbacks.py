""" Demonstrates the callback mechanism. This function will be called
    after the building of the config.
"""

import util.callbacks as callbacks

@callbacks.register('before_parsing')
def before_parsing(*args, **kwargs):

    config['objects']['hwppnompinohad']['input'] = "~/dust/dijetana/ana/CMSSW_7_2_3/HWPP_EE3C_FLAT_NOMPINOHAD.root?gen_yb0ys0/h_genptavg"
    config['objects']['hwppmpihad']['input'] =  "~/dust/dijetana/ana/CMSSW_7_2_3/HWPP_EE3C_FLAT_MPIHAD.root?gen_yb0ys0/h_genptavg"
    config['objects']['qcdp8nompinohad']['input'] = "~/dust/dijetana/ana/CMSSW_7_2_3/P8CUETP8_4C_FLAT_NOMPINOHAD2.root?gen_yb0ys0/h_genptavg"
    config['objects']['qcdp8mpihad']['input'] = "~/dust/dijetana/ana/CMSSW_7_2_3/P8CUETP8_4C_FLAT_MPIHAD.root?gen_yb0ys0/h_genptavg"

    config["y_lims"] = ["0.8", "1.4"]
    config["x_lims"] = ["50.", "3000."]
    config["x_log"] =  True
    config["x_label"] = "_ptavg_"
    config["y_label"] = "NP Correction"
    config["ax_texts"] = ["_cmsp_", "_yb0ys0_?_upperleft_"] 


@callbacks.register('after_ana_modules')
def after_modules(*args, **kwargs):
    
    config['objects']['qcdp8mpihad']['obj'] = config['objects']['qcdp8mpihad']['obj'].Divide(config['objects']['qcdp8nompinohad']['obj'])
    del config['objects']['qcdp8nompinohad']
    config['objects']['hwppmpihad']['obj'] = config['objects']['hwppmpihad']['obj'].Divide(config['objects']['hwppnompinohad']['obj'])
    del config['objects']['hwppnompinohad']

    config['objects']['fit_hwppmpihad'] = fit_obj
    config['objects']['fit_qcdp8mpihad']


