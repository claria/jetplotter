
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

        config['ana_modules'] = ['BuildTGraph',"Ratio", "MinusOne", 'DataLims']

        config['build_tgraph'] = [
                                 ('scaleunc', ('nlo', 'scunc_l', 'scunc_u')),
                                 ('pdfunc', ('nlo', 'pdfunc_l', 'pdfunc_u')),
                                 ]
        config['minusone'] = ['npunc', 'pdfunc', 'scaleunc']

        config["plot_id"] = ['npunc', '^scaleunc$', '^pdfunc$'] 

        config["ratio"] = [
                           ["scaleunc", "scaleunc"], 
                           ["pdfunc", "pdfunc"], 
                           ["npunc", "npunc"], 
                          ] 

        config["data_lims"] = [
                                ('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                              ]

        config['plot_order'] = []


        config['objects']["nlo"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_xs".format(rap_bin), 
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
            "input": "~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor".format(rap_bin), 
            "label": "NP uncertainty", 
            "step": True, 
            "style": "errorlines", 
            'dashes': [8,4],
            "zorder": 1.0
        } 
        config['objects']["pdfunc"] = {
            "label": "PDF uncertainty", 
            "step": True, 
            "style": "errorlines", 
            "zorder": 1.0
        } 
        config['objects']["scaleunc"] = {
            "label": "Scale uncertainty", 
            "step": True, 
            'dashes': [16,4],
            "style": "errorlines", 
            "zorder": 1.0
        } 


        config["y_lims"] = ["-0.3", "0.3"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Relative Uncertainty?_center_"
        config["ax_hlines"] = [
                {'y' : 0.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              "s=NNPDF 3.0-NLO?_upperleft2_",
                              '_8tev_'] 

        config["output_path"] = 'theo_unc_overview_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

