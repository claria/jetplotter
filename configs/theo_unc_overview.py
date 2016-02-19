
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
        config['ana_modules'] = ["Ratio", 'DataLims']
        config["plot_id"] = ["npunc", "scunc_l", "scunc_u", "pdfunc_l", "pdfunc_u"] 

        config["ratio"] = [
                           ["pdfunc_l", "nlo"], 
                           ["pdfunc_u", "nlo"], 
                           ["scunc_l", "nlo"], 
                           ["scunc_u", "nlo"], 
                           ["npunc", "npunc"], 
                           ["nlo", "nlo"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]

        config['plot_order'] = []

        config['objects']["scunc_l"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "_color2_", 
            "edgecolor": "auto", 
            "id": "scunc_l", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_scunc_l".format(rap_bin), 
            "label": "Scale Uncertainty", 
            "linestyle": "", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config['objects']["scunc_u"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "_color2_", 
            "edgecolor": "auto", 
            "id": "scunc_u", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_scunc_u".format(rap_bin), 
            "label": "__nolegend__", 
            "linestyle": "", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config['objects']["pdfunc_l"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "_color1_", 
            "edgecolor": "auto", 
            "id": "pdfunc_l", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_pdfunc_l".format(rap_bin), 
            "label": "PDF Uncertainty", 
            "linestyle": "", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config['objects']["pdfunc_u"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "_color1_", 
            "edgecolor": "auto", 
            "id": "pdfunc_u", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_pdfunc_u".format(rap_bin), 
            "label": "__nolegend__", 
            "linestyle": "", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config['objects']["npunc"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "auto", 
            "edgecolor": "auto", 
            "id": "nlo", 
            "input": "~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor".format(rap_bin), 
            "label": "NP Uncertainty", 
            "linestyle": "", 
            "marker": ".", 
            "step": True, 
            "style": "errorlines", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config['objects']["nlo"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "auto", 
            "edgecolor": "auto", 
            "id": "nlo", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_xs".format(rap_bin), 
            "label": "__nolegend__", 
            "linestyle": "", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
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
                              "s=NNPDF 3.0-NLO?_upperleft2_",
                              '_8tev_'] 

        config["output_path"] = 'theo_unc_overview_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

