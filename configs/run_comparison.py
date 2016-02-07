
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
                            ['run_a', '1.1363'],
                            ['run_b', '0.222'],
                            ['run_c', '0.141643'],
                            ['run_d', '0.1356'],
                            ]
        config["ratio"] = [
                           ["run_a", "run_d"], 
                           ["run_b", "run_d"], 
                           ["run_c", "run_d"], 
                           ["run_d", "run_d"], 
                          ] 
        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),]

        config['plot_order'] = ['run_a', 'run_b', 'run_c', 'run_d']

        config['objects']["run_a"] = {
            "input": "~/dust/ARTUS/artus_2015-11-10_08-50/DATA_A.root?yb0ys0/h_ptavg", 
            "label": "Run A"
        }
        config['objects']["run_b"] = {
            "input": "~/dust/ARTUS/artus_2015-11-10_08-50/DATA_B.root?yb0ys0/h_ptavg", 
            "label": "Run B"
        }
        config['objects']["run_c"] = {
            "input": "~/dust/ARTUS/artus_2015-11-10_08-50/DATA_C.root?yb0ys0/h_ptavg", 
            "label": "Run C"
        }
        config['objects']["run_d"] = {
            "input": "~/dust/ARTUS/artus_2015-11-10_08-50/DATA_D.root?yb0ys0/h_ptavg", 
            "label": "Run D"
        }

        config["y_lims"] = ["0.0", "2.0"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Ratio to Run D?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'run_comparison_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

