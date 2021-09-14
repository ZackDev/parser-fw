from abstract.AbstractSequenceProviderAndRunnerFactory import AbstractSequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProvider
from SequenceRunner import SequenceRunner

class SequenceProviderAndRunnerFactory(AbstractSequenceProviderAndRunnerFactory):
    def get_provider(self, sequence_name: str) -> SequenceProvider:
        return SequenceProvider(sequence_name)

    def get_runner(self, sequence_name: str) -> SequenceRunner:
        return SequenceRunner(sequence_name)
