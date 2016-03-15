
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    configs = []

    quantities = ['dijet_mass', 'ptavg', 'dijet_costhetastar', 'dijet_yboost', 'dijet_ystar', 'dijet_chi', 'dijet_deltaphi', 'dijet_deltar'] 
    x_logs = [True, True, False, False, False, True, False, False]
    y_logs = [True, True, True, True, True, True, False, False]
    y_lims = [(1.1E-10, 1.0), (1.1E-8, 1E0), (1.1E-4, 1E0), (1.1E-4, 1E0), (1.1E-6, 1E0), (1.1E-4, 1E-1), (0.0, 0.2), (0.0, 0.2)]
    x_lims = [(300., 6000.), (133., 2000.), (-1.0, 1.0), (-4.0, 4.0), (-4.0, 4.0), (1.0, 80.), (1., 5.0), (2., 6.0)]
    x_labels = ['$M_{1,2}$ (GeV)' ,'_ptavg_', 'costhetastar', '$0.5(y_1+y_2)$', '$0.5(y_1-y_2)$', '$\chi$', '$\Delta \phi_{1,2}$', '$\Delta R_{1,2}$']

    for i, quantity in enumerate(quantities):
        config = get_base_config()

        config['ana_modules'] = ['Normalize', 'Ratio']
        config['normalize'] = [('mgp6', 'unity'), ('data', 'unity')]
        config['ratio_copy'] = [('data', 'mgp6'),]
        # config['plot_id'] = '^corr$'

        config['objects']["ratio_data_to_mgp6"] = {
            "axis": "ax1", 
            "color": "black", 
            "label": "__nolegend__", 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
        } 
        config['objects']["data"] = {
            "axis": "ax", 
            "color": "black", 
            "input": "/afs/desy.de/user/g/gsieber/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?default/h_{0}".format(quantity), 
            "label": "Data", 
            "linestyle": "", 
            "marker": ".", 
            "step": False, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 2.0
        } 
        config['objects']["mgp6"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "color": "_color0_", 
            "input": "/afs/desy.de/user/g/gsieber/dust/dijetana/ana/CMSSW_7_2_3/QCDMGP6.root?default/h_{0}".format(quantity), 
            "label": "MG+P6", 
            "linestyle": "", 
            "marker": ".", 
            "style": "histo", 
            "zorder": 1.0
        }
        config['add_subplot'] = True
        config['y_axis_formatter'] = 'scientific'
        config['y_log'] = y_logs[i]
        config["y_lims"] = y_lims[i]
        config["y_subplot_lims"] = [0.0, 2.0]
        config["x_lims"] = x_lims[i]
        config['x_log'] = x_logs[i]
        config["x_label"] = "{0}".format(x_labels[i])
        config["y_label"] = "arb. unit"
        config["y_subplot_label"] = "Ratio to MC"
        config["legend_loc"] = 'upper right'
        config["ax_hlines"] = [
                {'axis': 'ax1', 'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                            "_20fb_",
                            ] 
        config["output_path"] = 'dijet_quantities_{}.png'.format(quantity)
        configs.append(config)

    return configs

