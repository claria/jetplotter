
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
        config['ana_modules'] = ["Normalize", "Multiply", "Ratio", "ToTGraph", "ReBinning"]
        # config["normalize"] = [("dataunf", "width")]
        config["normalize"] = [
                ('data', 'width'),
                ('dataunf_mgp6', 'width'),
                ('dataunf_mgp6_3d', 'width')
                ]
        config["multiply"] = [
                              ("nloct14", "_np")
                              ]
        config["ratio"] = [
                           ["data", "nloct14"], 
                           ["dataunf_mgp6", "nloct14"], 
                           ["dataunf_mgp6_3d", "nloct14"], 
                           ["dataunf_stat", "nloct14"], 
                           ["nloct14", "nloct14"],
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config["to_tgraph"] = [
                               "nloct14"] 
        config['plot_order'] = ['dataunf_stat', 'dataunf_syst', 'nloct14']


        config['objects']["_np"] = {
            "input": "~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor".format(rap_bin)
        } 
        config['objects']["data"] = {
            "color": "grey", 
            "edgecolor": "black", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data Reco", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

        config['objects']["dataunf_stat"] = {
            "color": "black", 
            "edgecolor": "black", 
            "input": "~/dust/dijetana/plot/data_summary.root?{0}/data_stat".format(rap_bin), 
            "label": "Data", 
            "marker": ".", 
            "step": False, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["dataunf_mgp6"] = {
            "color": "auto", 
            "edgecolor": "auto", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_QCDMGP6.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data - MGP6", 
            "marker": ".", 
            "step": False, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["dataunf_mgp6_3d"] = {
            "color": "auto", 
            "edgecolor": "auto", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_QCDMGP6_3D.root?idx/h_{0}_ptavg".format(rap_bin), 
            "label": "MGP6 3D", 
            "marker": ".", 
            "step": False, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["nloct14"] = {
            "alpha": 0.5, 
            "color": "_color0_", 
            "edgecolor": "_color0_", 
            "input_tgraph": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/CT14nlo_xs&~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/CT14nlo_pdfunc_l&~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/CT14nlo_pdfunc_u".format(rap_bin), 
            "label": "PDF Unc.", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "band", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        } 
        config["y_lims"] = ["0.0", "2.0"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "$p_\\mathrm{T,avg}$ (GeV)"
        config["y_label"] = "Ratio to NLO$\otimes$NP (CT14)?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'ratio_to_CT14nlo+np_unfolding_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

