
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    quantities = ['neutralHadronFraction', 'chargedHadronFraction', 'neutralEMFraction', 'electronFraction', 'muonFraction', 'nConstituents', 'nCharged']
    x_labels = ['neutral hadron fraction', 'charged hadron fraction', 'photon fraction', 'electron fraction', 'muon fraction', 'n constituents', 'n charged constituents']
    x_lims = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 200), (0.0, 200)]
    y_lims = [(1.1E-4, 1.1), (1.1E-4, 1.1), (1.1E-4, 1.1), (1.1E-4, 1.1), (1.1E-4, 1.1), (1.1E-7, 1.1), (1.1E-7, 1.1)]
    configs = []

    for i, quantity in enumerate(quantities):
        config = get_base_config()

        config['ana_modules'] = ['Normalize', 'Ratio']
        config['normalize'] = [('mgp6', 'unity'), ('data', 'unity')]
        config['ratio_copy'] = [('mgp6', 'data'),]
        # config['plot_id'] = '^corr$'

        config['objects']["ratio_mgp6_to_data"] = {
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
        config['y_log'] = True
        config["y_lims"] = y_lims[i]
        config["y_subplot_lims"] = [0.0, 2.00]
        config["x_lims"] = x_lims[i]
        config['x_log'] = False
        config["x_label"] = "{0}".format(x_labels[i])
        config["y_label"] = "arb. unit"
        config["legend_loc"] = 'upper right'
        config["ax_hlines"] = [
                {'axis': 'ax1', 'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                            "_20fb_",
                            ] 
        config["output_path"] = 'jet_constituent_{}.png'.format(quantity)
        configs.append(config)

    return configs

