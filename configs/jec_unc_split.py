def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config


def get_config():
    configs = []

    all_sources = [
         ['AbsoluteScale','AbsoluteStat','AbsoluteMPFBias', 'Fragmentation'],
         ['SinglePionECAL','SinglePionHCAL','FlavorQCD'],
         ['RelativeJEREC1','RelativeJEREC2','RelativeJERHF', 'RelativePtBB'],
         ['RelativePtEC1','RelativePtEC2','RelativePtHF', 'RelativeFSR'],
         ['RelativeStatEC2', 'RelativeStatHF', 'RelativeStatFSR'],
         ['PileUpDataMC', 'PileUpPtRef','PileUpPtBB','PileUpPtEC1','PileUpPtEC2','PileUpPtHF'],
         ]
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']

    
    for k, sources in enumerate(all_sources):
        for rap_bin in rap_bins:
            config = get_base_config()
            config['objects']['central'] = { 
                    'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}/h_genptavg'.format(rap_bin)
                                }


            for i, source in enumerate(sources):

                for var in ['up','dn']:
                    config['objects']['{0}_{1}'.format(source, var)] = {
                        'input' : '~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_{1}_{2}/h_genptavg'.format(rap_bin, source, var),
                        'color' : '_color{0}_'.format(i),
                        'style' : 'line',
                        'step' : 'True',
                        'label' : '{0}'.format(source),
                        }
            config['ana_modules'] = [
                                     'DataLims', 
                                     'Ratio'
                                     ]
            for source in sources:
                for var in ['up','dn']:
                    config.setdefault('ratio', []).append(('{0}_{1}'.format(source, var),'central'))


            config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)})]
            print config['data_lims']
            config['plot_id'] = ['{0}_{1}'.format(source, var) for source in sources for var in ['up', 'dn']]
            config["y_lims"] = ["0.9", "1.1"]
            config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
            config["x_log"] =  True
            config["x_label"] = "_ptavg_"
            config["legend_loc"] = "upper right"
            config["y_label"] = "Uncertainty?_center_"
            config["ax_hlines"] = [
                                    {'y' : 1.0, 'color' : 'black'}
                                    ]
            config["ax_texts"] = ["_cmsp_", "_{0}_?_upperleft_".format(rap_bin), '_20fb_'] 
            config["output_path"] = 'jec_relunc_{0}_{1}.png'.format(k, rap_bin)

            configs.append(config)
    return configs
