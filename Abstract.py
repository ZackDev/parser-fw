from __future__ import annotations
from abc import ABC, abstractmethod
import logging


class StepError(Exception):
    pass


class AbstractStep(ABC):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug(f'__init__() called with kwargs: {kwargs}')
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exception as exc:
            raise StepError('setattr error.') from exc


    @abstractmethod
    def run(self, data):
        raise NotImplementedError

    def step(self, data):
        self.logger.debug(f'step() called with data: {data}')
        return self.run(data)


class AbstractSequenceRunner(ABC):
    @abstractmethod
    def __init__(self, sequence_name):
        raise NotImplementedError

    @abstractmethod
    def add_step(self, step: AbstractStep):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError


class AbstractSequenceProvider(ABC):
    @abstractmethod
    def __init__(self, sequence_name):
        raise NotImplementedError

    @abstractmethod
    def get_sequence(self):
        raise NotImplementedError


class AbstractSequenceProviderAndRunnerFactory(ABC):
    def __init__(self, sequence_name):
        self.sequence_name = sequence_name

    @abstractmethod
    def get_provider(self) -> AbstractSequenceProvider:
        raise NotImplementedError

    @abstractmethod
    def get_runner(self) -> AbstractSequenceRunner:
        raise NotImplementedError
