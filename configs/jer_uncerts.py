
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
        config['ana_modules'] = ["BuildTGraph", "Ratio"]
        config['output_modules'] = ["PlotModule", "RootOutputModule"]
        # config["normalize"] = [("dataunf", "width")]
        config['build_tgraph'] = [
                                    ['jer_uncert', ['_def', 'dn', 'up']]
                                 ]
        config["ratio"] = [
                        ["jer_uncert", "jer_uncert"],
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)})]

        config['objects']['_def'] = {
                "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO_unc_def.root?{0}/h_recoptavg".format(rap_bin), 
                }
        config['objects']['up'] = {
                "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO_unc_up.root?{0}/h_recoptavg".format(rap_bin), 
                }
        config['objects']['dn'] = {
                "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO_unc_dn.root?{0}/h_recoptavg".format(rap_bin), 
                }

        config['objects']['jer_uncert'] = {
                "label": "JER Uncert.",
                "color": "_color1_",
                "style": "errorlines",
                "step":True,
                }

        config['plot_id'] = ['jer_uncert']
        config["y_lims"] = ["0.95", "1.05"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] =  "upper right"
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Frac. Uncert?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = ['_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'jer_uncert_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

