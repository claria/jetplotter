import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_q2label(q2):
    q2_str = r'{:.2G}'.format(q2)
    if "E" in q2_str:
        base, exponent = q2_str.split('E')
        if base == '1':
            return r"10^{{{1}}}".format(base, int(exponent))
        else:
            return r"{0}\times 10^{{{1}}}".format(base, int(exponent))
    else:
        return q2_str

ymax_lim = { 
        0 : {1.9 : 4.0},
        7 : {1.9 : 0.6, 10000 : 0.6},
        8 : {1.9 : 1.0, 10000 : 1.0},
        }


def get_config():
    configs = []
    partons = [0, 7, 8, 9]
    names = ['gluon', 'd valence quark', 'u valence quark', 'sea quarks']
    y_labels = ['$xg(x,Q^2\!)$', '$xd_{\mathrm{v}}(x,Q^2\!)$', '$xu_{\mathrm{v}}(x,Q^2\!)$', '$x\Sigma(x,Q^2\!)$',]
    q2s = [1.9, 10000]
    pdfsets = ["HFTD_HERA_V101_EIG", "HFTD_HERACMSTDJETS_V101_EIG"]
    pdf_labels = ["HERA-II DIS", "HERA-II DIS + CMS jets"]
   
    for k, q2 in enumerate(q2s):
        for j, pdfset in enumerate(pdfsets):
            for i, parton in enumerate(partons):
                config = get_base_config()
                config['ana_modules'] = ["PDFModule", 'Ratio']
                config["plot_id"] =  ["pdf_gluon_19", "_pdf_gluon_19_totunc", "_pdf_gluon_19_modexpunc",
                                      'ratio__pdf_gluon_19_modexpunc_to_pdf_gluon_19',
                                      'ratio__pdf_gluon_19_totunc_to_pdf_gluon_19',
                                      'ratio_pdf_gluon_19_to_pdf_gluon_19',
                                     ] 
                config["input_pdfsets"] = [
                        (
                        "pdf_gluon_19", {
                                "flavour": partons[i], 
                                "q2": q2s[k], 
                                "pdfset": pdfset
                                }
                        )
                ]
                config['ratio_copy'] = [
                                        ('_pdf_gluon_19_totunc', 'pdf_gluon_19'),
                                        ('_pdf_gluon_19_modexpunc', 'pdf_gluon_19'),
                                        ('pdf_gluon_19', 'pdf_gluon_19'),
                                        ]
                config['objects']['pdf_gluon_19'] = {
                    "edgealpha": 1.0, 
                    "edgecolor": "auto", 
                    "style": "band", 
                    "rasterized": True, 
                    "capsize": 0, 
                    "x_err": True, 
                    "color": "#C44E52", 
                    "linestyle": "", 
                    "label": "Exp. Uncert", 
                    "step": False, 
                    "cmap": "viridis", 
                    "zorder": 2.5, 
                    "obj": "null", 
                    "plot_datavals": False, 
                    "marker": ".", 
                    "alpha": 1.0, 
                    "fill": True, 
                    "y_err": True, 
                    "id": "nnpdf30", 
                    "axis": "ax"
                } 
                config["objects"]["_pdf_gluon_19_totunc"] = {
                    "edgealpha": 1.0, 
                    "edgecolor": "auto", 
                    "style": "band", 
                    "rasterized": True, 
                    "capsize": 0, 
                    "x_err": True, 
                    "color": "#55A868", 
                    "linestyle": "", 
                    "label": "Par. Uncert", 
                    "step": False, 
                    "cmap": "viridis", 
                    "zorder": 1.0, 
                    "obj": "null", 
                    "plot_datavals": False, 
                    "marker": ".", 
                    "alpha": 1.0, 
                    "fill": True, 
                    "y_err": True, 
                    "id": "_nnpdf30_totunc", 
                    "axis": "ax"
                }
                config['objects']['_pdf_gluon_19_modexpunc'] = {
                    "edgealpha": 1.0, 
                    "edgecolor": "auto", 
                    "style": "band", 
                    "rasterized": True, 
                    "capsize": 0, 
                    "x_err": True, 
                    "color": "Gold", 
                    "linestyle": "", 
                    "label": "Mod. Uncert", 
                    "step": False, 
                    "cmap": "viridis", 
                    "zorder": 2.0, 
                    "obj": "null", 
                    "plot_datavals": False, 
                    "marker": ".", 
                    "alpha": 1.0, 
                    "fill": True, 
                    "y_err": True, 
                    "id": "_nnpdf30_modexpunc", 
                    "axis": "ax"
                }
        
                config["objects"]["ratio__pdf_gluon_19_totunc_to_pdf_gluon_19"] = {
                    "edgealpha": 1.0, 
                    "edgecolor": "auto", 
                    "style": "band", 
                    "rasterized": True, 
                    "capsize": 0, 
                    "x_err": True, 
                    "color": "#55A868", 
                    "linestyle": "", 
                    "step": False, 
                    "cmap": "viridis", 
                    "zorder": 1.0, 
                    "obj": "null", 
                    "plot_datavals": False, 
                    "marker": ".", 
                    "alpha": 1.0, 
                    "fill": True, 
                    "y_err": True, 
                    "id": "_nnpdf30_totunc", 
                    "axis": "ax1"
                }
                config['objects']['ratio__pdf_gluon_19_modexpunc_to_pdf_gluon_19'] = {
                    "edgealpha": 1.0, 
                    "edgecolor": "auto", 
                    "style": "band", 
                    "rasterized": True, 
                    "capsize": 0, 
                    "x_err": True, 
                    "color": "Gold", 
                    "linestyle": "", 
                    "step": False, 
                    "cmap": "viridis", 
                    "zorder": 2.0, 
                    "obj": "null", 
                    "plot_datavals": False, 
                    "marker": ".", 
                    "alpha": 1.0, 
                    "fill": True, 
                    "y_err": True, 
                    "id": "_nnpdf30_modexpunc", 
                    "axis": "ax1"
                }
                config['objects']['ratio_pdf_gluon_19_to_pdf_gluon_19'] = {
                    "edgealpha": 1.0, 
                    "edgecolor": "auto", 
                    "style": "band", 
                    "rasterized": True, 
                    "capsize": 0, 
                    "x_err": True, 
                    "color": "#C44E52", 
                    "linestyle": "", 
                    "step": False, 
                    "cmap": "viridis", 
                    "zorder": 2.0, 
                    "obj": "null", 
                    "plot_datavals": False, 
                    "marker": ".", 
                    "alpha": 1.0, 
                    "fill": True, 
                    "y_err": True, 
                    "id": "nnpdf30", 
                    "axis": "ax1"
                } 

                if parton in ymax_lim and q2 in ymax_lim[parton]:
                    ymaxval = ymax_lim[parton][q2]
                else:
                    ymaxval = 'none'

                config["y_lims"] = ["0.0", ymaxval]
                config["y_subplot_lims"] = ["0.5", "1.5"]
                config["y_subplot_label"] = 'Rel. Uncert.'
                config["x_lims"] = [1E-4, 0.9]
                config['x_axis_formatter'] = 'scientific'
                config["x_log"] =  True
                config["add_subplot"] =  True
                config["legend_loc"] = 'best'
                config["x_label"] = "$x$"
                config["y_label"] = y_labels[i]
                config["ax_texts"] = [
                                      's={0}?_topleft_'.format(pdf_labels[j]),
                                      's=$Q^2\!={0}\mathrm{{GeV}}^2$?_topright_'.format(get_q2label(q2)),
                                      ] 
                config["output_path"] = 'pdfcomp_{0}_{1}_{2}.png'.format(pdfset, partons[i], q2)
                configs.append(config)

    return configs

# @callbacks.register('before_plot')
# def final_plot(**kwargs):
#     kwargs['mpl'].rcParams['legend.fontsize'] = 20
#     # kwargs['mpl'].rcParams['font.size'] = 20
