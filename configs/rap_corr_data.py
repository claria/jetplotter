
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
        config['ana_modules'] = ['Ratio']
        config['ratio'] = [('corr', 'nocorr'), ('nocorr', 'nocorr')]
        config['plot_id'] = '^corr$'

        config['objects']["nocorr"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/rapidityNOCORR_DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "nocorr"
        } 
        config['objects']["corr"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/rapidityCORR_DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Ratio with/without correction"
        }

        config["y_lims"] = [0.0, 2.0]
        config["x_lims"] = ['_{0}_xmin_'.format(rap_bin),'_{0}_xmax_'.format(rap_bin)]
        config['x_log'] = True
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Ratio to Data (No rap. correction)?_center_"
        config["z_label"] = "arb. unit"
        config["legend_loc"] = 'upper right'
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                            "_20fb_",
                            "_{0}_?_upperleft_".format(rap_bin),
                            ] 
        config["output_path"] = 'rap_corr_data_{}.png'.format(rap_bin)
        configs.append(config)

    return configs

