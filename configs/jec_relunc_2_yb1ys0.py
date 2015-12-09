""" Demonstrates the callback mechanism. This function will be called
    after the building of the config.
"""

import util.callbacks as callbacks




@callbacks.register('before_parsing')
def before_parsing(*args, **kwargs):
        #                'AbsoluteScale','AbsoluteStat','AbsoluteMPFBias', 'Fragmentation',
        #                'SinglePionECAL','SinglePionHCAL','FlavorQCD',
        #                'RelativeJEREC1','RelativeJEREC2','RelativeJERHF', 'RelativePtBB','
        #                 RelativePtEC1','RelativePtEC2','RelativePtHF', 'RelativeFSR',
        #                'RelativeStatEC2', 'RelativeStatHF', 'RelativeStatFSR',
        #                'PileUpDataMC', 'PileUpPtRef','PileUpPtBB','PileUpPtEC1','PileUpPtEC2','PileUpPtHF',

    config = kwargs['config']

    sources = ['RelativeJEREC1','RelativeJEREC2','RelativeJERHF', 'RelativePtBB']

    config['objects']['central'] = { 
                                'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?yb1ys0/h_genptavg'
                                }

    for i, source in enumerate(sources):
        for var in ['up','dn']:
            config['objects']['{0}_{1}'.format(source, var)] = {
                'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?yb1ys0_{0}_{1}/h_genptavg'.format(source, var),
                'color' : '_color{0}_'.format(i),
                'style' : 'line',
                'step' : 'True',
                'label' : '{0}'.format(source),
                }


    config["y_lims"] = ["0.9", "1.1"]
    config["x_lims"] = ["133.", "2000."]
    config["data_lims"] = ["_yb1ys0_xmin_", "_yb1ys0_xmax_"]
    config["x_log"] =  True
    config["x_label"] = "_ptavg_"
    config["y_label"] = "Uncertainty?_center_"
    config["ax_hlines"] = [
                            {'y' : 1.0, 'color' : 'black'}
                            ]
    config["ax_texts"] = ["_cmsp_", "_yb1ys0_?_upperleft_", '_20fb_'] 

    config["output_path"] = 'jec_relunc_2_yb1ys0.png'


@callbacks.register('after_input_modules')
def after_input_modules(*args, **kwargs):
    from modules.normalization import calc_ratio
    from modules.rebinning import rebin_histo
    config = kwargs['config']

    sources = ['RelativeJEREC1','RelativeJEREC2','RelativeJERHF', 'RelativePtBB']
    for source in sources:
        for var in ['up','dn']:
            config['objects']['{0}_{1}'.format(source, var)]['obj'] = calc_ratio(config['objects']['{0}_{1}'.format(source, var)]['obj'], 
                                                                                 config['objects']['central']['obj'])
            config['objects']['{0}_{1}'.format(source, var)]['obj'] = rebin_histo(config['objects']['{0}_{1}'.format(source, var)]['obj'], float(config['data_lims'][0]), float(config['data_lims'][1]))

    del config['objects']['central']

