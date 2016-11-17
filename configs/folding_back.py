
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
        config['ana_modules'] = [
                                  "Normalize", 
                                  "Ratio", 
                                  "ReBinning"
                                ]
        # config["normalize"] = [("dataunf", "width")]
        config["normalize"] = [
                ]
        config["ratio"] = [
                           ["backfolded_1", "reco"],
                           ["backfolded_2", "reco"],
                           ["backfolded_4", "reco"],
                           ["backfolded_8", "reco"],
                          ] 

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)})]
        config['plot_id'] = [
                            'backfolded_1',
                            'backfolded_2',
                            'backfolded_4',
                            'backfolded_8',
                            ]


        config['objects']["reco"] = {
            "input": "/afs/desy.de/user/g/gsieber/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/{0}/output.root?Reco".format(rap_bin), 
        } 
        config['objects']["backfolded_1"] = {
            "alpha": 1.0, 
            "color": "_color0_", 
            "edgecolor": "_color0_", 
            "input": "/afs/desy.de/user/g/gsieber/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/{0}/output.root?refolded_1".format(rap_bin), 
            "label": "Backfolded (n=1) / Reco", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
        } 
        config['objects']["backfolded_2"] = {
            "alpha": 1.0, 
            "color": "_color1_", 
            "edgecolor": "_color1_", 
            "input": "/afs/desy.de/user/g/gsieber/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/{0}/output.root?refolded_2".format(rap_bin), 
            "label": "Backfolded (n=2) / Reco", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
        } 
        config['objects']["backfolded_4"] = {
            "alpha": 1.0, 
            "color": "_color2_", 
            "edgecolor": "_color2_", 
            "input": "/afs/desy.de/user/g/gsieber/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/{0}/output.root?refolded_4".format(rap_bin), 
            "label": "Backfolded (n=4) / Reco", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
        } 
        config['objects']["backfolded_8"] = {
            "alpha": 1.0, 
            "color": "_color4_", 
            "edgecolor": "_color4_", 
            "input": "/afs/desy.de/user/g/gsieber/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/{0}/output.root?refolded_8".format(rap_bin), 
            "label": "Backfolded (n=8) / Reco", 
            "linestyle": "", 
            "marker": ".", 
            "plot": True, 
            "step": True, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
        } 

        config["y_lims"] = ["0.8", "1.5"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        # config['x_lims'] = [30., 3000.]
        config["x_log"] =  True
        config["y_log"] =  False
        config["legend_loc"] = 'upper right'
        config["x_label"] = "$p_\\mathrm{T,avg}$ (GeV)"
        config["y_label"] = "Ratio to Reco?_center_"
        # config["ax_hlines"] = [
        #         {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
        #         ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_8tev_'] 

        config["output_path"] = 'folding_back_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

