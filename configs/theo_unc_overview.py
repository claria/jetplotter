import util.callbacks as callbacks

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

        config['ana_modules'] = ['BuildTGraph','DataLims', "Ratio",  "MinusOne", "ScaleUnc", 'QuadraticSum', ]

        config['build_tgraph'] = [
                                 ('scaleunc', ('nlo', 'scunc_l', 'scunc_u')),
                                 ('pdfunc', ('nlo', 'pdfunc_l', 'pdfunc_u')),
                                 ('asunc', ('nlo', 'asunc_l', 'asunc_u')),
                                 ]
        config['scale_unc'] = [
                             ('asunc', 1.5)
                             ]

        config['quadratic_sum'] = [
                                ('totalunc', ('scaleunc', 'pdfunc', 'npunc', 
                                    # 'asunc'
                                    )),
                                 ]

        config['minusone'] = ['npunc', 'pdfunc', 'scaleunc', 'asunc']

        config["plot_id"] = ['totalunc', 'npunc', '^scaleunc$', '^pdfunc$'
                             #, '^asunc$'
                             ] 

        config["ratio"] = [
                           ["scaleunc", "scaleunc"], 
                           ["pdfunc", "pdfunc"], 
                           ["npunc", "npunc"], 
                           ["asunc", "asunc"], 
                          ] 

        config["data_lims"] = [
                                ('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                              ]

        config['plot_order'] = ['totalunc', 'pdfunc', 'scaleunc', 'npunc', 'asunc']


        config['objects']["nlo"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_xs".format(rap_bin), 
        }
        config['objects']["asunc_l"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_as117_xs".format(rap_bin), 
        }
        config['objects']["asunc_u"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_as119_xs".format(rap_bin), 
        }

        config['objects']["scunc_l"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_scunc_l".format(rap_bin), 
        } 
        config['objects']["scunc_u"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_scunc_u".format(rap_bin), 
        } 
        config['objects']["pdfunc_l"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_pdfunc_l".format(rap_bin), 
        } 
        config['objects']["pdfunc_u"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_pdfunc_u".format(rap_bin), 
        } 

        config['objects']["npunc"] = {
            "input": "~/dust/dijetana/plot/np_factors.root?{0}/res_np_factor".format(rap_bin),
            "label": "NP", 
            "step": True, 
            "style": "errorlines", 
            "linestyle": "--",
            "zorder": 1.0
        } 
        config['objects']["pdfunc"] = {
            "label": "PDF", 
            "step": True, 
            "style": "errorlines", 
            "dashes": [20,4],
            "zorder": 1.0
        } 
        config['objects']["scaleunc"] = {
            "label": "Scale", 
            "step": True, 
            "dashes": [4,4,10,4],
            "style": "errorlines", 
            "zorder": 1.0
        } 
        config['objects']["asunc"] = {
            "label": "$\\alpha_s$", 
            "step": True, 
            # 'dashes': [16,4],
            "style": "errorlines", 
            "zorder": 1.0
        } 
        config['objects']["totalunc"] = {
            "label": "Total", 
            "step": True, 
            "style": "errorlines", 
            # 'dashes': [8,4],
            "color": "black",
            "zorder": 1.0
        } 


        config["y_lims"] = ["-0.35", "0.35"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'lower left'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Relative uncertainty?_center_"
        config["ax_hlines"] = [
                {'y' : 0.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_|size=32'.format(rap_bin), 
                              "s=NNPDF 3.0-NLO?_upperleft2_|size=32",
                              {'s': ur'CMS' , 'x': 0.55, 'y': 0.95, 'ha': 'center', 'va': 'top', 'size': 40, 'weight': 'bold'}, 
                              {'s': ur'Simulation' , 'x': 0.555, 'y': 0.875, 'ha': 'center', 'va': 'top', 'size': 18, 'style':'italic'}, 
                              '_8tev_'] 

        config["output_path"] = 'theo_unc_overview_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 28
