from abc import ABCMeta, abstractmethod
import inspect

from util.setting_parser import SettingParser


class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class BaseModule(object):
    """Base Module all different modules have to be derived from.

       Please only use absolute imports (not relative ones like import ..module,
       since the module loader cannot handle this.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ Set up parser and argument group for module."""
        self.parser = SettingParser(add_help=False)
        self.arg_group = self.parser.add_argument_group(title=self.label, description=inspect.getdoc(self))

    @ClassProperty
    @classmethod
    def label(cls):
        """ Label of the module."""
        return cls.__name__

    @abstractmethod
    def __call__(self, **args):
        """This method needs to be overloaded and will be called by the core."""
        pass
