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
                          "_y0",
                          "_y1",
                          "_y2",
                          "_y3",
                          "_y4",
                          "_y5",
                          "_y6"
                         ]
    config['plot_order'] = [
                            'resolution_y0_fit',
                            'resolution_y1_fit',
                            'resolution_y2_fit',
                            'resolution_y3_fit',
                            'resolution_y4_fit',
                            'resolution_y5_fit',
                            'resolution_y6_fit',
                            ]

    config['objects']["_y0"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_notsmeared_QCDMGP6.root?default/h2_genrecopt_y0", 
        "label": "__nolegend__", 
    } 
    config['objects']["_y1"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_notsmeared_QCDMGP6.root?default/h2_genrecopt_y1", 
        "label": "__nolegend__", 
    } 
    config['objects']["_y2"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_notsmeared_QCDMGP6.root?default/h2_genrecopt_y2", 
        "label": "__nolegend__", 
    } 
    config['objects']["_y3"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_notsmeared_QCDMGP6.root?default/h2_genrecopt_y3", 
        "label": "__nolegend__", 
    } 
    config['objects']["_y4"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_notsmeared_QCDMGP6.root?default/h2_genrecopt_y4", 
        "label": "__nolegend__", 
    } 
    config['objects']["_y5"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_notsmeared_QCDMGP6.root?default/h2_genrecopt_y5", 
        "label": "__nolegend__", 
    } 
    config['objects']["_y6"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/resolution_notsmeared_QCDMGP6.root?default/h2_genrecopt_y6", 
        "label": "__nolegend__", 
    } 

    config['objects']["resolution_y0_fit"] = {
        "color": "_color0_", 
        "label": "$0.0 \leq |y| < 0.5$", 
        "style": "line"
    } 
    config['objects']["resolution_y1_fit"] = {
        "color": "_color1_", 
        "label": "$0.5 \leq |y| < 1.1$", 
        "style": "line"
    } 
    config['objects']["resolution_y2_fit"] = {
        "color": "_color2_", 
        "label": "$1.1 \leq |y| < 1.7$", 
        "style": "line"
    } 
    config['objects']["resolution_y3_fit"] = {
        "color": "_color3_", 
        "label": "$1.7 \leq |y| < 2.3$", 
        "style": "line"
    } 
    config['objects']["resolution_y4_fit"] = {
        "color": "_color4_", 
        "label": "$2.3 \leq |y| < 2.8$", 
        "style": "line"
    } 
    config['objects']["resolution_y5_fit"] = {
        "color": "_color5_", 
        "label": "$2.8 \leq |y| < 3.2$", 
        "style": "line"
    } 
    config['objects']["resolution_y6_fit"] = {
        "color": "green",
        "label": "$3.0 \leq |y| < 5.0$", 
        "style": "line"
    } 

    config['objects']["resolution_y0"] = {
        "color": "_color0_"
    } 
    config['objects']["resolution_y1"] = {
        "color": "_color1_"
    } 
    config['objects']["resolution_y2"] = {
        "color": "_color2_"
    } 
    config['objects']["resolution_y3"] = {
        "color": "_color3_"
    } 
    config['objects']["resolution_y4"] = {
        "color": "_color4_"
    } 
    config['objects']["resolution_y5"] = {
        "color": "_color5_"
    } 
    config['objects']["resolution_y6"] = {
        "color": "green"
    } 


    # config['fig_size'] = [10., 10.]
    config['y_log'] = False
    config["y_lims"] = [0.0, 0.20]
    config["x_log"] = True
    config["x_axis_formatter"] = 'scalar2'
    config["x_lims"] = [30., 2000.]
    config["legend_loc"] = 'upper right'
    config["x_label"] = "_ptgen_"
    config["y_label"] = "Relative resolution $\Delta p_{\mathrm{T}}^{\mathrm{ptcl}}/p_{\mathrm{T}}^{\mathrm{ptcl}}$"

    config["ax_texts"] = [
                          "_8tev_", 
                          ]

    config["output_path"] = 'resolution_pt_crystalball.png'
    configs.append(config)
    return configs


@callbacks.register('after_plot')
def final_plot(**kwargs):
    print 'hallo'

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    kwargs['mpl'].rcParams['font.size'] = 20
