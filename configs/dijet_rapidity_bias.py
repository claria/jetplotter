
def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['default', 'yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    config = get_base_config()
    config['ana_modules'] = []

    config['objects']["mgp6"] = {
        "input": "~/dust/dijetana/ana/CMSSW_7_2_3/rapidity_QCDMGP6.root?default/tp2_DeltaY", 
        "step": True, 
        "style": "heatmap", 
        "cmap": "bwr",
        "x_err": True, 
        "y_err": True, 
    }


    config["y_lims"] = ["-5.0", "5.0"]
    config["z_lims"] = ["-0.1", "0.1"]

    config["x_lims"] = [30.0, 2000.0]
    config["x_log"] =  True
    config["legend_loc"] = 'upper right'
    config["x_label"] = "$p_\\mathrm{T,avg}$ (GeV)"
    config["y_label"] = "Gen y - Reco y?_center_"
    config["ax_hlines"] = [
            ]
    config["ax_texts"] = [
                          '_20fb_'] 

    config["output_path"] = 'dijet_rapidity_bias.png'

    return [config]

