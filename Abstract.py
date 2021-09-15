from __future__ import annotations
from abc import ABC, abstractmethod
import logging


class StepError(Exception):
    pass


class AbstractStep(ABC):
    def __init__(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
        except Exception as exc:
            raise StepError('setattr error.') from exc
        self.logger = logging.getLogger(type(self).__name__)

    @abstractmethod
    def run(self, data):
        raise NotImplementedError

    def step(self, data):
        self.logger.debug(f'step() called with data: {data}')
        return self.run(data)


class AbstractSequenceRunner(ABC):
    @abstractmethod
    def add_step(self, step: AbstractStep):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError


class AbstractSequenceProvider(ABC):
    def __init__(self, config_name):
        self.config_name = config_name

    @abstractmethod
    def get_sequence(self):
        raise NotImplementedError


class AbstractSequenceProviderAndRunnerFactory(ABC):
    @abstractmethod
    def get_provider(self, sequence_name: str) -> AbstractSequenceProvider:
        raise NotImplementedError

    @abstractmethod
    def get_runner(self, sequence_name: str) -> AbstractSequenceRunner:
        raise NotImplementedError
