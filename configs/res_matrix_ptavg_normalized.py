
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    configs = []
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']

    for rap_bin in rap_bins:
        config = get_base_config()

        config['ana_modules'] = ['NormalizeToRow']
        config['normalize_to_row'] = ['resmatrix']

        config['objects']['resmatrix'] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "auto", 
            "edgecolor": "auto", 
            "id": "resmatrix", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_fastNLO.root?{0}/h2_res_matrix_ptavg".format(rap_bin), 
            "label": "__nolegend__", 
            "linestyle": "", 
            "marker": ".", 
            "step": False, 
            "style": "heatmap", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0, 
            "mask_value": 0.0
        }

        config["x_lims"] = ['_{0}_xmin_'.format(rap_bin), '_yb0ys0_xmax_'.format(rap_bin)]
        config["y_lims"] = ['100.', '_yb0ys0_xmax_'.format(rap_bin)]
        config["z_lims"] = [0.0, 1.0]
        config['x_log'] = True
        config['y_log'] = True
        config["x_label"] = "Reco _ptavg_"
        config["y_label"] = "Gen _ptavg_"
        config["z_label"] = ""
        config["legend_loc"] = 'upper right'
        config["ax_texts"] = [
                            "_8tev_",
                            "_{0}_?_upperleft_".format(rap_bin),
                            ] 
        config["output_path"] = 'res_matrix_ptavg_normalized_{}.png'.format(rap_bin)
        configs.append(config)

    return configs

