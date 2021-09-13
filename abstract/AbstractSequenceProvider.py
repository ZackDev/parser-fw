from __future__ import annotations
from abc import ABC, abstractmethod

class AbstractSequenceProvider(ABC):
    def __init__(self, config_name):
        self.config_name = config_name

    @abstractmethod
    def get_sequence(self):
        raise NotImplementedError
