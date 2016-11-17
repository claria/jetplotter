import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    configs = []

    config = get_base_config()

    config['output_modules'] = ['PlotModule']

    config['plot_order'] = [
                            'yb0ys0',
                            'yb0ys1',
                            'yb0ys2',
                            'yb1ys0',
                            'yb1ys1',
                            'yb2ys0',
                            ]

    config['objects']["yb0ys0"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/yb0ys0/output.root?chi2", 
        "color": "_color0_", 
        "label": "_yb0ys0_", 
        "style": "line"
    } 
    config['objects']["yb0ys1"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/yb0ys1/output.root?chi2", 
        "color": "_color1_", 
        "label": "_yb0ys1_", 
        "style": "line"
    } 
    config['objects']["yb0ys2"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/yb0ys2/output.root?chi2", 
        "color": "_color2_", 
        "label": "_yb0ys2_", 
        "style": "line"
    } 
    config['objects']["yb1ys0"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/yb1ys0/output.root?chi2", 
        "color": "_color3_", 
        "label": "_yb1ys0_", 
        "style": "line"
    } 
    config['objects']["yb1ys1"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/yb1ys1/output.root?chi2", 
        "color": "_color4_", 
        "label": "_yb1ys1_", 
        "style": "line"
    } 
    config['objects']["yb2ys0"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/FoldingBack/yb2ys0/output.root?chi2", 
        "color": "_color5_", 
        "label": "_yb2ys0_", 
        "style": "line"
    } 

    # config['fig_size'] = [10., 10.]
    config['y_log'] = False
    config["y_lims"] = [0.0, 30.]
    config["x_log"] = False
    config["x_axis_formatter"] = 'scalar2'
    config["x_lims"] = [0, 10.]
    config["legend_loc"] = 'upper right'
    config["x_label"] = "Number of iterations"
    config["y_label"] = "Reduced $\chi^2 / ndof$"

    config["ax_texts"] = [
                          "_8tev_", 
                          ]

    config["output_path"] = 'folding_back_chi2.png'
    configs.append(config)
    return configs


@callbacks.register('after_plot')
def final_plot(**kwargs):
    print 'hallo'

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    kwargs['mpl'].rcParams['font.size'] = 20
