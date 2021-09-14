from abc import ABC, abstractmethod
from abstract.AbstractSequenceProvider import AbstractSequenceProvider
from abstract.AbstractSequenceRunner import AbstractSequenceRunner

class AbstractSequenceProviderAndRunnerFactory(ABC):
    @abstractmethod
    def get_provider(self, sequence_name: str) -> AbstractSequenceProvider:
        raise NotImplementedError

    @abstractmethod
    def get_runner(self, sequence_name: str) -> AbstractSequenceRunner:
        raise NotImplementedError
