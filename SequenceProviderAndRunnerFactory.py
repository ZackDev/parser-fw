from Abstract import AbstractSequenceProviderAndRunnerFactory
from SequenceProvider import SequenceProvider
from SequenceRunner import SequenceRunner


class SequenceProviderAndRunnerFactory(AbstractSequenceProviderAndRunnerFactory):
    def get_provider(self) -> SequenceProvider:
        return SequenceProvider(self.sequence_name)

    def get_runner(self) -> SequenceRunner:
        return SequenceRunner(self.sequence_name)
