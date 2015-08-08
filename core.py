import argparse
import copy
import os
import sys
import json
import collections


class UserParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(UserParser, self).__init__(*args, **kwargs)
        self.register('type','bool', str2bool)
        self.register('type','str2kvfloat', str2kvfloat)
        self.register('type','str2kvint', str2kvint)
        self.register('type','str2kvbool', str2kvbool)
        self.register('type','str2kvstr', str2kvstr)

        self.register('action','setting', SettingAction)

    def parse_args(self, *args, **kwargs):
        args = super(UserParser, self).parse_args()
        for a in self._actions:
            # this is true if setting has not provided on commandline
            if hasattr(args, a.dest) and (getattr(args, a.dest) == a.default or 
                                          getattr(args, a.dest) == self._registry_get('type', a.type, a.type)(a.default)):

                if isinstance(a, SettingAction):
                    a(self, args, a.default, a.option_strings)
                    delattr(args, a.dest)
            else:
                # these args were actually provided on cmd line.
                if not hasattr(args, 'provided_args'):
                    setattr(args, 'provided_args', [])
                args.provided_args.append(a.dest)
        return args



def str2bool(s):
    """ Parse string content to bool."""
    if isinstance(s, bool):
        return s
    else:
        return s.lower() in ("yes", "true", "t", "1")

def str2kvfloat(s):
    k, v = get_tuple(s)
    return k, float(v)

def str2kvint(s):
    id, setting = get_tuple(s)
    return id, int(setting)

def str2kvbool(s):
    id, setting = get_tuple(s)
    b = setting.lower() in ("yes", "true", "t", "1")
    return id, b

def str2kvstr(s):
    return get_tuple(s)

def get_tuple(s):
    """Try to split s into key value pair at ':' delimiter. Set key to None if ':' not in s."""
    try:
        (id, setting) = s.split(':')
    except ValueError:
        (id, setting) = None, s
    return id, setting

def update_with_default(data):
    for id, item in data.iteritems():
        if id == '_default':
            continue
        data[id] = dict(data['_default'].items() + item.items())

class SettingAction(argparse.Action):
    """Stores a setting list object in the Parser namespace."""
    def __init__(self, list_default=None, *args, **kwargs):
        super(SettingAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            values = []
        if isinstance(values, basestring) or not isinstance(values, collections.Iterable):
            values = [values]

        if not hasattr(namespace, 'settings'):
            setattr(namespace, 'settings', {})
        # Ensure all values are list of tuples (id, val)
        for i in xrange(0, len(values)):
            if not isinstance(values[i], tuple):
                values[i] = (None, values[i])
            if values[i][0] is None:
                # values[i] = ('id_{0}'.format(i), values[i][1])
                values[i] = ('_default'.format(i), values[i][1])
        for id, val in values:
            if not id in namespace.settings:
                namespace.settings[id] = {}
                namespace.settings[id]['id'] = id
            namespace.settings[id][self.dest] = val
        # setattr(namespace, self.dest, SettingDict(values))


class DefaultDict(dict):

    def __init__(self, *args, **kwargs ):
        self.defaults = dict()
        self.update(*args, **kwargs)

    def setdefault(self, key, val):
        self.defaults[key] = val

    def __getitem__(self, key):
        if not key in self and key in self.defaults:
            return self.defaults[key]
        else:
            return dict.__getitem__(self, key)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)



class AutoGrowListAction(argparse.Action):
    """Stores a setting list object in the Parser namespace."""
    def __init__(self, list_default=None, *args, **kwargs):
        self.list_default = kwargs.pop('list_default', None)
        super(AutoGrowListAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, AutoGrowList(values, self.list_default))


class AutoGrowList(list):
    """Contains list of settings values.

       Returns item of idx in list if available, otherwise returns default
       value. Currently default value is just last accessible item in list.
       If item is set outside range of list, list is automatically extended
       to that idx filling the items inbetween with default values.
    """

    def __init__(self, setting, default=None):
        if default:
            self.default = default
        else:
            self.default = 'last'

        if isinstance(setting, basestring) or not isinstance(setting, collections.Iterable):
            setting = [setting]
        super(AutoGrowList, self).__init__(setting)

        if len(self) == 0 and self.default in [None, 'last', 'first']:
            raise ValueError('You either have to provide a list with len>0 or a valid default.')

    def __getitem__(self, idx):
        """Return item at idx if in list, else grow list and return default value."""
        if (idx >= len(self)):
            self._grow(idx)
        return super(AutoGrowList, self).__getitem__(idx)

    def _get_default(self):
        """Return default value. For now, default is just last accessible value in list."""
        if self.default == 'last':
            return self[-1]
        elif self.default == 'first':
            return self[0]
        elif self.default:
            return self.default
        else:
            raise ValueError('No default value provided. Thats not good.')

    def __setitem__(self, idx, value):
        """Set item if idx in list, else increase list up to idx."""
        if idx >= len(self):
            # Extend list up to idx with default vals.
            self._grow(idx)
        super(AutoGrowList, self).__setitem__(idx, value)

    def _grow(self, idx):
        """Grow list up to idx using default values."""
        self.extend((idx - len(self) + 1) * [self._get_default()])


def save_config(config, path, indent=4):
    """Save json config to file."""
    # Remove non serializiable objects from dict.
    out_config = copy.deepcopy(config)

    for id in out_config['settings'].keys():
        if 'obj' in out_config['settings'][id]:
            out_config['settings'][id].pop('obj')

    # Check that output directory exists
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    # Write config.
    with open(path, "w") as f:
        json.dump(out_config, f, skipkeys=True, indent=indent, sort_keys=True)

    # log.debug("Config written to \"{0}\"".format(path))
    print "Config written to \"{0}\"".format(path)
    return path

def read_config(path):
    with open(path) as json_file:
        try:
            config = json.load(json_file)
        except ValueError:
            # log.critical('Failed to parse json file {0}'.format(config_name))
            print 'Failed to parse json file {0}'.format(path)
            sys.exit(1)
    return config

def update_dict(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update_dict(d.get(k, {}), v)
            d[k] = r
        else:
            if 'provided_args' in u.keys() and k in u['provided_args']:
                d[k] = u[k]
            else:
                d[k] = u[k]
    return d

def print_config(config):
    print json.dumps(config, sort_keys=True, indent=4)

def walk_json():
    pass
