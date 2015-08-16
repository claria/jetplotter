from abc import ABCMeta, abstractmethod

import inspect

from src.user_parser import UserParser

class Module(object):
    """Base Module all different modules have to be derived from."""
    __metaclass__ = ABCMeta

    @classmethod
    def label(cls):
        return cls.__name__

    def __init__(self):
        self._parser = UserParser(add_help=False)
        self.parser = self._parser.add_argument_group(title=self.label(), description=inspect.getdoc(self))

    @abstractmethod
    def __call__(self, **args):
        """This method needs to be overloaded and will be called for all modules."""
        raise NotImplementedError()

