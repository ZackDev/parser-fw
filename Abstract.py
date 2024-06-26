from __future__ import annotations
from abc import ABC, abstractmethod
import logging


class StepError(Exception):
    pass


class AbstractStep(ABC):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug(f'__init__() called with kwargs: {kwargs}')
        for key, value in kwargs.items():
            if getattr(self, key, None) is None:
                setattr(self, key, value)
            else:
                raise StepError(f'attribute {key} already present.')

    @abstractmethod
    def run(self, data):
        raise NotImplementedError

    def step(self, data):
        self.logger.debug(f'step() called with data: {data}')
        return self.run(data)


class AbstractSequenceRunner(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def add_step(self, step: AbstractStep):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError


class AbstractSequenceProvider(ABC):
    @abstractmethod
    def __init__(self, config_directory: str):
        raise NotImplementedError

    @abstractmethod
    def get_sequence(self, sequence_name: str):
        raise NotImplementedError


class AbstractSequenceProviderAndRunnerFactory(ABC):
    def __init__(self, run_type: str):
        self.run_type = run_type

    @abstractmethod
    def get_provider(self, sequence_name) -> AbstractSequenceProvider:
        raise NotImplementedError

    @abstractmethod
    def get_runner(self) -> AbstractSequenceRunner:
        raise NotImplementedError
