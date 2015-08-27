"""
Dictionary containing lookup values which will be replaced in the 
settings.
"""
lookup_dict = {
    'x_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ (GeV)',
        '_pt_': '$p_{\mathrm{T}}$ (GeV)',
        '_y_boost_': '$y_b$',
        '_right_': '{"position" : [1.0,0.0], "va" : "top", "ha" : "right"}',
        '_center_': '{"position" : [0.5,0.0], "va" : "top", "ha" : "center"}'
    },
    'y_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ (GeV)',
        '_y_star_': '$y^*$',
        '_top_': '{"position" : [0.0,1.0], "va" : "top", "ha" : "right"}',
        '_center_': '{"position" : [0.0,0.5], "va" : "center", "ha" : "right"}'

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
        '_cms_': 'CMS?{"x": 0.0, "y":1.01, "va": "bottom", "ha" : "left"}',
        '_cmsp_': 'CMS Preliminary?{"x": 0.0, "y":1.01, "va": "bottom", "ha" : "left"}',
        '_20fb_': '$19.7\\,\mathrm{fb}^{-1}$ (8TeV)?{"x": 1.0, "y":1.01, "va": "bottom", "ha" : "right"}',
        '_8tev_': '$\sqrt{s}$ = (8TeV)?{"x": 1.0, "y":1.01, "va": "bottom", "ha" : "right"}',
        '_yb0ys0_': '$0.0 \leq y_b < 1.0$  $0.0 \leq y^* < 1.0$',
        '_yb1ys0_': '$1.0 \leq y_b < 2.0$  $0.0 \leq y^* < 1.0$',
        '_yb2ys0_': '$2.0 \leq y_b < 3.0$  $0.0 \leq y^* < 1.0$',
        '_yb0ys1_': '$0.0 \leq y_b < 1.0$  $1.0 \leq y^* < 2.0$',
        '_yb0ys2_': '$0.0 \leq y_b < 1.0$  $2.0 \leq y^* < 3.0$',
        '_yb1ys1_': '$1.0 \leq y_b < 2.0$  $1.0 \leq y^* < 2.0$',
        '_yb0ys0auto_': '$0.0 \leq y_b < 1.0$  $0.0 \leq y^* < 1.0$?0.03,0.85',
        '_topleft_': '{"x": 0.0, "y":1.01, "va": "bottom", "ha" : "left"}',
        '_topright_': '{"x": 1.0, "y":1.01, "va": "bottom", "ha" : "right"}',
        '_upperleft_': '{"x": 0.05, "y":0.95, "va": "top", "ha" : "left"}',
        '_upperright_': '{"x": 0.95, "y":0.95, "va": "top", "ha" : "right"}',
        '_bottomleft_': '{"x": 0.05, "y":0.05, "va": "bottom", "ha" : "left"}',
        '_bottomright_': '{"x": 0.95, "y":0.05, "va": "bottom", "ha" : "right"}',

    }

}


def get_lookup_val(key, s):
    """ Replaces all occurences of lookup keys in string with lookups."""
    if key in lookup_dict:
        for lk, lv in lookup_dict[key].iteritems():
            if lk in s:
                s = s.replace(lk, lv)
    return s
