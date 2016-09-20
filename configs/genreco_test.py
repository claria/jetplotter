
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []
    for rap_bin in rap_bins:
        config = get_base_config()

        config['ana_modules'] = ['Ratio', 'BuildTGraph','DataLims']
        config['ratio'] = [
                    # ('central_reco', 'central_gen')
                ]

        config['build_tgraph'] = [
                                 ('total', ('central_reco', 'total_dn', 'total_up')),
                                 ('flavorqcd', ('central_reco', 'flavor_dn', 'flavor_up')),
                                 ]

        config["plot_id"] = ['central_reco', 'gen_reco', 
                             '^total$', 'flavorqcd',
                              ]

        config['objects']["central_reco"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TEST_MIKKO_QCDMGP6.root?{0}/tp_RecoPtAvg".format(rap_bin), 
            "label": "Central reco", 
            "step": True, 
            "zorder": 1.0,
        }
        config['objects']["central_gen"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TEST_MIKKO_QCDMGP6.root?{0}/tp_GenPtAvg".format(rap_bin), 
            "label": "Central gen", 
            "step": True, 
            "zorder": 1.0,
        }
        config['objects']["total_up"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TEST_MIKKO_QCDMGP6.root?{0}_Total_up/tp_GenVsRecoPtAvg".format(rap_bin), 
        }
        config['objects']["total_dn"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TEST_MIKKO_QCDMGP6.root?{0}_Total_dn/tp_GenVsRecoPtAvg".format(rap_bin), 
        }
        config['objects']["flavor_up"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TEST_MIKKO_QCDMGP6.root?{0}_FlavorQCD_up/tp_GenVsRecoPtAvg".format(rap_bin), 
        }
        config['objects']["flavor_dn"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TEST_MIKKO_QCDMGP6.root?{0}_FlavorQCD_dn/tp_GenVsRecoPtAvg".format(rap_bin), 
        }

        config['objects']["total"] = {
            "label": "Total", 
            "step": True, 
            "style": "errorlines", 
            "dashes": [20,4],
            "zorder": 1.0
        } 
        config['objects']["flavorqcd"] = {
            "label": "FlavorQCD", 
            "step": True, 
            "dashes": [4,4,10,4],
            "style": "errorlines", 
            "zorder": 1.0
        } 


        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]

        config["y_lims"] = ["0.0", "2"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'lower left'
        config["x_label"] = "_ptavggen_"
        config["y_label"] = "<_ptavgreconu_/_ptavggennu_>?_center_"
        config["ax_hlines"] = [
                {'y' : 0.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              "s=NNPDF 3.0-NLO?_upperleft2_",
                              '_8tev_'] 

        config["output_path"] = 'genreco_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

