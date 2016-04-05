import os

import ROOT

from util.root_tools import get_root_object, get_tgraphasymm_from_histos, get_root_file, build_root_object

import numpy as np

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

from modules.base_module import BaseModule

import logging

log = logging.getLogger('__name__')


class RootModule(BaseModule):
    """ Input module to load histograms and graphs from a root file.

        This modules runs at the beginning to load objects from root files and puts these objects into the config dict.
        Therefore you always have to give the id in which the object will be stored. The --input-graph options has a few
        more options to construct a TGraphAsymmErrors from multiple histograms.
    """

    def __init__(self):
        super(RootModule, self).__init__()
        self.arg_group.add_argument('-i', '--input', nargs='+', type='str2kvstr', action='setting',
                                    help='Path to root file or objects in root files with syntax '
                                         'id:rootfile?path/to/object.')
        self.arg_group.add_argument('--input_tgraph', nargs='+', type='str2kvstr', action='setting',
                                    help='Path to root file or objects in root files with '
                                         'syntax id:rootfile?path/to/object.')

    def __call__(self, config):
        for id, item in config['objects'].iteritems():
            if 'input' in item:
                # just get object
                if not '=' in item['input']:
                    item['obj'] = get_root_object(item['input'])
                else:
                    kwargs = parse_query(item['input'])
                    item['obj'] = build_root_object(**kwargs)
            elif 'input_tgraph' in item:
                if '&' in item['input_tgraph']:
                    item['obj'] = get_tgraphasymm_from_histos(
                        *[get_root_object(input) for input in item['input_tgraph'].split('&')])
                else:
                    item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input_tgraph']))
            elif 'input_asymmerrgraph' in item:
                item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input']))


class RootOutputModule(BaseModule):
    def __init__(self):
        super(RootOutputModule, self).__init__()
        self.arg_group.add_argument('--root-output', default=None, nargs='+', type=str,
                                    help='List of ids, which objects will be written out to a root file.')

    def __call__(self, config):
        if config.get('root-output', []):
            ids = config['root-output']
        else:
            ids = config['objects'].keys()

        if 'root_output_filename' not in config.keys():
            root_output_filename = os.path.splitext(os.path.join(config['output_prefix'], config['output_path']))[0] + '.root'
        else:
            root_output_filename = config['root_output_filename'] 


        if 'root_output_folder' in config.keys():
            root_output_folder = config['root_output_folder']
        else:
            root_output_folder = '/'

        out_file = get_root_file(root_output_filename, "UPDATE")
        out_file.cd('/')

        if ROOT.gDirectory.GetDirectory(root_output_folder) != None:
            print "Folder {0} exists. Will be overwritten".format(root_output_folder)
            ROOT.gDirectory.Delete('{0};*'.format(root_output_folder))

        ROOT.gDirectory.mkdir(root_output_folder)
        ROOT.gDirectory.cd(root_output_folder)

        for id in ids:
            if id not in config['objects']:
                raise ValueError('Id {0} not found within objects. Check your supplied ids.'.format(id))
            if 'obj' in config['objects'][id]:
                log.info('Writing id {0} to file {1}'.format(id, root_output_filename))
                if config['objects'][id]['obj']:
                    config['objects'][id]['obj'].Write(id)
            else:
                log.debug('Omitting id {0} since no root object found.'.format(id))
                continue

        out_file.Close()

class BuildTGraph(BaseModule):
    def __init__(self):
        super(BuildTGraph, self).__init__()
        self.arg_group.add_argument('--build-tgraph', default=[], nargs='+', type='str2kvdict',
                                    help='List of ids, which objects will be written out to a root file.')

    def __call__(self, config):
        if config['build_tgraph']:
            for id, input_ids in config['build_tgraph']:
                if len(input_ids) == 1:
                    # Basically only copies th TGraph
                    new_graph = ROOT.TGraphErrors(config['objects'][input_ids[0]]['obj'])
                elif len(input_ids) == 2:
                    # The both inputs define the minimum maximum and the center is set by the mean of both.
                    tmp_tgraph1 = config['objects'][input_ids[0]]['obj']
                    tmp_tgraph2 = config['objects'][input_ids[1]]['obj']
                    if not (tmp_tgraph1.GetN() == tmp_tgraph2.GetN()):
                        raise ValueError('The both objects must have the same number of points.')
                    new_graph = ROOT.TGraphAsymmErrors(tmp_tgraph1)
                    for i in xrange(new_graph.GetN()):
                        tmp_tgraph1x, tmp_tgraph1y = ROOT.Double(0), ROOT.Double(0)
                        tmp_tgraph1.GetPoint(i, tmp_tgraph1x, tmp_tgraph1y)

                        tmp_tgraph2x, tmp_tgraph2y = ROOT.Double(0), ROOT.Double(0)
                        tmp_tgraph2.GetPoint(i, tmp_tgraph2x, tmp_tgraph2y)

                        center = 0.5 * (tmp_tgraph1y + tmp_tgraph2y)

                        new_graph.SetPoint(i, tmp_tgraph1x, 0.5 * (tmp_tgraph1y + tmp_tgraph2y))
                        new_graph.SetPointEYlow(i, abs(tmp_tgraph1y - tmp_tgraph2y) / 2.)
                        new_graph.SetPointEYhigh(i, abs(tmp_tgraph1y - tmp_tgraph2y) / 2.)

                        new_graph.SetPointEXlow(i, tmp_tgraph1.GetErrorX(i))
                        new_graph.SetPointEXhigh(i, tmp_tgraph1.GetErrorX(i))

                    config['objects'].setdefault(id, {})['obj'] = new_graph
                elif len(input_ids) == 3:
                    if isinstance(config['objects'][input_ids[0]]['obj'], ROOT.TGraph):
                        # The both inputs define the minimum maximum and the center is set by the mean of both.
                        tmp_tgraph1 = config['objects'][input_ids[0]]['obj']
                        tmp_tgraph2 = config['objects'][input_ids[1]]['obj']
                        tmp_tgraph3 = config['objects'][input_ids[2]]['obj']
                        if not (tmp_tgraph1.GetN() == tmp_tgraph2.GetN() == tmp_tgraph3.GetN()):
                            raise ValueError('The input objects must have the same number of points.')

                        new_graph = ROOT.TGraphAsymmErrors(tmp_tgraph1)

                        for i in xrange(tmp_tgraph1.GetN()):
                            tmp_tgraph1x, tmp_tgraph1y = ROOT.Double(0), ROOT.Double(0)
                            tmp_tgraph1.GetPoint(i, tmp_tgraph1x, tmp_tgraph1y)

                            tmp_tgraph2x, tmp_tgraph2y = ROOT.Double(0), ROOT.Double(0)
                            tmp_tgraph2.GetPoint(i, tmp_tgraph2x, tmp_tgraph2y)

                            tmp_tgraph3x, tmp_tgraph3y = ROOT.Double(0), ROOT.Double(0)
                            tmp_tgraph3.GetPoint(i, tmp_tgraph3x, tmp_tgraph3y)

                            new_graph.SetPoint(i, tmp_tgraph1x, tmp_tgraph1y)
                            new_graph.SetPointEYlow(i, tmp_tgraph1y - tmp_tgraph2y)
                            new_graph.SetPointEYhigh(i, tmp_tgraph3y - tmp_tgraph1y)

                            new_graph.SetPointEXlow(i, tmp_tgraph1.GetErrorX(i))
                            new_graph.SetPointEXhigh(i, tmp_tgraph1.GetErrorX(i))

                        config['objects'].setdefault(id, {})['obj'] = new_graph
                    elif isinstance(config['objects'][input_ids[0]]['obj'], ROOT.TH1):
                        print 'blub'
                        obj = get_tgraphasymm_from_histos(config['objects'][input_ids[0]]['obj'],
                                                          config['objects'][input_ids[1]]['obj'],
                                                          config['objects'][input_ids[2]]['obj'])
                        config['objects'].setdefault(id, {})['obj'] = obj


class Envelope(BaseModule):
    def __init__(self):
        super(Envelope, self).__init__()
        self.arg_group.add_argument('--envelope', default=[], nargs='+', type='str2kvdict',
                                    help='List of ids.')

    def __call__(self, config):
        if config['envelope']:
            for id, input_ids in config['envelope']:
                if len(input_ids) == 1:
                    # Basically only copies th TGraph
                    new_graph = ROOT.TGraphAsymmErrors(config['objects'][input_ids[0]]['obj'])
                elif len(input_ids) > 1:

                    objs = [config['objects'][cid]['obj'] for cid in input_ids]

                    if not all(item.GetN() == objs[0].GetN() for item in objs):
                        raise ValueError('All objects must have the same length,')

                    nobs = objs[0].GetN()

                    data = np.zeros((len(objs), nobs)) 

                    for j,obj in enumerate(objs):
                        for i in xrange(nobs):
                            tmp_X, tmp_Y = ROOT.Double(0), ROOT.Double(0)
                            obj.GetPoint(i, tmp_X, tmp_Y)
                            data[j, i] = tmp_Y

                    data_max = np.max(data, axis=0)
                    data_min = np.min(data, axis=0)
                    center = 0.5 * (data_max + data_min) 

                    new_graph = ROOT.TGraphAsymmErrors(objs[0])
                    for i in xrange(nobs):
                       tmp_X, tmp_Y = ROOT.Double(0), ROOT.Double(0)
                       new_graph.GetPoint(i, tmp_X, tmp_Y)
                       new_graph.SetPoint(i, tmp_X, center[i])
                       new_graph.SetPointEYlow(i, center[i] - data_min[i])
                       new_graph.SetPointEYhigh(i, data_max[i] - center[i])

                    config['objects'].setdefault(id, {})['obj'] = new_graph

