import argparse
import collections
import json
import sys
import re

import logging

log = logging.getLogger(__name__)


class SettingParser(argparse.ArgumentParser):
    """ Argparser with additional features for key/value based options.

        The main feature are str2kv types which are given as id:value and are
        all stored in a dict so different settings are automatically matched
        to the same id.

        Additionally the arg_group ensures that the actions are always called for the
        'setting' action, not only if the argument is supplied.
        Additionally a list 'provided_args' keeps a list of all args which were actually
        supplied on the command line.
    """

    def __init__(self, *args, **kwargs):
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = argparse.ArgumentDefaultsHelpFormatter
        super(SettingParser, self).__init__(*args, **kwargs)
        self.register('type', 'bool', str2bool)
        self.register('type', 'str2kvfloat', str2kvfloat)
        self.register('type', 'str2kvint', str2kvint)
        self.register('type', 'str2kvbool', str2kvbool)
        self.register('type', 'str2kvstr', str2kvstr)
        self.register('type', 'str2kvdict', str2kvdict)
        self.register('type', 'str2dict', str2dict)
        self.register('type', 'noneorfloat', noneorfloat)

        self.register('action', 'setting', SettingAction)

    def parse_args(self, *args, **kwargs):
        """ Parses args and ensures that all 'setting' actions are called.

            Argparser only calls action for non-default arguments. To ensure that all argument actions are called,
            all actions are called again.
        """
        args = super(SettingParser, self).parse_args()
        # Put also cmd call in args
        setattr(args, 'argv', ' '.join(['\'{0}\''.format(item) if ' ' in item else '{0}'.format(item) for item in sys.argv ]))
        for a in self._actions:
            # is_default_arg is true if setting has not provided on commandline
            # in case a setting has not been provided on the commandline,
            # argparse just calls setattr(args, a.dest, a.default) without calling any action.
            # Only if the type of a.default is not a string, the type function is called.
            is_default_arg = False
            if hasattr(args, a.dest):
                if isinstance(a.default, basestring) and \
                                getattr(args, a.dest) == self._registry_get('type', a.type, a.type)(a.default):
                    is_default_arg = True
                elif getattr(args, a.dest) == a.default:
                    is_default_arg = True

            if is_default_arg:
                if isinstance(a, SettingAction):
                    a(self, args, a.default, a.option_strings)
            else:
                # these args were actually provided on cmd line.
                # TODO: does not work if provided arg is actually a default
                if not hasattr(args, 'provided_args'):
                    setattr(args, 'provided_args', [])
                # but still we want to set the _default value in the dict if they are a SettingAction
                # we need this if we want to pass an arg for some of the ids but take the default for the rest
                if isinstance(a, SettingAction):
                    a(self, args, a.default, a.option_strings)
            # Identify actually provided args using sys.argv[1:]
            if any([arg.startswith(option) for arg in sys.argv[1:] for option in a.option_strings]):
                args.provided_args.append(a.dest)
        return args


def str2bool(s):
    """ Parse string content to bool."""
    if isinstance(s, bool):
        return s
    else:
        return s.lower() in ("yes", "true", "t", "1")


