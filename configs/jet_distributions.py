
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    configs = []

    quantities = ['jet1pt', 'jet2pt', 'jet1rap', 'jet2rap', 'jet1phi', 'jet2phi'] 
    x_logs = [True, True, False, False, False, False]
    y_logs = [True, True, True, True, True, True]
    y_lims = [(1.1E-7, 1E8), (1.1E-7, 1E8), (1.1E1, 1E5), (1.1E1, 1E5), (1.1E1, 1E5), (1.1E1, 1E5)]
    x_lims = [(133., 2000.), (133., 2000.), (-3.5, 3.5), (-3.5, 3.5), (-3.5, 3.5), (-3.5, 3.5)]
    x_labels = ['leading jet $p_{\mathrm{T}}$ (GeV)', 'second jet $p_{\mathrm{T}}$ (GeV)', 'leading jet $y$', 'second jet $y$', 'leading jet $\phi$', 'second jet $\phi$']
    normalize = [False, False, True, True, True, True]

    for i, quantity in enumerate(quantities):
        config = get_base_config()

        config['ana_modules'] = ['Normalize', 'Ratio']
        if not normalize[i]:
            config['ana_modules'].remove('Normalize')

        config['normalize'] = [
                               ('mgp6', 'data'), 
                               ]
        config['ratio_copy'] = [('data', 'mgp6'),]

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
        config["output_path"] = 'jet_quantities_{}.png'.format(quantity)
        configs.append(config)

    return configs

