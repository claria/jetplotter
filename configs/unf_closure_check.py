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
        config['ana_modules'] = ["Normalize", "ReBinning", 'Ratio']
        config["ratio"] = [
                           ["mgp6_reco", "mgp6_gen"], 
                           ["mgp6_gen", "mgp6_gen"], 
                           ["mgp6_response_reco", "mgp6_response_gen"], 
                           ["data_reco_mgp6", "mgp6_unf"], 
                           ["data_reco_mgp6_3d", "mgp6_unf_3d"], 
                           ["data_reco_p8", "p8_unf"], 
                           ["data_reco_fnlo", "fnlo_unf"], 
                           ["data_reco_fnlo_test", "fnlo_unf_test"], 
                           ["p8_reco", "p8_gen"], 
                           ["p8_gen", "p8_gen"], 
                           # ["fnlo_reco", "fnlo_gen"], 
                           ["fnlo_reco_test", "fnlo_gen_test"], 
                           # ["fnlo_gen", "fnlo_gen"], 
                          ] 

        config['normalize'] = [
            # ('mgp6_reco', 'width'),
            # ('mgp6_gen', 'width')
                ]
        config['plot_id'] = [
                    'mgp6_reco',
                    # 'mgp6_response_reco',
                    # 'fnlo_reco',
                    'fnlo_reco_test',
                    # 'p8_reco',
                    'data_reco_mgp6$',
                    # 'data_reco_mgp6_3d',
                    # 'data_reco_p8',
                    # 'data_reco_fnlo',
                    'data_reco_fnlo_test',
                ]
        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config['plot_order'] = ['dataunf_stat', 'dataunf_syst', 'nloct14']

        config['objects']["mgp6_reco"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/SMEARED_NEW2_QCDMGP6.root?{0}/h_ptavg".format(rap_bin), 
            "label": "MGP6 Reco/MGP6 Gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 8.0
        }
        config['objects']["mgp6_gen"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/SMEARED_NEW2_QCDMGP6.root?gen_{0}/h_genptavg".format(rap_bin), 
            "label": "Madgraph Gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["mgp6_response_reco"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_study_smeared2_QCDMGP6.root?{0}/h_unf_reco_ptavg".format(rap_bin), 
            "label": "MGP6 Reco/MGP6 Gen (Response)", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 12.0
        }
        config['objects']["mgp6_response_gen"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_study_smeared2_QCDMGP6.root?{0}/h_unf_gen_ptavg".format(rap_bin), 
            "label": "Madgraph Gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["data_reco_mgp6"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data Reco/Data Unf (MGP6)", 
            "marker": ".",
            "step": True,
            "style": "line",
            "x_err": True,
            "y_err": True,
            "zorder": 5.0
        }
        config['objects']["data_reco_mgp6_3d"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data Reco/Data Unf (MGP6 - 3D)", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

        config['objects']["data_reco_p8"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data Reco/Data Unf (P8)", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["data_reco_fnlo"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data Reco/Unf (fnlo)", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["data_reco_fnlo_test"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/DATA.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data Reco/Unf (fnlo)", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

        config['objects']["p8_reco"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_study_QCDP8.root?{0}/h_unf_reco_ptavg".format(rap_bin), 
            "label": "P8 Reco/P8 Gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["p8_gen"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_study_QCDP8.root?{0}/h_unf_gen_ptavg".format(rap_bin), 
            "label": "P8 gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

        config['objects']["p8_unf"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_QCDP8.root?{0}/h_ptavg".format(rap_bin), 
            "label": "P8 unf", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

        config['objects']["fnlo_reco"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_fastNLO.root?{0}/h_recoptavg".format(rap_bin), 
            "label": "fastNLO Reco(smeared)/fastNLO Gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["fnlo_reco_test"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_fastNLO_test.root?{0}/h_recoptavg".format(rap_bin), 
            "label": "fastNLO Reco(smeared)/fastNLO Gen (with fakes/miss)", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }


        config['objects']["fnlo_unf"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg".format(rap_bin), 
            "label": "fnlo Reco/ fnlo Gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["fnlo_unf_test"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO_WITHFAKES.root?{0}/h_ptavg".format(rap_bin), 
            "label": "fnlo Reco/ fnlo Gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }
        config['objects']["fnlo_gen"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_fastNLO.root?{0}/h_genptavg".format(rap_bin), 
            "label": "fnlo gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

#
#
        config['objects']["fnlo_gen_test"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/response_fastNLO_test.root?{0}/h_genptavg".format(rap_bin), 
            "label": "fnlo gen", 
            "marker": ".", 
            "step": True, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }


        config['objects']["mgp6_unf"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_QCDMGP6.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Madgraph Unf", 
            "marker": ".", 
            "step": False, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }

        config['objects']["mgp6_unf_3d"] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_QCDMGP6_3D.root?idx/h_{0}_ptavg".format(rap_bin), 
            "label": "Madgraph Unf", 
            "marker": ".", 
            "step": False, 
            "style": "line", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 3.0
        }


        config["y_lims"] = ["0.8", "1.5"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["legend_loc"] = 'upper right'
        config["x_label"] = "$p_\\mathrm{T,avg}$ (GeV)"
        config["y_label"] = "Ratio to Gen?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = [
                              '_{0}_?_upperleft_'.format(rap_bin), 
                              '_20fb_'] 

        config["output_path"] = 'unf_closure_check_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 14
    kwargs['mpl'].rcParams['lines.linewidth'] = 4
    # kwargs['mpl'].rcParams['font.size'] = 20
