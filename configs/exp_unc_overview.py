
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
        config['ana_modules'] = ["Ratio"]
        config["ratio"] = [
                           ["dataunf_lumi", "dataunf_stat"], 
                           ["dataunf_total", "dataunf_total"], 
                           ["dataunf_uncor", "dataunf_stat"], 
                           ["dataunf_jec", "dataunf_stat"], 
                           ["dataunf_stat", "dataunf_stat"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]

        config['plot_order'] = ['dataunf_stat']

        config['objects']["dataunf_stat"] = {
            "color": "black", 
            "edgecolor": "black", 
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_stat".format(rap_bin), 
            "label": "Stat. uncertainty", 
            "marker": ".", 
            "step": False, 
            "zorder": 2.0,
        }
        config['objects']["dataunf_lumi"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_lumi".format(rap_bin), 
            "label": "Lumi. uncertainty", 
            "style": "errorlines",
            "step": True,
        }
        config['objects']["dataunf_jec"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_jec".format(rap_bin), 
            "label": "JEC uncertainty", 
            "style": "errorlines",
            "step": True,
        }
        config['objects']["dataunf_uncor"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_unc".format(rap_bin), 
            "label": "Syst. unc. uncertainty", 
            "style": "errorlines",
            "step": True,
        }
        config['objects']["dataunf_total"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_tot".format(rap_bin), 
            "label": "Total uncertainty", 
            "style": "errorlines",
            "color": "black",
            "linestyle": "--",
            "step": True,
        }

        config["y_lims"] = ["0.7", "1.3"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Fractional Uncertainty?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'exp_unc_overview_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

