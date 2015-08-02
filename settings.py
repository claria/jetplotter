import collections
import argparse


class SettingListAction(argparse.Action):
    """Stores a setting list object in the Parser namespace."""
    def __init__(self, list_default=None, *args, **kwargs):
        self.list_default = kwargs.pop('list_default', None)
        super(SettingListAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, SettingList(values, self.list_default))


class SettingList(list):
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
        super(SettingList, self).__init__(setting)

        if len(self) == 0 and self.default in [None, 'last', 'first']:
            raise ValueError('You either have to provide a list with len>0 or a valid default.')

    def __getitem__(self, idx):
        """Return item at idx if in list, else grow list and return default value."""
        if (idx >= len(self)):
            self._grow(idx)
        return super(SettingList, self).__getitem__(idx)

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
        super(SettingList, self).__setitem__(idx, value)

    def _grow(self, idx):
        """Grow list up to idx using default values."""
        self += (idx-(len(self) - 1)) * [self._get_default()]
