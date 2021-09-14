from abc import ABC, abstractmethod
from abstract.AbstractStep import AbstractStep

class AbstractSequenceRunner(ABC):
    def add_step(self, step: AbstractStep):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
