import util.callbacks as callbacks

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
        config['ana_modules'] = ["Ratio", "MinusOne"]
        config["ratio"] = [
                           ["dataunf_lumi", "dataunf_stat"], 
                           ["dataunf_total", "dataunf_total"], 
                           ["dataunf_uncor", "dataunf_stat"], 
                           ["dataunf_jec", "dataunf_stat"], 
                           ["dataunf_jer", "dataunf_stat"], 
                           ["dataunf_stat", "dataunf_stat"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]

        config['plot_order'] = ['dataunf_stat', 'dataunf_jec', 'dataunf_uncor', 'dataunf_jer', 'dataunf_lumi']
        config['minusone'] = ['dataunf_stat', 'dataunf_jec', 'dataunf_uncor', 'dataunf_jer', 'dataunf_lumi', 'dataunf_total']

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
            "color": "_color2_",
            "dashes": [4,4,10,4],
            "step": True,
        }
        config['objects']["dataunf_jec"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_jec".format(rap_bin), 
            "label": "JEC uncertainty", 
            "style": "errorlines",
            "color": "_color0_",
            "dashes": [20,4],
            "step": True,
        }
        config['objects']["dataunf_jer"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_jer".format(rap_bin), 
            "label": "JER uncertainty", 
            "style": "errorlines",
            "color": "_color1_",
            "step": True,
        }

        config['objects']["dataunf_uncor"] = {
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_unc".format(rap_bin), 
            "label": "Uncor. uncertainty", 
            "style": "errorlines",
            "color": "_color3_",
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

        config["y_lims"] = ["-0.25", "0.25"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'lower left'
        config["legend_ncol"] = 2
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Relative Uncertainty?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'exp_unc_overview_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 22
    kwargs['mpl'].rcParams['lines.linewidth'] = 4
