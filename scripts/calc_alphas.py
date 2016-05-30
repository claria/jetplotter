#! /usr/bin/env python

import numpy as np

alphas = 0.11938

exp_unc = [0.001482, 0.0015118]

mod_vars = [0.11962, 0.11931, 0.11934, 0.11946, 0.11921, 0.11953, 0.11925, 0.11956]
print 'mod_vars', [alphas - var for var in mod_vars]

par_vars = [0.11907, 0.11960, 0.11901, 0.11938, 0.11939, 0.11946, 0.11938, 0.11938]

scale_vars = [0.11775, 0.11847, 0.11840, 0.11938, 0.12022, 0.12076, 0.12203]

mod_unc = [0.0, 0.0]
for var in mod_vars:
    mod_unc[0] += np.square(np.minimum(var-alphas, 0.0))
    mod_unc[1] += np.square(np.maximum(var-alphas, 0.0))


mod_unc = [np.sqrt(mod_unc[0]), np.sqrt(mod_unc[0])]

scale_unc = [alphas - np.min(scale_vars), np.max(scale_vars) - alphas] 
par_unc = [alphas - np.min(par_vars), np.max(par_vars) - alphas] 

print 'alphas={0}'.format(alphas)
print 'exp=-{0:.4f} +{1:.4f}'.format(exp_unc[0], exp_unc[1])
print 'mod=-{0:.4f} +{1:.4f}'.format(mod_unc[0], mod_unc[1])
print 'par=-{0:.4f} +{1:.4f}'.format(par_unc[0], par_unc[1])
print 'scale=-{0:.4f} +{1:.4f}'.format(scale_unc[0], scale_unc[1])