def noneorfloat(v):
    """ Return float if parseable, else None."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def str2kvfloat(s):
    """ Parses string of format id:value into tuple of (str, float)."""
    k, v = get_tuple(s)
    return k, float(v)


def str2kvdict(s):
    """ Parses string of format id:value into tuple of (str, dict)

        The passed value must be json parseable, eg something like
        id:{"key0": "val0", "key1": "val1"}
    """
    k, v = get_tuple(s)
    try:
        d = json.loads(v, object_pairs_hook=collections.OrderedDict)
    except ValueError:
        d = parse_query(v)

    return k, d

def str2kvquery(s):
    """ Parses string of format id:value into tuple of (str, dict)

        The passed value must be json parseable, eg something like
        id:{"key0": "val0", "key1": "val1"}
    """
    k, query = get_tuple(s)
    kwargs = parse_query(query)
    return k, kwargs


def str2dict(s):
    """ Parses string of format id:value into tuple of (str, dict)

        The passed value must be json parseable, eg something like
        {"key0": "val0", "key1": "val1"}
    """
    try:
        return json.loads(s, object_pairs_hook=collections.OrderedDict)
    except ValueError:
        return parse_query(s)


def str2kvint(s):
    """Parses string of format id:value into tuple of (str, int)"""
    id, setting = get_tuple(s)
    return id, int(setting)


def str2kvbool(s):
    """ Parses string of format id:value into tuple of (str, bool)."""
    id, setting = get_tuple(s)
    b = setting.lower() in ("yes", "true", "t", "1")
    return id, b


def str2kvstr(s):
    """ Parses string of format id:value into tuple of (str, str)."""
    return get_tuple(s)

def get_tuple(s):
    """ Try to split s into key value pair at ':' delimiter. Set key to None if ':' not in s."""
    try:
        (id, setting) = s.split(':', 1)
    except ValueError:
        (id, setting) = None, s
    return id, setting

def parse_query(query_str):

    if isinstance(query_str, dict):
        return query_str

    d = {}
    for item in re.split('[?|]+',  query_str):

        k, v = item.split('=', 1)
        try:
            d[k] = json.loads(v, object_pairs_hook=collections.OrderedDict)
        except ValueError as e:
            d[k] = json.loads('"{0}"'.format(escape(v)), object_pairs_hook=collections.OrderedDict)
    return d

def escape(inp_str):
    """
    Return string with escaped latex incompatible characters.
    :param inp_str:
    :return:
    """
    chars = {
        '\\': '\\\\',
        '\n': '\\n',
    }
    return ''.join([chars.get(char, char) for char in inp_str])


class SettingAction(argparse.Action):
    """ Stores a setting list object in the Parser namespace.

        All SettingAction argument values must have the structure --argument id_0:value_0 id_1:value_1.
        These are stored in a OrderedDict 'objects' with the structure
            objects['id_0']['argument'] = value_0
            objects['id_1']['argument'] = value_1

        In case the passed values is a string (currently only possible for default values) the id _default is used.
        Later in the code, setting lookups which fail, fall_back to the _default dict.
    """

    def __init__(self, *args, **kwargs):
        super(SettingAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        if values is None:
            values = []

        # In case the passed values are not a list-like object
        # we assume they originate from the argparse default values.
        # We then set the id to \'_default\'
        if isinstance(values, basestring) or not isinstance(values, collections.Iterable):
            values = [('_default', values)]

        # Ensure that namespace has the objects OrderedDict
        if not hasattr(namespace, 'objects'):
            setattr(namespace, 'objects', collections.OrderedDict())

        # Argparse does not call the action for default arguments. The SettingsParser ensures that all
        # setting action are called, but there is still the possibility that argparse used setattr to store the arg
        # in the namespace. Just make sure it isn't there.
        if hasattr(namespace, self.dest):
            delattr(namespace, self.dest)

        # All arguments should have been parsed to a tuple of (id, value). If no id is provided or if the id is None
        # we fallback to the '_default' id. This is used to provide default args directly.
        # But each id still has to be unique.
        for i in xrange(len(values)):
            if not isinstance(values[i], tuple) or len(values[i]) != 2:
                # Make it to a tuple
                values[i] = (None, values[i])
            if not values[i][0] or not isinstance(values[i][0], basestring):
                # values[i] = ('_default', values[i][1])
                raise ValueError('One of the supplied argument for --{1} '
                                 'is not of the format id:value.'.format(values[i], self.dest), )
        # Check if all ids for one setting are unique.
        if values:
            id_list = zip(*values)[0]
            if len(id_list) > len(set(id_list)):
                raise ValueError('The ids of the argument {0} are not unique. Ids : {1}'.format(self.dest, id_list))
        # All checks are done.
        # Store all (id, val) pairs in the objects dictionary
        for id, val in values:
            namespace.objects.setdefault(id, {})
            namespace.objects[id][self.dest] = val
