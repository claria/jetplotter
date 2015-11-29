#!/usr/bin/env python2
import os
import sys
import numpy as np
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.root_tools import get_np_object, get_root_object
from util.root2np import R2npObject1D, R2npObject2D 


def main():

    ybys_bins = ['yb0ys0', 'yb0ys1', 'yb0ys2', 'yb1ys0', 'yb1ys1', 'yb2ys0']
    ncorr = 0
    for i, ybys_bin in enumerate(ybys_bins):
        # unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root_corr = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/corr_h_ptavg'.format(ybys_bin))
        unf_data_corr = R2npObject2D(unf_data_root_corr)
        unf_data = R2npObject1D(unf_data_root)

        for xi, x in enumerate(unf_data_corr.xerrl):
            for yi, y in enumerate(unf_data_corr.yerrl):
                # print i, unf_data.xerrl[xi], unf_data.xerrl[yi], unf_data_corr.z[xi, yi]
                if infinalrange(unf_data.xl[yi], ybys_bin) and infinalrange(unf_data.xl[xi], ybys_bin):
                    corr = unf_data_corr.z[xi, yi]
                    if abs(corr) < 0.02:
                        corr = 0.0
                    print i, unf_data.xl[xi],i,  unf_data.xl[yi], '{0:.2f}'.format(corr)
                    ncorr += 1

    print 'NCorr = {0}'.format(ncorr)
        # print_data(data, labels=labels, ybys_bin=ybys_bin)



def infinalrange(pt_low, ybys_bin):
    cuts = {
            'yb0ys0' : (74.,1784.),
            'yb0ys1' : (74.,1248.),
            'yb0ys2' : (74.,548.),
            'yb1ys0' : (74.,1032.),
            'yb1ys1' : (74.,686),
            'yb2ys0' : (74.,430.),
            }
    if pt_low >= cuts[ybys_bin][0] and pt_low < cuts[ybys_bin][1]:
        return True
    return False

if __name__ == '__main__':
    main()
