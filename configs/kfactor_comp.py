
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

        config['ana_modules'] = ['ReBinning']
        config['data_lims'] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),]
        config['objects']['ct14nlo_kfac_ptavg'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_DEF_YBYS_NLO.root?{0}/CT14nlo_kfac'.format(rap_bin),
                'color' : '_color0_',
                'style' : 'line',
                'linestyle' : '-',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,avg}}$',
                }
        config['objects']['ct14nlo_kfac_ptmax'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_kfac'.format(rap_bin),
                'color' : '_color1_',
                'style' : 'line',
                'linestyle' : '-',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,max}}\exp{(0.3y^*)}$',
                }
        config['objects']['ct14nlo_kfac_ptavgexpystar'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVGEXPYS_YBYS_NLO.root?{0}/CT14nlo_kfac'.format(rap_bin),
                'color' : '_color2_',
                'style' : 'line',
                'linestyle' : '--',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,avg}}\exp{(0.3y^*)}$',
                }


        config["y_lims"] = ["0.5", "2.0"]
        config["x_lims"] = ["133.", "2000."]
        config["x_log"] =  True
        config["x_label"] = "_ptavg_"
        config["y_label"] = "k-factor?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = ["_{0}_?_upperleft_".format(rap_bin), '_8tev_'] 

        config["output_path"] = 'kfactor_comp_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

