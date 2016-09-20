
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
        config['ana_modules'] = ["DataLims"]


        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),]

        config['objects']["ewk"] = {
            "input": "~/dust/dijetana/ewk/ewk_dijet.root?{0}/ewk_corr".format(rap_bin),
            "color": "black",
            'label': 'Correction',
            'alpha': 1.0,
            "zorder": 2.5,
        } 

        config["data_lims"] = [
                               ('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                              ]

        config['plot_id'] = [
                             'ewk'
                             ]

        config["y_lims"] = ["0.88", "1.4"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "EW Correction"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin),
                             ] 

        config["output_path"] = 'ew_factors_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

