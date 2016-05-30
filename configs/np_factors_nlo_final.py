
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
        config['ana_modules'] = ["Divide", "FitObj", "DataLims", "Envelope", "RootOutputModule"]


        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),]
        config["envelope"] = [
                            ("res_np_factor", ("_fit_graph_origbin_hwpp_mpihad", "_fit_graph_origbin_p8_mpihad", '_fit_graph_origbin_pwgp8_m1_mpihad', '_fit_graph_origbin_pwgp8_s1_mpihad'))
                                ]

        config['root_output_filename'] = 'np_factors.root'
        config['root_output_folder'] = rap_bin

        config["fit_obj"] = [
                        ("pwgp8_s1_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ),
                        ("pwgp8_m1_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ),
                        ("p8_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ),
                        ("hwpp_mpihad", {
                                "fcn": "[0]/x**[1] + [2]", 
                                "fcn_0": [1.0, 1.0, 1.0], 
                                "options": "I"
                            }
                        ),
                    ]

        config["divide"] = [
                           ["p8_mpihad", "p8_nompinohad"], 
                           ["hwpp_mpihad", "hwpp_nompinohad"], 
                           ["pwgp8_s1_mpihad", "pwgp8_nompinohad"], 
                           ["pwgp8_m1_mpihad", "pwgp8_nompinohad"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config['plot_order'] = ['res_np_factor']
        config['plot_id'] = ['fit_pwgp8_s1_mpihad',# 'pwgp8_s1_mpihad',
                             'fit_pwgp8_m1_mpihad',# 'pwgp8_m1_mpihad', 
                             'fit_p8_mpihad',# 'p8_mpihad', 
                             'fit_hwpp_mpihad',# 'hwpp_mpihad', 
                             'res_np_factor'
                             ]

        config['objects']["res_np_factor"] = {
            "label": "Final Correction",
            "color": "black",
            'alpha': 1.0,
            "zorder": 2.5,
            # "style": 'band'
        } 
        config['objects']["pwgp8_s1_mpihad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET3/POWHEG_MPIHAD.root?{0}_xs".format(rap_bin), 
            "color": "_color2_"
        } 
        config['objects']["pwgp8_m1_mpihad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET_8CUEP8M1/POWHEG_MPIHAD_8CUEP8M1.root?{0}_xs".format(rap_bin), 
            "color": "_color3_"
        } 
        config['objects']["pwgp8_nompinohad"] = {
            "input": "/nfs/dust/cms/user/gsieber/POWHEG/RIVET3/POWHEG_NOMPINOHAD.root?{0}_xs".format(rap_bin)
        }

        config['objects']["p8_mpihad"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/P8_CUETP8S1_FLAT_MPIHAD.root?gen_{0}/h_genptavg".format(rap_bin), 
            "color": "_color4_"
        } 
        config['objects']["p8_nompinohad"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/P8_CUETP8S1_FLAT_NOMPINOHAD.root?gen_{0}/h_genptavg".format(rap_bin), 
        }
        config['objects']["hwpp_mpihad"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/HWPP_EE5C_FLAT_MPIHAD.root?gen_{0}/h_genptavg".format(rap_bin), 
            "color": "_color5_"
        } 
        config['objects']["hwpp_nompinohad"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/HWPP_EE5C_FLAT_NOMPINOHAD.root?gen_{0}/h_genptavg".format(rap_bin), 
        }

        config['objects']["fit_pwgp8_s1_mpihad"] = {
            "label": "Powheg+P8 8CUEP8S1",
            "style": "line",
            "color": "_color2_"
        } 
        config['objects']["fit_pwgp8_m1_mpihad"] = {
            "label": "Powheg+P8 8CUEP8M1",
            "style": "line",
            "color": "_color3_"
        } 
        config['objects']["fit_p8_mpihad"] = {
            "label": "P8",
            "style": "line",
            "color": "_color4_"
        } 
        config['objects']["fit_hwpp_mpihad"] = {
            "label": "Herwig++",
            "style": "line",
            "color": "_color5_"
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

        config["output_path"] = 'np_factors_nlo_final_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

