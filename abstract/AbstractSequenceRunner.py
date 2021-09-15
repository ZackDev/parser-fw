from abc import ABC, abstractmethod
from abstract.AbstractStep import AbstractStep

class AbstractSequenceRunner(ABC):
    @abstractmethod
    def add_step(self, step: AbstractStep):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError
