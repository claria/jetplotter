import argparse


class UserParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(UserParser, self).__init__(*args, **kwargs)
        self.register('type','bool', str2bool)
        self.register('type','str2kvfloat', str2kvfloat)
        self.register('type','str2kvint', str2kvint)
        self.register('type','str2kvbool', str2kvbool)
        self.register('type','str2kvstr', str2kvstr)

        self.register('action','setting', SettingAction)


def str2bool(s):
    """ Parse string content to bool."""
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

class SettingAction(argparse.Action):
    """Stores a setting list object in the Parser namespace."""
    def __init__(self, list_default=None, *args, **kwargs):
        super(SettingAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, SettingDict(values))


class SettingDict(dict):

    def __init__(self, *args, **kwargs ):
        self.default = kwargs.pop('default', None)
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        return self.default

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def update(self, *args, **kwargs):
        print args
        print kwargs
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v


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
