import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    configs = []

    config = get_base_config()

    config['ana_modules'] = ["CrystalBallResolutionAna"]
    config['output_modules'] = ['RootOutputModule', 'PlotModule']

    config["resolution"] = [
                          "_yb0ys0", 
                          "_yb1ys0", 
                          "_yb2ys0", 
                          "_yb0ys1", 
                          "_yb0ys2", 
                          "_yb1ys1"
                         ]


    config['objects']["_yb1ys1"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "auto", 
            "edgecolor": "auto", 
            "id": "_yb1ys1", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_QCDMGP6.root?yb1ys1/h2_GenVsRecoPtAvg", 
            "label": "__nolegend__", 
            "linestyle": "", 
            "marker": ".", 
            "step": False, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
    } 
    config['objects']["resolution_yb0ys2_fit"] = {
        "color": "_color2_", 
        "label": "_yb0ys2_", 
        "style": "line"
    } 
    config['objects']["resolution_yb1ys1_fit"] = {
        "color": "_color4_", 
        "label": "_yb1ys1_", 
        "style": "line"
    } 
    config['objects']["resolution_yb0ys0_fit"] = {
        "color": "_color0_", 
        "label": "_yb0ys0_", 
        "style": "line"
    } 
    config['objects']["resolution_yb1ys0_fit"] = {
        "color": "_color3_", 
        "label": "_yb1ys0_", 
        "style": "line"
    } 
    config['objects']["resolution_yb2ys0_fit"] = {
        "color": "_color5_", 
        "label": "_yb2ys0_", 
        "style": "line"
    } 
    config['objects']["resolution_yb0ys2"] = {
        "color": "_color2_"
    } 
    config['objects']["resolution_yb0ys1"] = {
        "color": "_color1_"
    } 
    config['objects']["resolution_yb0ys0"] = {
        "color": "_color0_"
    } 
    config['objects']["_yb2ys0"] = {
        "alpha": 1.0, 
        "axis": "ax", 
        "capsize": 0, 
        "cmap": "viridis", 
        "color": "auto", 
        "edgecolor": "auto", 
        "id": "_yb2ys0", 
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_QCDMGP6.root?yb2ys0/h2_GenVsRecoPtAvg", 
        "label": "__nolegend__", 
        "linestyle": "", 
        "marker": ".", 
        "step": False, 
        "style": "errorbar", 
        "x_err": True, 
        "y_err": True, 
        "zorder": 1.0
    } 
    config['objects']["resolution_yb2ys0"] = {
        "color": "_color5_"
    } 
    config['objects']["_yb0ys1"] = {
        "alpha": 1.0, 
        "axis": "ax", 
        "capsize": 0, 
        "cmap": "viridis", 
        "color": "auto", 
        "edgecolor": "auto", 
        "id": "_yb0ys1", 
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_QCDMGP6.root?yb0ys1/h2_GenVsRecoPtAvg", 
        "label": "__nolegend__", 
        "linestyle": "", 
        "marker": ".", 
        "step": False, 
        "style": "errorbar", 
        "x_err": True, 
        "y_err": True, 
        "zorder": 1.0
    } 
    config['objects']["_yb0ys0"] = {
        "alpha": 1.0, 
        "axis": "ax", 
        "capsize": 0, 
        "cmap": "viridis", 
        "color": "auto", 
        "edgecolor": "auto", 
        "id": "_yb0ys0", 
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_QCDMGP6.root?yb0ys0/h2_GenVsRecoPtAvg", 
        "label": "__nolegend__", 
        "linestyle": "", 
        "marker": ".", 
        "step": False, 
        "style": "errorbar", 
        "x_err": True, 
        "y_err": True, 
        "zorder": 1.0
    } 
    config['objects']["_yb1ys0"] = {
        "alpha": 1.0, 
        "axis": "ax", 
        "capsize": 0, 
        "cmap": "viridis", 
        "color": "auto", 
        "edgecolor": "auto", 
        "id": "_yb1ys0", 
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_QCDMGP6.root?yb1ys0/h2_GenVsRecoPtAvg", 
        "label": "__nolegend__", 
        "linestyle": "", 
        "marker": ".", 
        "step": False, 
        "style": "errorbar", 
        "x_err": True, 
        "y_err": True, 
        "zorder": 1.0
    } 
    config['objects']["_yb0ys2"] = {
        "alpha": 1.0, 
        "axis": "ax", 
        "capsize": 0, 
        "cmap": "viridis", 
        "color": "auto", 
        "edgecolor": "auto", 
        "id": "_yb0ys2", 
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_QCDMGP6.root?yb0ys2/h2_GenVsRecoPtAvg", 
        "label": "__nolegend__", 
        "linestyle": "", 
        "marker": ".", 
        "step": False, 
        "style": "errorbar", 
        "x_err": True, 
        "y_err": True, 
        "zorder": 1.0
    } 
    config['objects']["resolution_yb0ys1_fit"] = {
        "color": "_color1_", 
        "label": "_yb0ys1_", 
        "style": "line"
    } 
    config['objects']["resolution_yb1ys0"] = {
        "color": "_color3_"
    } 
    config['objects']["resolution_yb1ys1"] = {
        "color": "_color4_"
    }


    # config['fig_size'] = [10., 10.]
    config['y_log'] = False
    config["y_lims"] = [0.0, 0.20]
    config["x_log"] = True
    config["x_axis_formatter"] = 'scalar2'
    config["x_lims"] = [50., 2000.]
    config["legend_loc"] = 'upper right'
    config["x_label"] = "_ptavggen_"
    config["y_label"] = "Relative resolution $\Delta p_{\mathrm{T,avg}}/p_{\mathrm{T,avg}}$"

    config["ax_texts"] = [
                          "_8tev_", 
                          ]

    config["output_path"] = 'resolution_ptavg_crystalball.png'
    configs.append(config)
    return configs


@callbacks.register('after_plot')
def final_plot(**kwargs):
    print 'hallo'

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    kwargs['mpl'].rcParams['font.size'] = 20
