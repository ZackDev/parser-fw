from __future__ import annotations
from abc import ABC, abstractmethod

class AbstractConfigProvider(ABC):
    def __init__(self, config_name):
        self.config_name = config_name

    @abstractmethod
    def get_source_class(self):
        raise NotImplementedError

    @abstractmethod
    def get_parser_class(self):
        raise NotImplementedError

    @abstractmethod
    def get_sink_class(self):
        raise NotImplementedError

    @abstractmethod
    def get_source_parameters(self):
        raise NotImplementedError

    @abstractmethod
    def get_parser_parameters(self):
        raise NotImplementedError

    @abstractmethod
    def get_sink_parameters(self):
        raise NotImplementedError
