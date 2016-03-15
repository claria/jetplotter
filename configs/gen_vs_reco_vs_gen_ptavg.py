
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

        # config['ana_modules'] = ['NormalizeToRow']
        # config['normalize_to_row'] = ['resmatrix']

        config['objects']['genreco'] = {
            "edgecolor": "auto", 
            "style": "heatmap", 
            "rasterized": True, 
            "capsize": 0, 
            "input": "/nfs/dust/cms/user/gsieber/ARTUS/artus_2015-12-16_13-07/QCDMGP6.root?{0}/h2_GenVsRecoPt".format(rap_bin), 
            "x_err": True, 
            "color": "auto", 
            "y_err": True, 
            "label": "__nolegend__", 
            "step": False, 
            "cmap": "viridis", 
            "zorder": 1.0, 
            "obj": "null", 
            "plot_datavals": False, 
            "marker": ".", 
            "alpha": 1.0, 
            "fill": True, 
            "linestyle": "", 
        }

        config["x_lims"] = [0.5, 1.5]
        config["y_lims"] = [50, 4000.]
        config["y_axis_formatter"] = 'scalar2'
        config["z_lims"] = [1E-6, None]
        config['x_log'] = False
        config['y_log'] = True
        config['z_log'] = True
        config["x_label"] = "_ptavgreconu_/_ptavggennu_"
        config["y_label"] = "_ptavggen_"
        config["z_label"] = "arb.unit"
        config["legend_loc"] = 'upper right'
        config["ax_texts"] = [
                            "_8tev_",
                            "_{0}_?_upperleft_".format(rap_bin),
                            ] 
        config["output_path"] = 'gen_vs_reco_vs_gen_ptavg_{}.png'.format(rap_bin)
        configs.append(config)

    return configs

