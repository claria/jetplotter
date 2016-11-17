
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['default', 'yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []
    for rap_bin in rap_bins:
        config = get_base_config()
        config['ana_modules'] = ["Ratio"]

        config["ratio"] = [
                           ["miss_ptavg", "all_ptavg"], 
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config['objects']["all_ptavg"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_study_smeared2_QCDMGP6.root?{0}/h_unf_gen_ptavg".format(rap_bin), 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "no_plot": True, 
        }
        config['objects']["miss_ptavg"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_study_smeared2_QCDMGP6.root?{0}/h_unf_ybys_miss_ptavg".format(rap_bin), 
            "label": "MG+P6",
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
        }


        config["y_lims"] = ["0.0", "1.0"]

        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "$p_\\mathrm{T,avg}$ (GeV)"
        config["y_label"] = "Fraction?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'dijet_ybys_miss_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

