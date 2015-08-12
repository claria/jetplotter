import argparse
import collections
import json


class UserParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(UserParser, self).__init__(*args, **kwargs)
        self.register('type', 'bool', str2bool)
        self.register('type', 'str2kvfloat', str2kvfloat)
        self.register('type', 'str2kvint', str2kvint)
        self.register('type', 'str2kvbool', str2kvbool)
        self.register('type', 'str2kvstr', str2kvstr)
        self.register('type', 'str2kvdict', str2kvdict)
        self.register('type', 'noneorfloat', noneorfloat)

        self.register('action', 'setting', SettingAction)

    def parse_args(self, *args, **kwargs):
        args = super(UserParser, self).parse_args()
        for a in self._actions:
            # this is true if setting has not provided on commandline
            # in case a setting has not been provided on the commandline,
            # argparse just calls setattr(args, a.dest, a.default) without calling any action.
            # Only if the type of a.default is a string, the type function is called.
            is_default_arg = False
            if hasattr(args, a.dest):
                if isinstance(a.default, basestring) and getattr(args, a.dest) == self._registry_get('type', a.type,
                                                                                                     a.type)(a.default):
                    is_default_arg = True
                elif getattr(args, a.dest) == a.default:
                    is_default_arg = True

            if is_default_arg:
                if isinstance(a, SettingAction):
                    a(self, args, a.default, a.option_strings)
                    # delattr(args, a.dest)
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

def noneorfloat(v):
    """Return float if parseable, else None."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

def str2kvfloat(s):
    k, v = get_tuple(s)
    return k, float(v)

def str2kvdict(s):
    k, v = get_tuple(s)
    return k, json.loads(v)


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
        (id, setting) = s.split(':', 1)
    except ValueError:
        (id, setting) = None, s
    return id, setting


class SettingAction(argparse.Action):
    """Stores a setting list object in the Parser namespace."""

    def __init__(self, *args, **kwargs):
        super(SettingAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if values is None:
            values = []
        if isinstance(values, basestring) or not isinstance(values, collections.Iterable):
            values = [values]

        if not hasattr(namespace, 'objects'):
            setattr(namespace, 'objects', {})
        if hasattr(namespace, self.dest):
            delattr(namespace, self.dest)
        # Ensure all values are list of tuples (id, val)
        for i in xrange(0, len(values)):
            if not isinstance(values[i], tuple):
                values[i] = (None, values[i])
            if values[i][0] is None:
                # values[i] = ('id_{0}'.format(i), values[i][1])
                values[i] = ('_default'.format(i), values[i][1])
        for id, val in values:
            if id not in namespace.objects:
                namespace.objects[id] = {}
                namespace.objects[id]['id'] = id
            namespace.objects[id][self.dest] = val


class AutoGrowListAction(argparse.Action):
    """Stores a setting list object in the Parser namespace."""

    def __init__(self, list_default=None, *args, **kwargs):
        self.list_default = list_default
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
        if idx >= len(self):
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
