#!/usr/bin/env python2
import os
import sys
import numpy as np
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.root_tools import get_np_object, get_root_object
from util.root2np import R2npObject1D


def main():
    pass
    ybys_bins = ['yb0ys0', 'yb0ys1', 'yb0ys2', 'yb1ys0', 'yb1ys1', 'yb2ys0']

    for i, ybys_bin in enumerate(ybys_bins):
        # unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO_WITHFAKES.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root.Scale(1.0, 'width')
        unf_data = R2npObject1D(unf_data_root)

        data = collections.OrderedDict()
        data['yb_low'] = np.array([float(ybys_bin[2])] * len(unf_data.xl))
        data['yb_high'] = np.array([float(ybys_bin[2]) + 1.0] * len(unf_data.xl))
        data['ys_low'] = np.array([float(ybys_bin[5])] * len(unf_data.xl))
        data['ys_high'] = np.array([float(ybys_bin[5]) + 1.0] * len(unf_data.xl))

        data['pt_low'] = unf_data.xerrl
        data['pt'] = unf_data.x
        data['pt_high'] = unf_data.xerru

        # print unf_data.x
        # print unf_data.xerrl
        # print unf_data.xl

        data['sigma'] = unf_data.y
        data['stat_l'] = unf_data.yerrl
        data['stat_h'] = unf_data.yerrl


        print "# BEGIN YODA_SCATTER2D /REF/CMS_2015_DIJET/d0{0}-x01-y01".format(i+1)
        print "Path=/REF/CMS_2015_DIJET/d0{0}-x01-y01".format(i+1)
        print "Type=Scatter2D"
        print "# xval	 xerr-	 xerr+	 yval	 yerr-	 yerr+"

        print_data(data, ybys_bin=ybys_bin)

        print "# END YODA_SCATTER2D"
        print

def infinalrange(pt_low, ybys_bin):
    cuts = {
            'yb0ys0' : (133.,1784.),
            'yb0ys1' : (133.,1248.),
            'yb0ys2' : (133.,548.),
            'yb1ys0' : (133.,1032.),
            'yb1ys1' : (133.,686),
            'yb2ys0' : (133.,430.),
            }
    if pt_low >= cuts[ybys_bin][0] and pt_low < cuts[ybys_bin][1]:
        return True
    return False

def print_data(data, ybys_bin):
    # labels = data.keys()
    # labels.sort()
    nbins = len(data['sigma'])
    for i in xrange(nbins):
        if infinalrange(data['pt'][i], ybys_bin):
            out_data = [data['pt'], data['pt_low'], data['pt_high'],data['sigma'], data['stat_l'], data['stat_h']]
            vals = ['{0:<15.5g}'.format(value[i]) for value in out_data]
            print ' '.join(vals)

# unfolded data
# stat unc
# correlations
# jec
# systematic unfolding

if __name__ == '__main__':
    main()
