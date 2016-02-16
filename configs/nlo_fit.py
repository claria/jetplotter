
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []

    fit_start_params = {
            'yb0ys0' : [1.56951e-04, 4.72895e+00, 1.25370e+01, 4.41885e+03],
            'yb0ys1' : [1.25998e-02, 4.86297e+00, 7.80386e+00, 1.58397e+03],
            'yb0ys2' : [2.71653e+00, 4.28902e+00, 7.67473e+00, 5.83335e+02],
            'yb1ys0' : [4.56147e-04, 4.88011e+00, 1.26727e+01, 2.80141e+03],
            'yb1ys1' : [1.62403e-01, 3.89047e+00, 1.73026e+01, 1.40653e+03],
            'yb2ys0' : [2.39237e-02, 4.39508e+00, 1.41838e+01, 1.16487e+03],
            }
    for rap_bin in rap_bins:
        config = get_base_config()
        config['ana_modules'] = ["Multiply", "FitObj"]
        config["multiply"] = [
                              ("ct14nlo", "_np")]
        config["fit_obj"] = [
                        ("ct14nlo", {
                                "fcn": "[0]*(x/[3])**(-1*[1])*(1-(x/[3]))**[2]", 
                                "fcn_0": fit_start_params[rap_bin],
                                "options": "IS"
                            }
                        ),
                        ]
        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        # config['plot_order'] = []
        # config['plot_id'] = []

        config['objects']["_np"] = {
            "input": "~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor".format(rap_bin)
        } 
        config['objects']["ct14nlo"] = {
            "color": "black", 
            "edgecolor": "black", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/CT14nlo_xs".format(rap_bin), 
            "label": "CT14 - NLO", 
        } 
        config['objects']["fit_ct14nlo"] = {
            "label": "Fit",
            "style": "line",
            "color": "_color0_"
        } 

        config["y_lims"] = [1E-5, 1E5]
        config["y_log"] = True
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "$\sigma$"
        config["ax_hlines"] = [
                # {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin),
                              '_8tev_'
                             ] 

        config["output_path"] = 'theory_fit_ct14nlo_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

