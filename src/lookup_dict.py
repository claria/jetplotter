"""
Dictionary containing lookup values which will be replaced in the 
settings.
"""
lookup_dict = {
    'x_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ (GeV)',
        '_pt_': '$p_{\mathrm{T}}$ (GeV)',
        '_y_boost_': '$y_b$'
    },
    'y_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ (GeV)',
        '_y_star_': '$y_s$'
    },
    'label': {
        '_yb0ys0_': '$0.0 \leq y_b < 1.0$  $0.0 \leq y^* < 1.0$',
        '_yb1ys0_': '$1.0 \leq y_b < 2.0$  $0.0 \leq y^* < 1.0$',
        '_yb2ys0_': '$2.0 \leq y_b < 3.0$  $0.0 \leq y^* < 1.0$',
        '_yb0ys1_': '$0.0 \leq y_b < 1.0$  $1.0 \leq y^* < 2.0$',
        '_yb0ys2_': '$0.0 \leq y_b < 1.0$  $2.0 \leq y^* < 3.0$',
        '_yb1ys1_': '$1.0 \leq y_b < 2.0$  $1.0 \leq y^* < 2.0$',
    },
    'color': {
        '_color0_': '#4C72B0',
        '_color1_': '#55A868',
        '_color2_': '#C44E52',
        '_color3_': '#8172B2',
        '_color4_': '#CCB974',
        '_color5_': '#64B5CD'
    },
    'ax_texts': {
        '_cms_': 'CMS?top left',
        '_cmsp_': 'CMS Preliminary?top left',
        '_20fb_': '$20\\,\mathrm{fb}^{-1}$ (8TeV)?top right',
        '_yb0ys0_': '$0.0 \leq y_b < 1.0$  $0.0 \leq y^* < 1.0$?0.03,0.85',
    }

}
