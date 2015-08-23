from abc import ABCMeta, abstractmethod
import inspect

from util.setting_parser import SettingParser


class BaseModule(object):
    """Base Module all different modules have to be derived from.

       Please only use absolute imports (not relative ones like import ..module,
       since the module loader cannot handle this.
    """
    __metaclass__ = ABCMeta

    @classmethod
    def label(cls):
        return cls.__name__

    def __init__(self):
        self.parser = SettingParser(add_help=False)
        self.arg_group = self.parser.add_argument_group(title=self.label(), description=inspect.getdoc(self))

    @abstractmethod
    def __call__(self, **args):
        """This method needs to be overloaded and will be called for all modules."""
        raise NotImplementedError()
