# -*- coding: utf-8 -*-

import numpy as np

import ROOT


class MplObject1D(object):
    """Python representation of 1d root objects to be used for matplotlib plotting."""

    def __init__(self, root_object):

        # lists of ROOT classes which can be converted
        histos_1d = ['TH1D', 'TH1F', 'TProfile']
        self.name = root_object.GetName()
        self.root_object = root_object
        self.title = root_object.GetTitle()
        self.xlabel = root_object.GetXaxis().GetTitle()
        self.ylabel = root_object.GetYaxis().GetTitle()

        if root_object.ClassName() in histos_1d:
            # labeled bins
            self.xlabels = np.array(
                [root_object.GetXaxis().GetBinLabel(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # if GetBinLabel is empty, the returned strings have length 0.
            # Sum of Zeroes is 0, so set self.xlabels to None
            self.xlabels = self.xlabels if (sum(np.array([len(i) for i in self.xlabels]))) else None

            # bin center
            self.x = np.array([root_object.GetXaxis().GetBinCenter(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # lower bin edge
            self.xl = np.array(
                [root_object.GetXaxis().GetBinLowEdge(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # upper bin edge
            self.xu = np.array([root_object.GetXaxis().GetBinUpEdge(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            self.xerr = self.x - self.xl
            # bin content
            self.y = np.array([root_object.GetBinContent(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # bin content
            self.yerr = np.array([root_object.GetBinError(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # lower bin error
            self.yerrl = np.array([root_object.GetBinErrorLow(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # upper bin error
            self.yerru = np.array([root_object.GetBinErrorUp(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
        elif isinstance(root_object, ROOT.TGraph):
            self.x = np.zeros((root_object.GetN()))
            self.y = np.zeros((root_object.GetN()))
            for i in xrange(root_object.GetN()):
                tmpx, tmpy = ROOT.Double(0), ROOT.Double(0)
                root_object.GetPoint(i, tmpx, tmpy)
                self.x[i] = tmpx
                self.y[i] = tmpy
            self.xerr = np.array([root_object.GetErrorX(i) for i in xrange(root_object.GetN())])
            self.xl = np.array([self.x[i] - root_object.GetErrorXlow(i) for i in xrange(root_object.GetN())])
            self.xu = np.array([self.x[i] + root_object.GetErrorXhigh(i) for i in xrange(root_object.GetN())])
            self.yerr = np.array([root_object.GetErrorY(i) for i in xrange(root_object.GetN())])
            # map yerr < 0 to zero
            self.yerr[self.yerr < 0.] = 0.
            self.yerrl = np.array([root_object.GetErrorYlow(i) for i in xrange(root_object.GetN())])
            self.yerrl[self.yerrl < 0.] = 0.
            self.yerru = np.array([root_object.GetErrorYhigh(i) for i in xrange(root_object.GetN())])
            self.yerru[self.yerru < 0.] = 0.
        elif isinstance(root_object, ROOT.TF1):
            raise NotImplementedError
        else:
            raise TypeError(str(root_object.ClassName()) + ' cannot be converted to an MPLObject1d.')

    @property
    def xerrl(self):
        return self.x - self.xl

    @property
    def xerru(self):
        return self.xu - self.x

    @property
    def xbinwidth(self):
        return self.xu - self.xl

    @property
    def xbinedges(self):
        return np.concatenate((self.xl, self.xu[-1:]))

    @property
    def ybinwidth(self):
        return self.yu - self.yl

    @property
    def ybinedges(self):
        return np.concatenate((self.yl, self.yu[-1:]))

    @property
    def yl(self):
        return self.y - self.yerrl

    @property
    def yu(self):
        return self.y + self.yerru


class MplObject2D(object):
    """Python representation of 2d root objects to be used for matplotlib plotting."""

    def __init__(self, root_object):

        # lists of ROOT classes which can be converted
        histos_2d = ['TH2D', 'TH2F', 'TProfile2D']
        self.name = root_object.GetName()
        self.root_object = root_object
        self.title = root_object.GetTitle()
        self.xlabel = root_object.GetXaxis().GetTitle()
        self.ylabel = root_object.GetYaxis().GetTitle()

        if root_object.ClassName() in histos_2d:
            # bin center
            self.x = np.array([root_object.GetXaxis().GetBinCenter(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # lower bin edge
            self.xl = np.array(
                [root_object.GetXaxis().GetBinLowEdge(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            # upper bin edge
            self.xu = np.array([root_object.GetXaxis().GetBinUpEdge(i) for i in xrange(1, root_object.GetNbinsX() + 1)])
            self.xerr = self.x - self.xl

            self.y = np.array([root_object.GetYaxis().GetBinCenter(i) for i in xrange(1, root_object.GetNbinsY() + 1)])
            # lower bin edge
            self.yl = np.array(
                [root_object.GetYaxis().GetBinLowEdge(i) for i in xrange(1, root_object.GetNbinsY() + 1)])
            # upper bin edge
            self.yu = np.array([root_object.GetYaxis().GetBinUpEdge(i) for i in xrange(1, root_object.GetNbinsY() + 1)])
            self.yerr = self.y - self.yl

            self.z = np.zeros((root_object.GetNbinsY(), root_object.GetNbinsX()))
            self.zl = np.zeros((root_object.GetNbinsY(), root_object.GetNbinsX()))
            self.zu = np.zeros((root_object.GetNbinsY(), root_object.GetNbinsX()))
            for x in xrange(1, root_object.GetNbinsX() + 1):
                for y in xrange(1, root_object.GetNbinsY() + 1):
                    self.z[y - 1, x - 1] = root_object.GetBinContent(x, y)
                    self.zl[y - 1, x - 1] = root_object.GetBinContent(x, y) - root_object.GetBinErrorLow(x, y)
                    self.zu[y - 1, x - 1] = root_object.GetBinContent(x, y) + root_object.GetBinErrorUp(x, y)
            self.zerr = self.z - self.zl
        else:
            raise TypeError(str(root_object.ClassName()) + ' cannot be converted to an MPLObject1d.')

    @property
    def xerrl(self):
        return self.x - self.xl

    @property
    def xerru(self):
        return self.xu - self.x

    @property
    def xbinwidth(self):
        return self.xu - self.xl

    @property
    def xbinedges(self):
        return np.concatenate((self.xl, self.xu[-1:]))

    @property
    def ybinwidth(self):
        return self.yu - self.yl

    @property
    def yerrl(self):
        return self.y - self.xl

    @property
    def yerru(self):
        return self.yu - self.y

    @property
    def ybinedges(self):
        return np.concatenate((self.yl, self.yu[-1:]))

    @property
    def zbinwidth(self):
        return self.zu - self.zl

    @property
    def zbinedges(self):
        return np.concatenate((self.zl, self.zu[-1:]))

    @property
    def zerrl(self):
        return self.z - self.zl

    @property
    def zerru(self):
        return self.zu - self.z
