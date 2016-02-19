
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['default', 'yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []
    locations = {
                'default' : 'upperright',
                'yb0ys0' : 'upperright',
                'yb0ys1' : 'upperright',
                'yb0ys2' : 'upperright',
                'yb1ys0' : 'upperleft',
                'yb1ys1' : 'upperleft',
                'yb2ys0' : 'upperleft',
            }

    for rap_bin in rap_bins:
        config = get_base_config()
        config['ana_modules'] = []

        config['objects']["data"]= {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "auto", 
            "edgecolor": "auto", 
            "id": "data", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?{0}/h2_y12".format(rap_bin), 
            "label": "__nolegend__", 
            "linestyle": "", 
            "marker": ".", 
            "mask_value": 0.0, 
            "step": False, 
            "style": "heatmap", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        }

        config["y_lims"] = ["-3.0", "3.0"]
        config["x_lims"] = [-3.0, 3.0]
        config["x_label"] = "leading jet rapidity"
        config["y_label"] = "second jet rapidity"
        config["z_label"] = "arb. unit"
        # config["legend_loc"] = legend_locs[rap_bin]
        config["ax_texts"] = [
                            "_20fb_",
                            "_{0}_?_{1}_".format(rap_bin, locations[rap_bin]),
                            ] 
        config["output_path"] = 'jet12_rapidity_{}.png'.format(rap_bin)
        configs.append(config)

    return configs

