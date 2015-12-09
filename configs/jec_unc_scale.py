""" Demonstrates the callback mechanism. This function will be called
    after the building of the config.
"""

import util.callbacks as callbacks

@callbacks.register('before_parsing')
def before_parsing(*args, **kwargs):

        # jec_sources  = [
        #                'AbsoluteScale','AbsoluteStat','AbsoluteMPFBias',
        #                'Fragmentation',
        #                'SinglePionECAL',
        #                'SinglePionHCAL',
        #                'FlavorQCD',
        #                'RelativeJEREC1','RelativeJEREC2','RelativeJERHF',
        #                'RelativePtBB','RelativePtEC1','RelativePtEC2','RelativePtHF',
        #                'RelativeFSR',
        #                'RelativeStatEC2', 'RelativeStatHF', 'RelativeStatFSR',
        #                'PileUpDataMC',
        #                'PileUpPtRef',
        #                'PileUpPtBB','PileUpPtEC1','PileUpPtEC2','PileUpPtHF',
        #                ]

    config = kwargs['config']
    inputs = {
        'central' : {
            'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?yb0ys0/h_ptavg'
            },
        'absolutescale_up' : {
            'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?yb0ys0_AbsoluteScale_up/h_ptavg',
            'color' : '_color0_',
            'style' : 'line',
            'step' : 'True',
            'label' : 'AbsoluteScale',
            },
        'absolutescale_dn' : {
            'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?yb0ys0_AbsoluteScale_dn/h_ptavg',
            'color' : '_color0_',
            'style' : 'line',
            'step' : 'True',
            },
        'absolutestat_up' : {
            'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?yb0ys0_AbsoluteStat_up/h_ptavg',
            'color' : '_color1_',
            'style' : 'line',
            'step' : 'True',
            'label' : 'AbsoluteStat',
            },
        'absolutestat_dn' : {
            'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?yb0ys0_AbsoluteStat_dn/h_ptavg',
            'color' : '_color1_',
            'style' : 'line',
            'step' : 'True',
            },
        'absolutempfbias_up' : {
            'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?yb0ys0_AbsoluteMPFBias_up/h_ptavg',
            'color' : '_color2_',
            'style' : 'line',
            'step' : 'True',
            'label' : 'AbsoluteMPFBias',
            },
        'absolutempfbias_dn' : {
            'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?yb0ys0_AbsoluteMPFBias_dn/h_ptavg',
            'color' : '_color2_',
            'style' : 'line',
            'step' : 'True',
            },


    }
    config['objects'].update(inputs)

    config["y_lims"] = ["0.9", "1.1"]
    config["x_lims"] = ["133.", "2000."]
    config["x_log"] =  True
    config["x_label"] = "_ptavg_"
    config["y_label"] = "Uncertainty?_center_"
    config["ax_hlines"] = [
                            {'y' : 1.0, 'color' : 'black'}
                            ]
    config["ax_texts"] = ["_cmsp_", "_yb0ys0_?_upperleft_", '_20fb_'] 


@callbacks.register('after_input_modules')
def after_input_modules(*args, **kwargs):
    from modules.normalization import calc_ratio
    from modules.rebinning import rebin_histo
    config = kwargs['config']
    config['objects']['absolutescale_up']['obj'] = calc_ratio(config['objects']['absolutescale_up']['obj'], config['objects']['central']['obj'])
    config['objects']['absolutescale_up']['obj'] = rebin_histo(config['objects']['absolutescale_up']['obj'], 133., 1784.)
    config['objects']['absolutescale_dn']['obj'] = calc_ratio(config['objects']['absolutescale_dn']['obj'], config['objects']['central']['obj'])
    config['objects']['absolutescale_dn']['obj'] = rebin_histo(config['objects']['absolutescale_dn']['obj'], 133., 1784.)

    config['objects']['absolutestat_up']['obj'] = calc_ratio(config['objects']['absolutestat_up']['obj'], config['objects']['central']['obj'])
    config['objects']['absolutestat_up']['obj'] = rebin_histo(config['objects']['absolutestat_up']['obj'], 133., 1784.)
    config['objects']['absolutestat_dn']['obj'] = calc_ratio(config['objects']['absolutestat_dn']['obj'], config['objects']['central']['obj'])
    config['objects']['absolutestat_dn']['obj'] = rebin_histo(config['objects']['absolutestat_dn']['obj'], 133., 1784.)

    config['objects']['absolutempfbias_up']['obj'] = calc_ratio(config['objects']['absolutempfbias_up']['obj'], config['objects']['central']['obj'])
    config['objects']['absolutempfbias_up']['obj'] = rebin_histo(config['objects']['absolutempfbias_up']['obj'], 133., 1784.)
    config['objects']['absolutempfbias_dn']['obj'] = calc_ratio(config['objects']['absolutempfbias_dn']['obj'], config['objects']['central']['obj'])
    config['objects']['absolutempfbias_dn']['obj'] = rebin_histo(config['objects']['absolutempfbias_dn']['obj'], 133., 1784.)


    del config['objects']['central']

