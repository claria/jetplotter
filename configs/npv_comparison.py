
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
        config['ana_modules'] = ['Normalize', "Ratio", "DataLims"]
        config['normalize'] = [
                            ['npv_low', 'unity'],
                            ['npv_high', 'unity'],
                            ]
        config["ratio"] = [
                           ["npv_high", "npv_low"], 
                           ["npv_low", "npv_low"], 
                          ] 
        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),]

        config['plot_id'] = ['npv_high']

        config['objects']["npv_high"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/NPV_STUDY_HIGH_QCDMGP6.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Hig NPV(>15)/Low NPV(<15)"
        }
        config['objects']["npv_low"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/NPV_STUDY_LOW_QCDMGP6.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Run B"
        }

        config["y_lims"] = ["0.0", "2.0"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Ratio?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'npv_comparison_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

