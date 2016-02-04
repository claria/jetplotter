
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    hlt_paths = ['HLT_PFJET80', 'HLT_PFJET140','HLT_PFJET200','HLT_PFJET260','HLT_PFJET320']
    ref_hlt_paths = ['HLT_PFJET40', 'HLT_PFJET80', 'HLT_PFJET140','HLT_PFJET200','HLT_PFJET260']
    rap_bins = ['default', 'yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []

    for ref_hlt_path, hlt_path in zip(ref_hlt_paths, hlt_paths):
        print ref_hlt_path,hlt_path
        for rap_bin in rap_bins:
            config = get_base_config()
            config['ana_modules'] = [
                                    "Efficiency", 
                                    "TriggerEfficiencyFit"
                                    ]
            config["trigger_efficiency_fit"] = [("eff_emul", "{}")]
            config["efficiency"] = [("_emul", "_trg")] 



            config['objects']['_trg'] = {
                    "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TRIGGER_PTAVG_DATA.root?{0}/TriggerEffs/{1}".format(rap_bin, ref_hlt_path), 
                    "label": "trg"
            }
            config['objects']["fit_eff_emul"] = {
                    "style": "line"
            } 
            config['objects']["eff_emul"] = {
                    "color": "black", 
                    "label": "{0}".format(hlt_path)
            } 
            config['objects']["_emul"] = {
                    "input": "~/dust/dijetana/ana/CMSSW_7_2_3/TRIGGER_PTAVG_DATA.root?{0}/TriggerEffs/emul_{1}".format(rap_bin, hlt_path), 
                    "label": "emul"
            }


            config["y_lims"] = ["0.0", "1.1"]
            config["x_lims"] = [50., 1000.]
            config['margin'] = 0.05
            config["x_log"] =  True
            config["x_label"] = "_ptavg_"
            config["y_label"] = "Efficiency"
            config["ax_texts"] = [
                                "_20fb_",
                                "_{0}_?_upperleft_".format(rap_bin),
                                ] 
            config["output_path"] = 'trigger_eff_{}_{}.png'.format(hlt_path, rap_bin)
            configs.append(config)

    return configs

