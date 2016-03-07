
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
        config['ana_modules'] = ["Ratio", "FitObj", "BuildTGraph", "RootOutputModule"]

        config["build_tgraph"] = []
        config["fit_obj"] = [
                        ("hw7_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ),
                        ("pwgp8_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ) 

                    ]

        config["ratio"] = [
                           ["hw7_mpihad", "hw7_nompinohad"], 
                           ["pwgp8_mpihad", "pwgp8_nompinohad"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config['plot_order'] = []
        config['plot_id'] = ['fit_hw7_mpihad', 'hw7_mpihad','fit_pwgp8_mpihad', 'pwgp8_mpihad']

        config['objects']["hw7_mpihad"] = {
            "input": "~/dust/HW7/HW7_NLO+PS_2.root?{0}_xs".format(rap_bin), 
            "label": "Herwig 7",
            "color": "_color0_"
        } 
        config['objects']["hw7_nompinohad"] = {
            "input": "~/dust/HW7/HW7_NLO+PS_NOMPINOHAD_2.root?{0}_xs".format(rap_bin)
        }
        config['objects']["pwgp8_mpihad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET3/POWHEG_MPIHAD.root?{0}_xs".format(rap_bin), 
            "label": "Powheg+P8",
            "color": "_color2_"
        } 
        config['objects']["pwgp8_nompinohad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET3/POWHEG_NOMPINOHAD.root?{0}_xs".format(rap_bin)
        }

        config['objects']["fit_hw7_mpihad"] = {
            "label": "Herwig 7",
            "style": "line",
            "color": "_color0_"
        } 
        config['objects']["fit_pwgp8_mpihad"] = {
            "label": "Herwig 7",
            "style": "line",
            "color": "_color2_"
        } 

        config["y_lims"] = ["0.88", "1.4"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "NP Correction"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin),
                             ] 

        config["output_path"] = 'np_factors_nlo_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

