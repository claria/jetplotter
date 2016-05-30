
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

        config['ana_modules'] = []

        config['objects']['corr'] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "bwr", 
            "color": "auto", 
            "edgecolor": "auto", 
            "id": "corr", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/corr_h_ptavg".format(rap_bin), 
            "label": "__nolegend__", 
            "linestyle": "", 
            "marker": ".", 
            "step": False, 
            "style": "heatmap", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        }

        config["x_lims"] = ['_{0}_xmin_'.format(rap_bin), '_{0}_xmax_'.format(rap_bin)]
        config["y_lims"] = ['_{0}_xmin_'.format(rap_bin), '_{0}_xmax_'.format(rap_bin)]
        config["z_lims"] = [-1.0, 1.0]
        config['x_log'] = True
        config['y_log'] = True
        config["x_label"] = "_ptavg_"
        config["y_label"] = "_ptavg_"
        config['x_axis_formatter'] = 'scalar2'
        config['y_axis_formatter'] = 'scalar2'
        config["z_label"] = "Correlation coefficient"
        config["legend_loc"] = 'upper right'
        config["ax_texts"] = [
                            "_20fb_",
                            "_{0}_?_upperleft_".format(rap_bin),
                            ] 
        config["output_path"] = 'unf_nlo_corr_{}.png'.format(rap_bin)
        configs.append(config)

    return configs

